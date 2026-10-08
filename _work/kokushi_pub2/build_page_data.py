import json
F=json.load(open('pub2_final.json')); dg=json.load(open('diag_pub2.json'))
main={}
for l in open('/home/claude/eisei_yakugaku/future_questions.jsonl'):
    r=json.loads(l); main[r['problem_id']]=r
def q(r): return {'text':r['problem_text'],'choices':r['choices'],'answer':r['answer'],'comment':r['comment'],'section':r.get('section','')}
def oldq(pid):
    r=main[pid]; d=q(r)
    assert not r.get('assets') and not r.get('image'), pid
    return d
rows={(r['problem_id'],r['variant']):r for r in F}
ids=[]; [ids.append(r['problem_id']) for r in F if r['problem_id'] not in ids]
items=[]
for pid in ids:
    e=rows.get((pid,'easy')); a=rows.get((pid,'advanced'))
    if e['base']=='revised':
        note='【やさしい版】'+e['design_note']+'　【発展版】'+a['design_note']
        src=list(dict.fromkeys(e['sources']+a['sources']))
        items.append({'id':pid,'lec':'公衆2','kind':'revised','unchanged':False,'pilot':False,'old':oldq(pid),'rev':q(a),'easy':q(e),'note':note,'sources':src,'tags':[]})
    else:
        items.append({'id':pid,'lec':'公衆2','kind':'pnew','unchanged':False,'pilot':False,'old':None,'rev':None,'easy':q(e),'note':e['design_note'],'sources':e['sources'],'tags':e['tags']})
for it in dg['items']:
    if it['verdict'] in ('merge_delete','move'):
        pid=it['problem_id']; kind='del' if it['verdict']=='merge_delete' else 'move'
        note=(('移動先：' if kind=='move' else '')+(it.get('move_to') or '')+'。'+' '.join(it['issues'])+(' 事実の問題：'+' '.join(it['fact_errors']) if it['fact_errors'] else ''))
        items.append({'id':pid,'lec':'公衆2','kind':kind,'unchanged':False,'pilot':False,'old':oldq(pid),'rev':None,'easy':None,'note':note,'sources':it.get('sources',[]),'tags':[]})
json.dump(items,open('page/pub2_data.json','w'),ensure_ascii=False,indent=1)
import collections;print(collections.Counter(i['kind'] for i in items))
olderr={it['problem_id']:it['fact_errors'] for it in dg['items'] if it['fact_errors'] and it['verdict'] in('revise','keep')}
json.dump(olderr,open('page/olderr.json','w'),ensure_ascii=False)
print(list(olderr))
