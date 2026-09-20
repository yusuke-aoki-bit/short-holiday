# -*- coding: utf-8 -*-
"""原稿（manuscript/mijikai_kyujitsu.md）+ テンプレート（tools/template.html）→ index.html"""
import html, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'manuscript', 'mijikai_kyujitsu.md')
TPL = os.path.join(ROOT, 'tools', 'template.html')
OUT = os.path.join(ROOT, 'index.html')

# 章ごとの日付バッジ。第二要素が 'y' の章は夜色（木曜の深夜が絡む章）
WHEN = {
    '第一章': ('1月16日 金', ''),
    '第二章': ('1月19日 月', ''),
    '第三章': ('1月20日 – 2月13日', ''),
    '第四章': ('2月7日 土', ''),
    '第五章': ('2月7日 – 2月13日', 'y'),
    '第六章': ('2月14日 土・午前', ''),
    '第七章': ('2月14日 土・午後', ''),
    '第八章': ('2月14日 土・夜', 'y'),
    '第九章': ('2月16日 – 3月6日', 'y'),
    '第十章': ('3月14日 土', ''),
    'エピローグ': ('4月4日 土', ''),
}

def esc(s):
    return html.escape(s, quote=False)

def parse(lines):
    chapters, cur = [], None
    for ln in lines:
        if ln.startswith('## '):
            parts = ln[3:].strip().split('　')
            cur = {'num': parts[0], 'name': '　'.join(parts[1:]), 'lines': []}
            chapters.append(cur)
        elif cur is not None:
            cur['lines'].append(ln)
    return chapters

def render(lines):
    out, buf = [], []
    def flush():
        if buf:
            cls = 'note letter' if buf[0].startswith(('『', 'とおるくんへ')) else 'note'
            out.append('    <div class="%s">%s</div>' % (cls, esc('\n'.join(buf))))
            del buf[:]
    for ln in lines:
        s = ln.rstrip()
        if s in ('', '---'):
            continue
        if s.startswith('　　'):          # 全角スペース2つ＝手紙・メモの引用ブロック
            buf.append(s[2:])
            continue
        flush()
        t = s[1:] if s.startswith('　') else s
        if t == '（了）':
            out.append('    <p class="end">（了）</p>')
        elif t[:1] in ('「', '『'):
            out.append('    <p class="ni">%s</p>' % esc(t))
        else:
            out.append('    <p>%s</p>' % esc(t))
    flush()
    return '\n'.join(out)

def main():
    chapters = parse(io.open(SRC, encoding='utf-8').read().split('\n'))
    toc, secs = [], []
    for i, c in enumerate(chapters, 1):
        cid = 'ch%02d' % i
        when, kind = WHEN.get(c['num'], ('', ''))
        wcls = 'when when-y' if kind == 'y' else 'when'
        toc.append('<li><a href="#%s"><span class="t-n">%s</span><span class="t-t">%s</span><span class="%s">%s</span></a></li>'
                   % (cid, esc(c['num']), esc(c['name']), wcls, esc(when)))
        hint = '\n  <p class="hint" aria-hidden="true">縦組みでは、本文は左へスクロールします</p>' if i == 1 else ''
        secs.append(
            '<section class="chapter" id="%s">\n'
            '  <h2 class="ch-head"><span class="ch-num">%s</span><span class="ch-name">%s</span><span class="%s">%s</span></h2>\n'
            '  <div class="ch-body" tabindex="0" role="region" aria-label="%s 本文">\n%s\n  </div>%s\n</section>'
            % (cid, esc(c['num']), esc(c['name']), wcls, esc(when), esc(c['num']), render(c['lines']), hint))
    body = ('\n<nav class="toc col" aria-label="目次">\n  <h2>目次</h2>\n  <ol>\n' + '\n'.join(toc) +
            '\n  </ol>\n</nav>\n\n<main class="honbun shell" id="honbun">\n' + '\n\n'.join(secs) + '\n</main>\n')
    tpl = io.open(TPL, encoding='utf-8').read()
    assert '<!-- BODY -->' in tpl
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(tpl.replace('<!-- BODY -->', body))
    print('index.html:', len(chapters), 'chapters')

if __name__ == '__main__':
    main()
