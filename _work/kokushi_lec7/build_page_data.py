import json
F=json.load(open('lec7_final.json')); dg=json.load(open('diag_lec7.json'))
main={}
for l in open('/home/claude/eisei_yakugaku/future_questions.jsonl'):
    r=json.loads(l); main[r['problem_id']]=r
def q(r): return {'text':r['problem_text'],'choices':r['choices'],'answer':r['answer'],'comment':r['comment'],'section':r.get('section','')}
def oldq(pid):
    r=main[pid]; d=q(r)
    if r.get('assets'): d['img']='img/'+r['assets'][0].split('/')[-1]
    return d
rows={(r['problem_id'],r['variant']):r for r in F}
ids=list(dict.fromkeys(r['problem_id'] for r in F))
items=[]
for pid in ids:
    e=rows[(pid,'easy')]; a=rows.get((pid,'advanced'))
    if e['base']=='revised':
        items.append({'id':pid,'lec':'衛I7','kind':'revised','unchanged':False,'pilot':False,'old':oldq(pid),'rev':q(a),'easy':q(e),
          'note':'【やさしい版】'+e['design_note']+'　【発展版】'+a['design_note'],'sources':list(dict.fromkeys(e['sources']+a['sources'])),'tags':[]})
    else:
        items.append({'id':pid,'lec':'衛I7','kind':'pnew','unchanged':False,'pilot':False,'old':None,'rev':None,'easy':q(e),'note':e['design_note'],'sources':e['sources'],'tags':e['tags']})
for it in dg['items']:
    if it['verdict'] in ('merge_delete','move'):
        pid=it['problem_id']; kind='del' if it['verdict']=='merge_delete' else 'move'
        note=(((it.get('move_to')+'。 ') if it.get('move_to') else '')+' '.join(it['issues'])+(' 事実の問題：'+' '.join(it['fact_errors']) if it['fact_errors'] else ''))
        items.append({'id':pid,'lec':'衛I7','kind':kind,'unchanged':False,'pilot':False,'old':oldq(pid),'rev':None,'easy':None,'note':note,'sources':it.get('sources',[]),'tags':[]})
json.dump(items,open('page/lec7_data.json','w'),ensure_ascii=False,indent=1)
olderr={it['problem_id']:it['fact_errors'] for it in dg['items'] if it['fact_errors'] and it['verdict'] in('revise','keep')}
json.dump(olderr,open('page/olderr.json','w'),ensure_ascii=False)
import collections;print(collections.Counter(i['kind'] for i in items), list(olderr))
