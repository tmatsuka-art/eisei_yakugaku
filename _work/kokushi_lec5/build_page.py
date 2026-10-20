import json, html, re, shutil
D=json.load(open('diag_lec5.json'))
diag={x['problem_id']:x for x in D['items']}
orig={json.loads(l)['problem_id']:json.loads(l) for l in open('lec5_future.jsonl')}
final=[json.loads(l) for l in open('final_lec5.jsonl')]
ver={}
for f in ['verify_0.json','verify_1.json','verify_2.json']:
    for v in json.load(open(f)): ver[v['problem_id']]=v
def q(d,after=False):
    o={'section':d.get('section') or '', 'text':d['problem_text'],'choices':d['choices'],'answer':[str(a) for a in d['answer']],'comment':d['comment']}
    if after: o['image']= d['problem_id']=='F227'
    else: o['image']= bool(d.get('num_images'))
    return o
items=[]
for r in final:
    pid=r['problem_id']; v=ver.get(pid,{})
    chk = '合格' if v.get('severity')=='ok' else ('修正のうえ合格' if v.get('severity')=='major' else '小修正のうえ合格')
    if pid in orig:
        o=orig[pid]
        items.append({'id':pid,'lec':5,'verdict':r['verdict'],'summary':r['change_summary'],'kind':'',
          'before':q(o),'after':q(r,True),'sources':r.get('sources',[]),'check':chk,
          'issues':diag[pid].get('issues',[]),'code':[o.get('new_corecurri_code'),r.get('new_corecurri_code')],'tags':[]})
    else:
        items.append({'id':pid,'lec':5,'verdict':'new','summary':r.get('note',''),'kind':'新コアカリ対応' if r.get('kind')=='curri' else '抜け',
          'after':q(r,True),'sources':r.get('sources',[]),'check':chk,'issues':[],'code':[None,r.get('new_corecurri_code')],'tags':r.get('tags',[])})
for pid,dg in diag.items():
    if dg['verdict']=='merge_delete':
        o=orig[pid]
        vd='move' if pid=='F1235' else 'merge_delete'
        summ = 'この回（栄養）の範囲外なので、公衆衛生「第7回 社会的影響・国際動向」へ移します（内容はその回の点検で見直します）。' if pid=='F1235' else dg['plan']
        items.append({'id':pid,'lec':5,'verdict':vd,'summary':summ,'kind':'','before':q(o),'sources':dg.get('sources',[]),
          'issues':dg.get('issues',[])+[('事実の誤り：'+x) for x in dg.get('fact_errors',[])],'code':[o.get('new_corecurri_code'),None],'tags':[]})
order={'rewrite':0,'polish':0,'keep':0,'new':1,'merge_delete':2,'move':2}
items.sort(key=lambda x:order[x['verdict']])
json.dump(items,open('page/page_lec5_data.json','w'),ensure_ascii=False)
print(len(items),{k:sum(1 for x in items if x['verdict']==k) for k in order})
