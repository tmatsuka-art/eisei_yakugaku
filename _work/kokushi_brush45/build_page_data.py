import json
m=json.load(open('merged.json'))
src='../kokushi_easy/page/'
data=[]; olderr={}; concerns=[]
for f in ['lec4_data.json','lec5_data.json']:
    for x in json.load(open(src+f)):
        x=dict(x)
        o=m.get(x['id'])
        if o:
            e=o['easy']
            x['easy']={'text':e['problem_text'],'choices':e['choices'],'answer':e['answer'],'comment':e['comment'],'section':e.get('section') or x['easy'].get('section')}
            head='【10月15日の見直し】'+o['change_note']
            x['note']=head+'\n\n【10月8日の作成メモ】'+(x.get('note') or '')
            x['sources']=o.get('sources') or x.get('sources')
            if o.get('old_errors'): olderr[x['id']]=o['old_errors']
            for c in o.get('concerns') or []: concerns.append(f"{x['id']}：{c}")
            x['brushed']=o['action']=='fix'
        data.append(x)
json.dump(data,open('page/lec45_data.json','w'),ensure_ascii=False)
json.dump({'old_err':olderr,'concerns':concerns},open('page/extra.json','w'),ensure_ascii=False,indent=1)
print(len(data), len(olderr), len(concerns))
for c in concerns: print(' -',c[:160])
