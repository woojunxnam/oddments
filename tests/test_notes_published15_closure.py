"""Synthetic GitHub/HTTP fixtures only; no real publication proof is invented."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import notes_published15_closure as c
HELPER='tests/synthetic-future-helper.py'


def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()


def put(root,p,value):
    raw=value if isinstance(value,bytes)else c.encoded(value)
    target=root/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    return {'path':p,'raw_sha256':c.sha(raw)}


def commit(root,message):
    git(root,'add','-f','.');git(root,'commit','-qm',message)


@pytest.fixture
def published(tmp_path,monkeypatch):
    root=tmp_path/'fixture';root.mkdir();git(root,'init','-q');git(root,'config','user.name','Synthetic fixture');git(root,'config','user.email','fixture@example.invalid')
    # Source fixture1781 is a count/integrity test, not a pharmacy-law corpus.
    protected=[c.EXPORT,'notes/guide.json',*sorted(c.POLICIES)]
    protected += ['data/fixture/%04d.json'%i for i in range(1781-len(protected))]
    for p in protected:put(root,p,('SYNTHETIC OLD '+p+'\n').encode())
    put(root,c.BUILD,{'content_sha256':'e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824'})
    put(root,c.FOURTEENTH,(ROOT/c.FOURTEENTH).read_bytes())
    put(root,c.FIFTEENTH,dict(annotation_inputs_ready=True,purpose='FIFTEENTH_ANNOTATION_LAYER_NOT_SEMANTIC_OR_AUDIT_APPROVAL',
        semantic_notes_sha256='e1519c0290ff220eb8251307e26340d76d394a7ec1f3e651194d4495a03f1824',
        source_bindings={'notes/guide.json':c.sha((root/'notes/guide.json').read_bytes())}))
    put(root,c.PROTECTED,{'files':[{'path':p}for p in protected]})
    put(root,'scripts/notes_revision.py',b'M\n')
    put(root,HELPER,b'SYNTHETIC OLD UNCHANGED HELPER\n')
    put(root,'revisions/baselines/complete-notes-2026-10-23.1.md',b'SYNTHETIC ORIGINAL BASELINE\n')
    # Keep the real immutable14 tail, but the synthetic fixture exits in a
    # clearly marked prefix after testing only the reconstructed HEAD routing.
    guard=(ROOT/c.OLD_GUARD).read_text()
    early='''if __name__=='__main__':
    from pathlib import Path
    import subprocess
    r=Path(__file__).resolve().parents[1]
    assert (r/'scripts/notes_revision.py').read_bytes()==b'M\\n'
    assert subprocess.check_output(['git','-C',str(r),'show','HEAD:scripts/notes_revision.py'])==b'M\\n'
    assert b'OLD' in (r/'site/notes/complete-notes.md').read_bytes()
    print('SYNTHETIC OLD-GUARD FIXED-HEAD VIEW VERIFIED; NOT A REAL RELEASE')
    raise SystemExit(0)

'''
    marker='ROOT = Path(__file__).resolve().parents[1]'
    assert marker in guard
    put(root,c.OLD_GUARD,(guard.replace(marker,early+marker,1)).encode())
    put(root,c.OLD15_CODE,b'SYNTHETIC IMMUTABLE OLD15 SOURCE\n')
    commit(root,'synthetic tested and published source tree')
    published=git(root,'rev-parse','HEAD');tree=git(root,'rev-parse','HEAD^{tree}')
    def primary(name,payload,url):
        ref=put(root,c.RECEIPTS+name,payload)
        return {**ref,'official_url':url,'http_status':200,'tls_verified':True,'retrieved_at_utc':'2026-11-04T08:00:00+00:00'}
    pr=primary('pull.json',dict(number=192,merged=True,merged_at='2026-11-04T07:00:00Z',merge_commit_sha=published,
        head={'sha':published},base={'ref':'main','repo':{'full_name':c.REPOSITORY}}),c.API+'pulls/192')
    cp=primary('commit.json',{'sha':published,'commit':{'tree':{'sha':tree}}},c.API+'commits/'+published)
    def run(ident,workflow):
        return primary(str(ident)+'.json',dict(id=ident,repository={'full_name':c.REPOSITORY},head_sha=published,
            head_branch='main',path=workflow,status='completed',conclusion='success'),c.API+'actions/runs/'+str(ident))
    qa=run(10,'.github/workflows/qa.yml');pages=run(11,'.github/workflows/pages.yml')
    assets=[{'source_path':p,'payload':primary('asset-'+Path(p).name,(root/p).read_bytes(),c.ORIGIN+p.removeprefix('site/'))}for p in [c.EXPORT,c.BUILD]]
    receipt=dict(schema_version=1,status='ACTUAL_PUBLISHED_VERIFIED',controller_actor='/root',repository=c.REPOSITORY,
        published_commit=published,tested_commit=published,published_tree=tree,pull_number=192,pull=pr,
        published_commit_payload=cp,tested_commit_payload=cp,ci_runs=[qa],pages_run=pages,public_assets=assets,
        canonical_release_credit=0,question_audit_credit=0)
    ref=put(root,c.RECEIPTS+'receipt.json',receipt)
    # Current N-facing code/output differ; immutable inputs and old manifests do not.
    put(root,'scripts/notes_revision.py',b'N1 LIVE MUST NEVER REACH THE OLD GUARD\n')
    put(root,c.EXPORT,b'SYNTHETIC CURRENT N1\n');put(root,c.BUILD,{'current':'N1'})
    commit(root,'synthetic retained HTTP proof and current N-facing files')
    closure,writes=c.prepare(root,published,ref)
    for p,raw in writes.items():put(root,p,raw)
    binding=put(root,c.CLOSURE_PREFIX+'fixture-v1.json',closure);commit(root,'synthetic immutable exact closure retention')
    monkeypatch.setattr(c,'APPROVED_CLOSURES',{(binding['path'],binding['raw_sha256']):{'published_commit':published,'published_tree':tree}})
    return root,ref,receipt,binding,closure


def reapprove(root,binding,value,monkeypatch):
    new=put(root,binding['path'],value);commit(root,'synthetic invalid rehash test')
    monkeypatch.setattr(c,'APPROVED_CLOSURES',{(new['path'],new['raw_sha256']):{'published_commit':value['published_commit'],'published_tree':value['published_tree']}})
    return new


def test_full_tree_fixed_head_uses_old_preimages_and_not_live_n1(published):
    root,_,_,binding,value=published
    assert len(value['protected_current_raw_sha256'])==1781
    assert set(value['retained_preimages'])=={'scripts/notes_revision.py',c.EXPORT,c.BUILD}
    result=c.verify_old_guards(root,binding)
    assert result['old_git_objects_required']is False and result['original_markdown']==b'SYNTHETIC ORIGINAL BASELINE\n'
    assert b'N1 LIVE'in(root/'scripts/notes_revision.py').read_bytes()


def test_runtime_shallow_checkout_has_no_original_published_commit(published,tmp_path):
    root,_,_,binding,value=published;shallow=tmp_path/'shallow'
    subprocess.run(['git','clone','-q','--depth','1',root.as_uri(),str(shallow)],check=True)
    with pytest.raises(subprocess.CalledProcessError):git(shallow,'cat-file','-e',value['published_commit']+'^{commit}')
    assert c.verify_old_guards(shallow,binding)['original_markdown']==b'SYNTHETIC ORIGINAL BASELINE\n'


@pytest.mark.parametrize('defect',['proposed','failed_ci','wrong_ci_tree','failed_pages','wrong_pages_tree','asset_error_page','tls','official_origin','credit_type'])
def test_missing_or_false_primary_publication_proof_is_not_a_publish_receipt(published,defect):
    root,ref,receipt,binding,value=published;receipt=copy.deepcopy(receipt)
    if defect=='proposed':receipt['status']='PROPOSED'
    elif defect=='credit_type':receipt['canonical_release_credit']=False
    elif defect in {'failed_ci','wrong_ci_tree','failed_pages','wrong_pages_tree'}:
        item=receipt['ci_runs'][0]if 'ci'in defect else receipt['pages_run'];raw=json.loads((root/item['path']).read_bytes())
        if defect.startswith('failed'):raw['conclusion']='failure'
        else:raw['head_sha']='0'*40
        new=put(root,item['path'],raw);item['raw_sha256']=new['raw_sha256']
    elif defect=='asset_error_page':
        item=receipt['public_assets'][0]['payload'];new=put(root,item['path'],b'HTTP200 access denied');item['raw_sha256']=new['raw_sha256']
    elif defect=='tls':receipt['pages_run']['tls_verified']=False
    else:receipt['pages_run']['official_url']='https://example.invalid/actions/runs/11'
    newref=put(root,ref['path'],receipt);commit(root,'synthetic invalid publication proof')
    with pytest.raises(ValueError):c.prepare(root,value['published_commit'],newref)


@pytest.mark.parametrize('defect',['missing_preimage','wrong_origin','drop_old_file','wrong_blob','wrong_tree','wrong1781','credit'])
def test_even_rehashed_closure_cannot_skip_changed_paths_or_expand_aliases(published,monkeypatch,defect):
    root,_,_,binding,value=published;value=copy.deepcopy(value)
    if defect=='missing_preimage':value['retained_preimages'].pop('scripts/notes_revision.py')
    elif defect=='wrong_origin':value['retained_preimages']['scripts/notes_revision.py']['path']='reports/full-corpus-review/progress.json'
    elif defect=='drop_old_file':value['full_source_files'].pop('scripts/verify_representative_protected.py')
    elif defect=='wrong_blob':value['full_source_files']['scripts/notes_revision.py']['git_blob_sha1']='0'*40
    elif defect=='wrong_tree':value['published_tree']='0'*40
    elif defect=='wrong1781':value['protected_current_raw_sha256'].pop(next(iter(value['protected_current_raw_sha256'])))
    else:value['question_audit_credit']=False
    new=reapprove(root,binding,value,monkeypatch)
    with pytest.raises(ValueError):c.verify_old_guards(root,new)


def test_current_governance_cannot_be_replaced_by_a_retained_old_alias(published,monkeypatch):
    root,_,_,binding,value=published;value=copy.deepcopy(value);policy=next(iter(c.POLICIES))
    original=(root/policy).read_bytes();dest=c.PREIMAGES+value['published_commit']+'/'+policy
    put(root,dest,original);put(root,policy,b'Changed current policy must fail')
    value['retained_preimages'][policy]={'path':dest,'raw_sha256':c.sha(original)}
    new=reapprove(root,binding,value,monkeypatch)
    with pytest.raises(ValueError,match='raw SHA changed'):c.verify_old_guards(root,new)


@pytest.mark.parametrize('source',[c.OLD15_CODE,c.OLD_GUARD,c.PROTECTED])
def test_immutable_old_code_and_protection_inventory_are_not_hidden_by_preimages(published,monkeypatch,source):
    root,_,_,binding,value=published;value=copy.deepcopy(value);raw=(root/source).read_bytes()
    dest=c.PREIMAGES+value['published_commit']+'/'+source;put(root,dest,raw)
    put(root,source,raw+b'\n# unauthorized current change\n')
    value['retained_preimages'][source]={'path':dest,'raw_sha256':c.sha(raw)}
    new=reapprove(root,binding,value,monkeypatch)
    with pytest.raises(ValueError):c.verify_old_guards(root,new)


def test_root_only_preparation_does_not_grant_approval_or_activate(published):
    root,ref,_,_,value=published
    with pytest.raises(ValueError,match='Only root'):
        c.write_preparation(root,'worker',value['published_commit'],ref,c.CLOSURE_PREFIX+'another.json')


def retain_all(published,monkeypatch):
    root,ref,_,_,old=published
    value,writes=c.prepare(root,old['published_commit'],ref,retain_all=True)
    assert set(value['retained_preimages'])==set(value['full_source_files'])
    for relative,raw in writes.items():put(root,relative,raw)
    binding=put(root,c.CLOSURE_PREFIX+'fixture-full-v2.json',value)
    commit(root,'synthetic immutable full old-tree retention')
    monkeypatch.setattr(c,'APPROVED_CLOSURES',{
        **c.APPROVED_CLOSURES,(binding['path'],binding['raw_sha256']):{
            'published_commit':value['published_commit'],'published_tree':value['published_tree']}})
    return root,binding,value


def test_retain_all_recovers_a_later_changed_previously_unchanged_helper(published,monkeypatch):
    root,_,_,_,default=published
    assert HELPER not in default['retained_preimages']
    original=(root/HELPER).read_bytes()
    root,binding,value=retain_all(published,monkeypatch)
    assert value['full_source_files']==default['full_source_files']
    assert value['published_tree']==default['published_tree']
    assert value['retained_preimages'][HELPER]=={
        'path':c.PREIMAGES+value['published_commit']+'/'+HELPER,'raw_sha256':c.sha(original)}
    put(root,HELPER,b'SYNTHETIC LATER LEGITIMATE CURRENT HELPER\n')
    commit(root,'synthetic later current helper change')
    assert c.old_bytes(root,value,HELPER)==original
    with pytest.raises(ValueError,match='SOURCE_BLOCKED'):
        c.old_bytes(root,default,HELPER)
    with c.fixed_view(root,binding)as(view,closure):
        assert (view/HELPER).read_bytes()==original
        assert git(view,'rev-parse','HEAD^{tree}')==default['published_tree']
    assert b'LATER LEGITIMATE'in(root/HELPER).read_bytes()


def test_full_retained_preimage_mutation_fails_even_when_current_still_matches(published,monkeypatch):
    root,binding,value=retain_all(published,monkeypatch)
    target=value['retained_preimages'][HELPER]['path']
    put(root,target,b'SYNTHETIC ALTERED PREIMAGE\n');commit(root,'synthetic invalid retained blob')
    with pytest.raises(ValueError,match='raw SHA changed'):
        c.validate(root,binding,coverage=True)


@pytest.mark.parametrize('source',[HELPER,c.FIFTEENTH])
def test_retain_all_cannot_overwrite_any_existing_preimage(published,source):
    root,ref,_,_,value=published
    target=c.PREIMAGES+value['published_commit']+'/'+source
    put(root,target,b'SYNTHETIC CONFLICTING EXISTING PREIMAGE\n')
    with pytest.raises(ValueError,match='Cannot overwrite'):
        c.prepare(root,value['published_commit'],ref,retain_all=True)
    assert (root/target).read_bytes()==b'SYNTHETIC CONFLICTING EXISTING PREIMAGE\n'


@pytest.mark.parametrize('source',[sorted(c.POLICIES)[0],c.OLD15_CODE,'data/fixture/0000.json'])
def test_full_preimages_do_not_relax_current_frozen_inputs(published,monkeypatch,source):
    root,binding,value=retain_all(published,monkeypatch)
    assert source in value['retained_preimages']
    put(root,source,(root/source).read_bytes()+b'SYNTHETIC UNAUTHORIZED CURRENT CHANGE\n')
    commit(root,'synthetic forbidden frozen current change')
    with pytest.raises(ValueError,match='raw SHA changed'):
        c.validate(root,binding,coverage=True)


def test_root_prepare_cli_retain_all_preserves_existing_manifest_and_requires_new_path(published):
    import note_review_queue as q
    root,ref,_,_,value=published
    put(root,q.STATE,q.empty(root));commit(root,'synthetic root-owned empty note checkpoint')
    output=c.CLOSURE_PREFIX+'cli-full-v2.json'
    result=subprocess.run([sys.executable,str(ROOT/'scripts/notes_published15_closure.py'),
        '--root',str(root),'--actor','/root','--prepare','--retain-all',
        '--published-commit',value['published_commit'],'--receipt',ref['path'],'--output',output],
        capture_output=True,text=True,check=True)
    metadata=json.loads(result.stdout);full=json.loads((root/output).read_bytes())
    assert metadata['preimages']==len(value['full_source_files'])
    assert set(full['retained_preimages'])==set(full['full_source_files'])
    assert (output,metadata['raw_sha256'])not in c.APPROVED_CLOSURES
    # An existing partial closure cannot silently become a different full one.
    with pytest.raises(ValueError,match='Refusing to replace'):
        c.write_preparation(root,'/root',value['published_commit'],ref,
            c.CLOSURE_PREFIX+'fixture-v1.json',retain_all=True)
    assert json.loads((root/c.CLOSURE_PREFIX/'fixture-v1.json').read_bytes())==value
