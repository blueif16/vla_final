#!/usr/bin/env bash
# Chapter 5 web page: download the paper figures we may reuse and convert them for docs/assets/img/ch5/.
# Every source is CC BY 4.0 on its arXiv abstract page (checked 2026-11-13): LIBERO-CF 2602.17659 (v3),
# LIBERO-PRO 2510.03827 (v2), Haon et al. 2509.00328 (v1). The other three chapter 5 papers (LIBERO-Plus, LangGap,
# Grant et al.) carry arXiv's default licence, so none of their figures are copied.
# Needs curl, ffmpeg and google-chrome (only to render LIBERO-CF's Figure 4, which arXiv serves as an SVG).
# Run from the repo root: bash tools/ch5/fetch_figures.sh
set -euo pipefail
OUT=docs/assets/img/ch5
mkdir -p "$OUT"
TMP=$(mktemp -d)          # downloads stay in their own empty folder
trap 'rm -rf "$TMP"' EXIT
UA="Mozilla/5.0 (course learning-site builder)"
get() { curl -sfL -A "$UA" "$1" -o "$TMP/$2"; }
# JPG at most 1600 px wide, metadata stripped, quality 3 (the teaching-web skill's rule)
jpg() { ffmpeg -loglevel error -y -i "$TMP/$1" -map_metadata -1 -vf "scale='min(1600,iw)':-2${3:+,$3}" -q:v 3 "$OUT/$2"; }

CF=https://arxiv.org/html/2602.17659v3
get "$CF/visionshortcut-v7.png" cf-fig2.png
get "$CF/method-v6.png" cf-fig3.png
get "$CF/guidance_scale-v3.svg" cf-fig4.svg
get "$CF/real-fig-row-1-v3.png" cf-fig5-row1.png
jpg cf-fig2.png libero-cf-fig2-vision-shortcuts.jpg
jpg cf-fig3.png libero-cf-fig3-cag.jpg
# Figure 5, first row: crop its first scene (Coke / Sprite / Fanta), the paper's pixels unchanged otherwise
ffmpeg -loglevel error -y -i "$TMP/cf-fig5-row1.png" -map_metadata -1 -vf "crop=980:376:90:0" -q:v 3 "$OUT/libero-cf-fig5-cans.jpg"
# Figure 4 is vector: render it on white at 1600 px in headless Chrome, then convert
printf '<html><body style="margin:0;background:#fff"><img src="cf-fig4.svg" style="width:1600px;display:block"></body></html>' > "$TMP/fig4.html"
google-chrome --headless=new --disable-gpu --no-sandbox --user-data-dir="$TMP/chrome" --allow-file-access-from-files \
  --window-size=1600,618 --screenshot="$TMP/cf-fig4.png" "file://$TMP/fig4.html" >/dev/null 2>&1
jpg cf-fig4.png libero-cf-fig4-guidance-scale.jpg

PRO=https://arxiv.org/html/2510.03827v2
get "$PRO/language_ood_1.png" pro-fig3a.png
get "$PRO/language_ood_3.png" pro-fig3b.png
jpg pro-fig3a.png libero-pro-fig3a-original.jpg
jpg pro-fig3b.png libero-pro-fig3b-messy.jpg

ST=https://arxiv.org/html/2509.00328v1
get "$ST/Graphic_DOWN_UPSIZED.png" steer-fig1.png
jpg steer-fig1.png haon-fig1-steering.jpg

ls -la "$OUT"
