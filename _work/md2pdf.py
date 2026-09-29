# -*- coding: utf-8 -*-
"""運用マニュアル_教員用.md を、印刷向けCSS付きHTMLに変換する。
   その後 Chrome --headless --print-to-pdf でPDF化する（PDF化はシェル側）。"""
import markdown, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
md_path = ROOT / "_work" / "運用マニュアル_教員用.md"
out_html = ROOT / "_work" / "運用マニュアル_教員用.html"

body = markdown.markdown(
    md_path.read_text(encoding="utf-8"),
    extensions=["tables", "fenced_code", "attr_list", "sane_lists"],
)

CSS = """
@page { size: A4; margin: 16mm 15mm; }
* { box-sizing: border-box; }
body { font-family: "Yu Gothic","Meiryo","Hiragino Kaku Gothic ProN",sans-serif;
  font-size: 10pt; line-height: 1.72; color: #1a2035; margin: 0;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
h1 { font-size: 21pt; color: #5C2787; margin: 0 0 6px; padding-bottom: 10px;
  border-bottom: 3px solid #3aaab2; line-height: 1.3; }
h2 { font-size: 14pt; color: #fff;
  background: linear-gradient(90deg,#5C2787 0%,#3aaab2 100%);
  padding: 7px 13px; border-radius: 6px; margin: 26px 0 12px; break-after: avoid; }
h3 { font-size: 12pt; color: #2c8c93; margin: 18px 0 7px;
  border-left: 4px solid #7dc5b6; padding-left: 9px; break-after: avoid; }
p { margin: 0 0 8px; }
a { color: #2c8c93; text-decoration: none; }
strong { color: #5C2787; }
ul, ol { margin: 6px 0 10px; padding-left: 1.4em; }
li { margin-bottom: 4px; }
table { border-collapse: collapse; width: 100%; margin: 10px 0 14px;
  font-size: 9.2pt; break-inside: avoid; }
th { background: #e6f5f6; color: #5C2787; font-weight: 700;
  border: 1px solid #b8dde0; padding: 6px 9px; text-align: left; }
td { border: 1px solid #dde3ee; padding: 6px 9px; vertical-align: top; }
tr:nth-child(even) td { background: #f8fbfc; }
code { background: #f1eef7; color: #5b1f8c; padding: 1px 5px; border-radius: 4px;
  font-family: "Consolas","Courier New",monospace; font-size: 9pt; }
pre { background: #f6f8fc; border: 1px solid #dde3ee; border-left: 4px solid #3aaab2;
  border-radius: 6px; padding: 12px 14px; overflow-x: auto; break-inside: avoid;
  font-size: 9pt; line-height: 1.6; }
pre code { background: none; color: #1a2035; padding: 0;
  font-family: "BIZ UDGothic","MS Gothic","Consolas",monospace; }
blockquote { background: #fff7ec; border: 1px solid #f0c27a; border-left: 4px solid #e0a94e;
  border-radius: 6px; margin: 12px 0; padding: 9px 14px; color: #6a4f22;
  break-inside: avoid; font-size: 9.6pt; }
blockquote p { margin: 0 0 5px; }
blockquote p:last-child { margin-bottom: 0; }
blockquote strong { color: #9a6212; }
hr { border: none; border-top: 1px solid #e3e8f0; margin: 16px 0; }
/* 目次（最初のol） */
body > ol:first-of-type { background: #f8fbfc; border: 1px solid #dde3ee;
  border-radius: 8px; padding: 12px 14px 12px 34px; }
"""

html = (
    '<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">'
    "<title>衛生薬学 運用マニュアル（教員用）</title>"
    f"<style>{CSS}</style></head><body>{body}</body></html>"
)
out_html.write_text(html, encoding="utf-8")
print("HTML written:", out_html, f"({len(html):,} bytes)")
