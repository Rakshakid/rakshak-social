#!/bin/bash
# vid.sh slide <stem> <audio_src.mp4> <dur>   -> out/<stem>.mp4 (1080x1350, slow push-in, overlay fades in at 0.8s)
# vid.sh story <stem> <audio_src.mp4> <dur>   -> out/<stem>.mp4 (1080x1920, push-in, 3 text states)
set -e
cd "$(dirname "$0")/out"
kind=$1; s=$2; a=$3; d=$4
if [ "$kind" = slide ]; then W=1080; H=1350; else W=1080; H=1920; fi
FR=$(python3 -c "print(int($d*30))")
ZP="scale=$((W*2)):$((H*2)),zoompan=z='1+0.06*on/$FR':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$FR:s=${W}x${H}:fps=30"
if [ "$kind" = slide ]; then
  ffmpeg -loglevel error -y -loop 1 -i ${s}_bg.png -loop 1 -i ${s}_ov.png -i "$a" -filter_complex \
  "[0]$ZP[bg];[1]format=rgba,fade=in:st=0.8:d=0.6:alpha=1[ov];[bg][ov]overlay=0:0:shortest=1,format=yuv420p[v]" \
  -map "[v]" -map 2:a -t $d -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart $s.mp4
else
  ffmpeg -loglevel error -y -loop 1 -i ${s}_bg.png -loop 1 -i ${s}_base.png -loop 1 -i ${s}_s0.png -loop 1 -i ${s}_s1.png -loop 1 -i ${s}_s2.png -i "$a" -filter_complex \
  "[0]$ZP[bg];[1]format=rgba[b];\
[2]format=rgba,fade=in:st=0.4:d=0.5:alpha=1,fade=out:st=3.1:d=0.4:alpha=1[t0];\
[3]format=rgba,fade=in:st=3.5:d=0.5:alpha=1,fade=out:st=5.9:d=0.4:alpha=1[t1];\
[4]format=rgba,fade=in:st=6.3:d=0.5:alpha=1[t2];\
[bg][b]overlay=0:0[v0];[v0][t0]overlay=0:0[v1];[v1][t1]overlay=0:0[v2];[v2][t2]overlay=0:0,format=yuv420p[v]" \
  -map "[v]" -map 5:a -t $d -c:v libx264 -crf 20 -preset medium -c:a aac -b:a 192k -movflags +faststart $s.mp4
fi
echo done $s.mp4
