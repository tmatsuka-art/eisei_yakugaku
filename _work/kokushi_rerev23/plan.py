"""鈴木先生の判断（lec23）→ アプリ反映案（disposition）と確認ページ用データを作る。"""
import json, glob, os
B='/home/claude/eisei_yakugaku/_work/'
data={x['id']:x for x in json.load(open(B+'kokushi_easy/page/lec23_data.json'))}
dec={os.path.basename(f)[:-5]:json.load(open(f)) for f in glob.glob(B+'kokushi_rerev23/suzuki_db/*.json')}
log=json.load(open(B+'kokushi_easy/apply_log_lec23.json'))
copy={}; added={}
for o,a,n in log:
    if a=='発展': copy[o]=n
    if a=='add': added[o]=n
rerev={x['id']:x for x in json.load(open(B+'kokushi_rerev23/rerev_draft.json'))}
LAB={'easy':'やさしい版','rev':'発展版','old':'旧版'}
plan=[]
for i,it in data.items():
    d=dec[i]; vs=d.get('versions') or []; note=d.get('note','')
    touched=not d.get('updatedAt','').startswith('2026-10-08')
    p={'id':i,'lec':it['lec'],'kind':it['kind'],'sel':vs,'note':note,'touched':touched}
    acts=[]
    if not touched:
        p['main']='今のまま'; acts.append('変更なし（鈴木先生の判断なし。10月8日の反映のまま）')
    elif it['kind']=='new':
        if not vs:
            if note=='不要':
                p['main']='削除'; acts.append(f'{i}（元の新作）を削除')
                if i in added: acts.append(f'{added[i]}（やさしい版）を削除')
            else:
                p['main']='保留'; acts.append('選択なし・コメントなし → 今のまま（先生のご判断待ち）')
        elif vs==['easy']:
            p['main']='やさしい版'; acts.append(f'{i} をやさしい版に置き換え')
            if i in added: acts.append(f'{added[i]}（やさしい版の追加分）は重複になるので削除')
        elif vs==['rev']:
            p['main']='元の新作'; acts.append(f'{i}（元の新作）のまま')
            if i in added: acts.append(f'{added[i]}（やさしい版）を削除')
    else:
        if not vs:
            p['main']='今のまま'; acts.append('選択なし → 今のまま（変更なしの問題）')
        else:
            m=[k for k in ('easy','rev','old') if k in vs][0]; p['main']=LAB[m]
            r=' ＝再改訂版' if (i in rerev and rerev[i]['target']==m) else ''
            acts.append(f'{i} に{LAB[m]}{r}' + ('' if m=='easy' else '（今のやさしい版と入れ替え）'))
            if 'rev' in vs and m!='rev':
                r2=' ＝再改訂版' if (i in rerev and rerev[i]['target']=='rev') else ''
                acts.append(f'{copy.get(i,"新しい番号")} に発展版{r2}（「発展」タグ）')
            elif i in copy:
                acts.append(f'{copy[i]}（発展版のコピー）を削除')
            if 'old' in vs and m!='old':
                r3=' ＝再改訂版' if (i in rerev and rerev[i]['target']=='old') else ''
                acts.append(f'新しい番号に旧版{r3}を追加（「旧版」タグ）')
    p['acts']=acts; p['rerev']=i in rerev
    plan.append(p)
order=lambda p:(p['lec'], int(p['id'][1:]))
plan.sort(key=order)
json.dump(plan,open(B+'kokushi_rerev23/apply_plan.json','w'),ensure_ascii=False,indent=1)
# page data
def q(v): return None if not v else {'text':v['text'],'choices':v['choices'],'answer':v['answer'],'comment':v['comment'],'section':v.get('section','')}
items=[]
for p in plan:
    i=p['id']; it=data[i]
    if i in rerev:
        r=rerev[i]; before=it[r['target']]
        items.append({'id':i,'lec':p['lec'],'type':'rerev','target':r['target'],'request':r['request'] if not r['request'].startswith('（') else '','sel':p['sel'],
          'before':q(before),'after':{'text':r['problem_text'],'choices':r['choices'],'answer':r['answer'],'comment':r['comment'],'section':r['section']},
          'change':r['change'],'check':r.get('check',''),'acts':p['acts'],'commented':not r['request'].startswith('（')})
    elif p['main'] in ('削除','保留'):
        items.append({'id':i,'lec':p['lec'],'type':'del' if p['main']=='削除' else 'hold','sel':p['sel'],'request':p['note'],
          'before':q(it.get('easy')) ,'trial':q(it.get('rev')),'acts':p['acts']})
json.dump(items,open(B+'kokushi_rerev23/page/rerev23_data.json','w'),ensure_ascii=False)
for p in plan: print(p['id'],p['sel'],p['main'],' / '.join(p['acts']))
print(len(items))
