"""Execute the generated reader's filtering and count explanations on controlled cases."""
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys

import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from publish_practice import build_payload, render


class Controls(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids, self.labels, self.options = {}, {}, {}
        self.select, self.label, self.option = None, None, None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            assert attrs['id'] not in self.ids
            self.ids[attrs['id']] = attrs
        if tag == 'label':
            self.label = attrs.get('for')
            self.labels[self.label] = ''
        if tag == 'select':
            self.select = attrs.get('id')
            self.options[self.select] = {}
        if tag == 'option' and self.select:
            self.option = attrs['value']
            self.options[self.select][self.option] = {'attrs': attrs, 'text': ''}

    def handle_data(self, data):
        if self.label:
            self.labels[self.label] += data
        if self.select and self.option is not None:
            self.options[self.select][self.option]['text'] += data

    def handle_endtag(self, tag):
        if tag == 'label':
            self.label = None
        if tag == 'option':
            self.option = None
        if tag == 'select':
            self.select = None


def execute_reader_functions(html, assertions):
    names = ['filterContext', 'inSelectedPool', 'filterSummaryData', 'updateFilterSummary', 'matches']
    functions = []
    for name in names:
        found = [line for line in html.splitlines() if line.startswith('function ' + name + '(')]
        assert len(found) == 1, name
        functions.append(found[0])
    harness = r'''
const assert=require('assert/strict');
const Q=[
 {question_id:'MA-EXP-0001',family_id:'shared',collection_id:'original',area:1,question_type:'SBA',topic:'refill'},
 {question_id:'MA-RW-0001',family_id:'shared',collection_id:'revision',area:1,question_type:'SBA',topic:'refill'},
 {question_id:'MA-EXP-0002',family_id:'shared',collection_id:'original',area:1,question_type:'SBA',topic:'refill'},
 {question_id:'MA-EXP-0003',family_id:'transfer',collection_id:'original',area:3,question_type:'SATA',topic:'transfer'},
 {question_id:'MA-REV-0001',family_id:'privacy',collection_id:'quality',area:1,question_type:'SBA',topic:'privacy'},
 {question_id:'MA-CASE-0001',family_id:'held',collection_id:'plus',area:4,question_type:'SBA',topic:'privacy'}
];
const D={collections:['original','plus','quality','revision'].map(id=>({id,title:id}))};
const recommendedIds=new Set(['MA-RW-0001','MA-EXP-0003','MA-REV-0001']);
const state={bookmarks:['MA-EXP-0001','MA-REV-0001'],attempts:{'MA-EXP-0001':{correct:false},'MA-CASE-0001':{correct:true}}};
const searchIndex=new Map(Q.map(q=>[q.question_id,(q.question_id+' '+q.topic).toLowerCase()]));
const controls={};
for(const id of ['query','area','qtype','saved','scope','collection','filter-summary','filter-breakdown','filter-exception','filter-session-help','filter-example-text'])controls['#'+id]={value:'',textContent:'',hidden:false};
controls['#collection'].options=[{value:'',dataset:{name:'모든 모음'}},...D.collections.map(group=>({value:group.id,dataset:{name:group.title}}))];
const $=id=>{if(!controls[id])throw Error('Missing control '+id);return controls[id];};
let filtered=[],selectedNoteId='';
function view(changes={}){
 selectedNoteId=changes.note??'';
 const defaults={query:'',area:'',qtype:'',saved:'',scope:'recommended',collection:''};
 for(const [id,value] of Object.entries(defaults))controls['#'+id].value=changes[id]??value;
 controls['#collection'].selectedOptions=[controls['#collection'].options.find(option=>option.value===controls['#collection'].value)];
 filtered=matches();updateFilterSummary();
 return{ids:filtered.map(q=>q.question_id),summary:filterSummaryData(),text:controls['#filter-summary'].textContent,
  exception:controls['#filter-exception'].textContent,exceptionHidden:controls['#filter-exception'].hidden,
  help:controls['#filter-session-help'].textContent,example:controls['#filter-example-text'].textContent};
}
'''
    result = subprocess.run(['node', '-e', harness + '\n'.join(functions) + '\n' + assertions],
        text=True, capture_output=True)
    assert result.returncode == 0, result.stderr


class FilterContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = build_payload()
        cls.reader = data, render(data)

    def test_accessible_controls_distinguish_stored_and_filtered_counts(self):
        data, html = self.reader
        controls = Controls(html)
        assert controls.labels['scope'] == '문항 포함 범위'
        assert controls.labels['collection'] == '문항 모음 (선택)'
        for identifier in ['scope', 'collection', 'practice', 'timed', 'chaos']:
            for described_by in controls.ids[identifier]['aria-describedby'].split():
                assert described_by in controls.ids
        assert controls.ids['filter-summary']['role'] == 'status'
        assert controls.ids['filter-summary']['aria-live'] == 'polite'
        assert controls.ids['filter-summary']['aria-atomic'] == 'true'
        assert 'aria-live' not in controls.ids['result-count']
        assert controls.options['scope']['recommended']['text'] == f"대표·개정 우선 ({len(data['quality_selection']['recommended_ids']):,}개)"
        assert controls.options['scope']['all']['text'] == f"모든 변형 포함 ({len(data['questions']):,}개)"
        assert controls.options['collection']['']['text'] == f"모든 모음 (총 {len(data['questions']):,}개)"
        for collection in data['collections']:
            identifier = collection['id']
            total = sum(q['collection_id'] == identifier for q in data['questions'])
            option = controls.options['collection'][identifier]
            assert option['text'] == f"{option['attrs']['data-name']} (모음 총 {total:,}개)"


    def test_scope_and_collection_intersections_drive_the_visible_count(self):
        execute_reader_functions(self.reader[1], r'''
    let result=view();
    assert.deepEqual(result.ids,['MA-RW-0001','MA-EXP-0003','MA-REV-0001']);
    assert.equal(result.summary.collectionTotal,6);assert.equal(result.summary.scopeCount,3);
    assert.equal(result.text,'현재 조건에 맞는 3문항');
    result=view({collection:'original'});
    assert.deepEqual(result.ids,['MA-EXP-0003']);
    assert.equal(result.summary.collectionTotal,3);assert.equal(result.summary.scopeCount,1);
    assert.match(result.example,/대표·개정 우선 \+ original.*1문항.*모든 변형 \+ original.*3문항/);
    result=view({scope:'all',collection:'original'});
    assert.deepEqual(result.ids,['MA-EXP-0001','MA-EXP-0002','MA-EXP-0003']);
    assert.equal(result.summary.collectionTotal,3);assert.equal(result.summary.scopeCount,3);
    assert.equal(result.summary.familyCount,2);assert.equal(result.summary.standardCeiling,2);
    result=view({query:'refill'});
    assert.deepEqual(result.ids,['MA-RW-0001']);assert.equal(result.summary.scopeCount,3);
    assert.equal(result.summary.matchedCount,1);assert.equal(result.text,'현재 조건에 맞는 1문항');
    result=view({area:'3',qtype:'SATA'});
    assert.deepEqual(result.ids,['MA-EXP-0003']);assert.equal(result.summary.scopeCount,3);
    assert.equal(result.summary.matchedCount,1);assert.equal(result.exceptionHidden,true);
    ''')


    def test_saved_and_id_lookups_only_bypass_the_scope(self):
        execute_reader_functions(self.reader[1], r'''
    let result=view({saved:'bookmarks',collection:'original'});
    assert.deepEqual(result.ids,['MA-EXP-0001']);assert.equal(result.summary.scopeCount,3);
    assert.equal(result.summary.archiveReason,'북마크 복습');assert.equal(result.exceptionHidden,false);
    assert.match(result.exception,/선택한 모음과 나머지 필터는 계속 적용/);
    result=view({saved:'wrong',collection:'original'});
    assert.deepEqual(result.ids,['MA-EXP-0001']);assert.equal(result.summary.archiveReason,'오답 복습');
    result=view({query:'  MA-EXP-0001  '});
    assert.deepEqual(result.ids,['MA-EXP-0001']);assert.equal(result.summary.archiveReason,'ID 검색');
    result=view({query:'MA-EXP-0001',collection:'revision'});
    assert.deepEqual(result.ids,[]);assert.equal(result.summary.scopeCount,1);
    assert.equal(result.text,'현재 조건에 맞는 0문항');assert.match(result.help,/조건에 맞는 문항이 없습니다/);
    result=view({saved:'bookmarks',area:'3'});assert.deepEqual(result.ids,[]);
    result=view({saved:'wrong',qtype:'SATA'});assert.deepEqual(result.ids,[]);
    result=view({query:'ma-',area:'3'});assert.deepEqual(result.ids,['MA-EXP-0003']);
    result=view({scope:'all',saved:'bookmarks'});
    assert.deepEqual(result.ids,['MA-EXP-0001','MA-REV-0001']);assert.equal(result.exceptionHidden,true);
    ''')

    def test_note_filter_uses_exact_evidence_and_survives_archive_exceptions(self):
        execute_reader_functions(self.reader[1], r'''
    for(const q of Q)q.note_evidence=[{unit_id:q.family_id==='shared'?'note-a':'note-b'}];
    let result=view({note:'note-a'});
    assert.deepEqual(result.ids,['MA-RW-0001']);assert.equal(result.summary.scopeCount,1);
    result=view({note:'note-a',scope:'all'});
    assert.deepEqual(result.ids,['MA-EXP-0001','MA-RW-0001','MA-EXP-0002']);
    assert.equal(result.summary.familyCount,1);
    result=view({note:'note-a',saved:'wrong'});
    assert.deepEqual(result.ids,['MA-EXP-0001']);
    result=view({note:'note-b',query:'MA-EXP-0001'});
    assert.deepEqual(result.ids,[]);
    result=view({note:'unknown'});assert.deepEqual(result.ids,[]);
    result=view({note:'note-a',collection:'quality'});assert.deepEqual(result.ids,[]);
    ''')


    def test_session_ceilings_follow_distinct_families_and_existing_limits(self):
        execute_reader_functions(self.reader[1], r'''
    let result=view({scope:'all'});
    assert.equal(result.summary.matchedCount,6);assert.equal(result.summary.familyCount,4);
    assert.equal(result.summary.standardCeiling,4);assert.equal(result.summary.timedCeiling,4);
    assert.match(result.help,/같은 사례·지문·보기의 반복을 제외/);
    Q.splice(0,Q.length,...Array.from({length:130},(_,i)=>({question_id:'test-'+i,family_id:'f'+(i===129?0:i),collection_id:'original',area:1,question_type:'SBA'})));
    recommendedIds.clear();searchIndex.clear();
    for(const q of Q){recommendedIds.add(q.question_id);searchIndex.set(q.question_id,q.question_id);}
    result=view({collection:'original'});
    assert.equal(result.summary.collectionTotal,130);assert.equal(result.summary.matchedCount,130);
    assert.equal(result.summary.familyCount,129);
    assert.equal(result.summary.standardCeiling,20);assert.equal(result.summary.timedCeiling,120);
    assert.equal(result.text,'현재 조건에 맞는 130문항');
    assert.match(result.help,/일반 연습 최대 20문항 · 시간 연습 최대 120문항/);
    ''')
