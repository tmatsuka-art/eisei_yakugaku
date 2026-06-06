# -*- coding: utf-8 -*-
import json, re

cand = ['097024','097245','098025','098140','099138','099240','100025',
        '101138','101139','102025','102139','103025','103139','104134',
        '105139','106139','107140','108139','109024','109025','109139',
        '110025','110139','110140','111138']
cand = set(cand)
fig_re = re.compile(r'図|表|グラフ|下図|右図|左図')

with open('hygiene_with_images_v4.jsonl', encoding='utf-8') as f:
    for line in f:
        o = json.loads(line)
        pid = o.get('problem_id')
        if pid not in cand:
            continue
        q = o.get('problem_text') or ''
        refs_fig = bool(fig_re.search(q))
        nimg = o.get('num_images', 0)
        nimg_det = o.get('num_images_detected', 0)
        assets = o.get('assets') or []
        ch = o.get('choices') or []
        empty_choices = (len(ch) == 0)
        warn = ''
        if refs_fig and not nimg and not assets:
            warn = '  <<< 図に言及するが画像なし＝要注意'
        if empty_choices:
            warn += '  <<< 選択肢が空＝回答ボタン出ない'
        print(f"{pid} | num_images={nimg} detected={nimg_det} | 図言及={refs_fig} | choices数={len(ch)} | assets={assets}{warn}")
