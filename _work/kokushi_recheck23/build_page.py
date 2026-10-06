import json
D='kokushi_recheck23/'
now={json.loads(l)['problem_id']:json.loads(l) for n in (2,3) for l in open(D+f'lec{n}_now.jsonl')}
logs={x['problem_id']:x for n in (2,3) for x in json.load(open(D+f'lec{n}_fix_log.json'))}
V={x['problem_id']:x for x in json.load(open(D+'verify_fix.json'))}
items=[]
for n in (2,3):
    for l in open(D+f'lec{n}_fix_final.jsonl'):
        r=json.loads(l); p=r['problem_id']; o=now[p]; lg=logs.get(p,{})
        s=lg.get('summary','')
        cg=lg.get('chatgpt') or []
        if cg: s+=' 【ChatGPTの指摘】'+' / '.join(f"{c['point']}→{c['verdict']}" for c in cg)
        stem=(r['problem_text']!=o['problem_text'] or r['choices']!=o['choices'])
        items.append({'id':p,'lec':n,'verdict':'rewrite' if stem else 'keep','summary':s,
            'before':{'section':o['section'],'text':o['problem_text'],'choices':o['choices'],'answer':o['answer'],'comment':o['comment'],'image':False},
            'after':{'section':r['section'],'text':r['problem_text'],'choices':r['choices'],'answer':r['answer'],'comment':r['comment']},
            'sources':[],'check':('合格' if V[p]['verdict']=='pass' else '小修正のうえ合格') if p in V else '','issues':[]})
t=open(D+'page_fix_template.html').read()
import re
t=re.sub(r'承認済み48問のうち修正案のある\d+問',f'承認済み48問のうち修正案のある{len(items)}問',t)
d=json.dumps(items,ensure_ascii=False).replace('</','<\\/')
open(D+'review_fix23.html','w').write(t.replace('__DATA__',d))
print(len(items))
