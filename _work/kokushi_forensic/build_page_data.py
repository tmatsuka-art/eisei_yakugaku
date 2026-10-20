import json
F=json.load(open('fx_final.json'))
def q(r): return {'text':r['problem_text'],'choices':r['choices'],'answer':r['answer'],'comment':r['comment'],'section':r.get('section','')}
items=[{'id':r['problem_id'],'lec':'衛II7','kind':'pnew','unchanged':False,'pilot':False,'old':None,'rev':None,'easy':q(r),'note':r['design_note'],'sources':r['sources'],'tags':r['tags']} for r in F]
json.dump(items,open('page/fx_data.json','w'),ensure_ascii=False,indent=1)
print(len(items))
