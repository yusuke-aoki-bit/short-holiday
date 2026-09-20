# 短い休日

> **移転しました** → [https://heijitsu-bunko.pages.dev/works/mijikai-kyujitsu](https://heijitsu-bunko.pages.dev/works/mijikai-kyujitsu)
>
> この作品は「平日文庫」で公開しています。このリポジトリはアーカイブ済みで、GitHub Pages は移転先への転送ページになっています。公開当時の原本はコミット履歴に残っています。

---

# 短い休日 — A Short Holiday

中編小説『短い休日』の公開用リポジトリです。公開先: <https://yusuke-aoki-bit.github.io/short-holiday/>

本文・スタイル・スクリプト・ファビコンをすべて `index.html` 一枚に収めた自己完結構成で、外部への通信は一切発生しません（Webフォントも使っていません）。

- 本文：全10章＋エピローグ／約23,000字
- 縦組み・横組みの切り替えつき（選んだ組方はブラウザに記憶されます）
- 巻末に「設計図」（人物相関・一週間の構造・手紙の三角形・年表・伏線表・不穏さの設計）を、ネタバレ折りたたみで収録

> 長い一週間が過ぎ、短い休日が訪れる。
> その一週間の記憶が、彼にはない。

---

## 1. 公開

`main` ブランチの `/ (root)` を GitHub Pages で配信しています。push すれば数分で反映されます。

公開URLを変える（リポジトリ名の変更、独自ドメインへの移行など）ときは次を実行してください。

```sh
sh tools/set-site-url.sh https://example.com/新しいパス/
```

`index.html` の canonical から現在のURLを読み取り、`index.html`・`404.html`・`sitemap.xml`・`robots.txt`・`README.md`・`tools/template.html` をまとめて置換します。

---

## 2. ファイル構成

```
index.html            本文＋設計図（これ一枚で完結）
ogp.png               SNSカード用の画像（1200×630）
404.html              本文と同じデザインのエラーページ
robots.txt            全クロール許可＋sitemapの場所
sitemap.xml           1ページぶんのサイトマップ
.nojekyll             GitHub Pages の Jekyll 処理を無効化する
manuscript/
  mijikai_kyujitsu.md   本文の原稿（マークダウン）
  design_notes.md       設計書（主題・人物・時系列・伏線・不穏さの設計・検算記録）
tools/
  build_site.py       原稿 + テンプレート → index.html
  template.html       index.html の外枠（CSS・JS・設計図はここ）
  make_ogp.py         ogp.png を作り直す
  set-site-url.sh     公開URLを一括置換する
```

---

## 3. 本文を直したいとき

**`index.html` を直接いじらないでください。** 原稿を直してから作り直します。

```sh
# 1. 原稿を編集する
$EDITOR manuscript/mijikai_kyujitsu.md

# 2. index.html を作り直す
python3 tools/build_site.py
```

原稿の書式は次のとおりです。

| 書き方 | 出力 |
| --- | --- |
| `## 第一章　金曜日の夜` | 章見出し（章番号と章題。日付バッジは `build_site.py` の `WHEN` で指定） |
| 行頭が全角スペース1つ | 地の文（1字下げ） |
| 行頭が `「` や `『` | 会話文・付箋（字下げなし） |
| 行頭が全角スペース2つ | 手紙などの引用ブロック（連続する行が1ブロックになる） |
| `（了）` | 中央寄せの結び |

デザイン（配色・級数・組方）や設計図を変えたいときは `tools/template.html` を編集して、同じく `python3 tools/build_site.py` を実行してください。

OGP画像を作り直すときは Pillow と Noto Serif CJK が必要です。

```sh
pip install pillow
python3 tools/make_ogp.py
```

---

## 4. クレジット

本作は創作であり、登場する人物・団体・出来事はすべて架空のものです。作中の症状の描写は物語のためのもので、医学的な記述ではありません。

執筆にあたり Anthropic の AI「Claude」を使用しています。構成・加筆・最終的な判断は作者によるものです。

&copy; Yusuke
