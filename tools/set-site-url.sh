#!/bin/sh
# 公開URLを一括で書き換えます。何度でも実行できます。
#   使い方:  sh tools/set-site-url.sh https://yourname.github.io/repo/
set -e

if [ -z "$1" ]; then
  echo "使い方: sh tools/set-site-url.sh https://yourname.github.io/repo/"
  exit 1
fi

NEW="$1"
case "$NEW" in */) ;; *) NEW="$NEW/" ;; esac

OLD=$(sed -n 's/.*<link rel="canonical" href="\([^"]*\)".*/\1/p' index.html | head -1)
[ -z "$OLD" ] && OLD="https://USERNAME.github.io/REPO/"

if [ "$OLD" = "$NEW" ]; then
  echo "すでに $NEW が設定されています。"
  exit 0
fi

# template.html も一緒に書き換える（これを忘れると再ビルドで元に戻ります）
for f in index.html 404.html sitemap.xml robots.txt README.md tools/template.html; do
  if [ -f "$f" ]; then
    sed -i.bak "s#$OLD#$NEW#g" "$f"
    rm -f "$f.bak"
  fi
done

echo "公開URLを $OLD から $NEW に変更しました。"
