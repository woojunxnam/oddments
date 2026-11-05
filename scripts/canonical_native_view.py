"""Read-only immutable Git registry view for actual native validator execution.

External proposals remain private. This module never enrolls or promotes records.
"""
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from types import MappingProxyType
import json
import subprocess

from canonical_successor import BoundaryViolation, read_committed_preimages, require, safe_path, strict_json


class NativeView:
    def __init__(self, root, base_commit, replacements=None):
        self._root=Path(root).resolve();self._base_commit=base_commit
        self._replacements=dict(replacements or {})
        for path in self.replacements:safe_path(path)
        raw=subprocess.check_output(['git','-C',str(self.root),'ls-tree','-r','-z',base_commit])
        self._tree={}
        for row in raw.split(b'\0'):
            if row:
                meta,path=row.split(b'\t',1);mode,kind,oid=meta.split();path=path.decode()
                if kind==b'blob' and mode in {b'100644',b'100755'}:self._tree[path]=oid.decode()
        needed=[p for p in self.tree if p.endswith('.json') and p.startswith(('data/','schemas/'))]
        self._cache=read_committed_preimages(self.root,base_commit,needed)
        self._cache.update(self.replacements)

    @property
    def root(self):return self._root
    @property
    def base_commit(self):return self._base_commit
    @property
    def replacements(self):return MappingProxyType(self._replacements)
    @property
    def tree(self):return MappingProxyType(self._tree)
    @property
    def cache(self):return MappingProxyType(self._cache)

    def relative(self,path):
        path=Path(path)
        require(path.is_absolute(),'Native reader requires an absolute canonical path')
        try:relative=path.relative_to(self.root).as_posix()
        except ValueError:raise BoundaryViolation('Native reader path outside canonical root')
        safe_path(relative);return relative

    def read(self,relative):
        safe_path(relative)
        if relative not in self.cache:
            require(relative in self.tree,'Native reader missing immutable source: '+relative)
            self._cache.update(read_committed_preimages(self.root,self.base_commit,[relative]))
        return self.cache[relative]

    def load_json(self,path):
        # Fresh values prevent a producer mutating the trusted in-memory preimage.
        return strict_json(self.read(self.relative(path)))

    def iter_json_files(self,directory):
        relative=self.relative(directory);prefix=relative+'/'
        return [self.root/path for path in sorted(set(self.tree)|set(self.replacements))
            if path.startswith(prefix) and '/' not in path[len(prefix):] and path.endswith('.json')]

    def load_records(self,directory):
        return [(path,self.load_json(path))for path in self.iter_json_files(directory)]


def native_validation(view, *, release=False, withdrawal_context=None):
    """Run actual native checks, never a supplied PASS summary or substitute schema."""
    from qa_common import QAReport, canonical_read_view, load_json
    from validate_rules import validate_rules
    from validate_drugs import validate_drugs
    from validate_audits import validate_audits
    from validate_questions import validate_questions
    from validate_governance import validate_governance
    from validate_study_guide import validate_study_guide
    from validate_study_guide_audits import validate_study_guide_audits
    from check_placeholders import check_placeholders
    from check_private_paths import check_private_paths
    from check_study_guide_scope_coverage import scope_coverage_report
    from validate_all import validate_blueprint
    from check_answer_cue_patterns import answer_cue_report
    from check_answer_distribution import analyze_answer_distribution
    from check_structural_patterns import analyze_structural_patterns
    from check_sba_answer_length import analyze_sba_answer_length
    from detect_duplicates import detect_duplicates
    from release_context import validate_release_date
    from datetime import date
    result=QAReport()
    with canonical_read_view(view):
        rule_report,rules=validate_rules();result.extend(rule_report)
        drug_report,drugs=validate_drugs(rules);result.extend(drug_report)
        # Question/audit schemas are checked even for unreleased preflight records.
        audit_report,audits=validate_audits();result.extend(audit_report)
        question_report,questions=validate_questions(rules,drugs,audits);result.extend(question_report)
        audit_report,_=validate_audits(set(questions));result.extend(audit_report)
        result.extend(validate_governance(rules,questions))
        # Do not crash subsequent validators on malformed schemas/dependencies.
        if not result.ok:return result,questions
        guide_report,_=validate_study_guide(rules,questions,withdrawal_context=withdrawal_context)
        result.extend(guide_report)
        guide_audit_report,_=validate_study_guide_audits();result.extend(guide_audit_report)
        result.extend(check_placeholders());result.extend(check_private_paths())
        result.extend(scope_coverage_report());result.extend(validate_blueprint())
        result.extend(answer_cue_report(questions=questions))
        duplicate=detect_duplicates()
        if duplicate['finding_count']:result.error('native duplicate detector: '+str(duplicate['finding_count'])+' findings')
        distribution,failed=analyze_answer_distribution()
        if failed:result.error('native answer distribution gate failed')
        structural,failed=analyze_structural_patterns()
        if failed:result.error('native structural-pattern gate failed: '+str(structural['finding_count']))
        length,failed=analyze_sba_answer_length()
        if failed:result.error('native SBA length gate failed')
        if release:
            result.extend(validate_release_date(load_json(view.root/'data/blueprint.json'),
                load_json(view.root/'data/exam_style/mpje_style_profile.json'),reference_date=date.today()))
    return result,questions
