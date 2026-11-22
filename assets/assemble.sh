#!/bin/bash
# Assemble the make.fun TikTok ad.
# Pass 1: scenes (slow zoom + 0.4s crossfades) + brand badge + VO + music -> clip.mp4
# Pass 2: press-pack end-card recipe from https://make.fun/press/llms.txt
#         (transparent card over last 2.5s, referral code typed in) -> ad.mp4
set -e
cd "$(dirname "$0")/.."

# Scene durations (s): VO lengths are 2.81 / 5.23 / 6.24 / 4.22 + ~0.7s pad.
D1=3.5; D2=5.9; D3=6.9; D4=4.9
# xfade offsets (each fade 0.4s): total = 21.2 - 3*0.4 = 20.0s; card starts at 17.5s.
ffmpeg -y -v error \
  -framerate 30 -loop 1 -t $D1 -i assets/scene1.png \
  -framerate 30 -loop 1 -t $D2 -i assets/scene2.png \
  -framerate 30 -loop 1 -t $D3 -i assets/scene3.png \
  -framerate 30 -loop 1 -t $D4 -i assets/scene4.png \
  -i assets/makefun-badge-9x16.png \
  -i assets/vo1.mp3 -i assets/vo2.mp3 -i assets/vo3.mp3 -i assets/vo4.mp3 \
  -i assets/music.wav \
  -filter_complex "\
[0:v]zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[v0];\
[1:v]zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[v1];\
[2:v]zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[v2];\
[3:v]zoompan=z='1+0.0006*on':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps=30,format=yuv420p[v3];\
[v0][v1]xfade=transition=fade:duration=0.4:offset=3.1[x1];\
[x1][v2]xfade=transition=fade:duration=0.4:offset=8.6[x2];\
[x2][v3]xfade=transition=fade:duration=0.4:offset=15.1[x3];\
[x3][4:v]overlay=0:0:enable='lt(t,17.5)'[v];\
[5:a]adelay=350|350[vo1];[6:a]adelay=3500|3500[vo2];[7:a]adelay=9000|9000[vo3];[8:a]adelay=15600|15600[vo4];\
[9:a]atrim=0:20,volume=0.6,afade=t=out:st=19:d=1[mus];\
[vo1][vo2][vo3][vo4][mus]amix=inputs=5:duration=longest:dropout_transition=0[a]" \
  -map '[v]' -map '[a]' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 128k \
  -t 20 -movflags +faststart clip.mp4

# Pass 2: end card (numbers from manifest.json referral_card.fields 9:16).
CLIP=clip.mp4 CODE=jqdv7ndk FONT=assets/JetBrainsMono-Bold.ttf
W=1080 H=1920 CARD=assets/makefun-card-9x16-transparent.webm LEN=2.5 REST=1.433
CX=210 CY=1232 CW=5 CH=78 MID=1271 SIZE=62
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$CLIP")
T=$(awk "BEGIN{print $D-$LEN}")
ffmpeg -y -v error -i "$CLIP" -c:v libvpx-vp9 -i "$CARD" -filter_complex "\
[0:v]scale=$W:$H:force_original_aspect_ratio=increase,crop=$W:$H,setsar=1,fps=60,format=yuva420p,split[clip][soft];\
[soft]gblur=sigma=28,eq=saturation=0.35,fade=t=in:st=$T:d=0.8:alpha=1[soft];\
[clip][soft]overlay[bg];\
[1:v]format=yuva420p,setpts=PTS-STARTPTS+$T/TB[card];\
[bg][card]overlay=eof_action=pass,\
drawbox=x=$CX-2:y=$CY-2:w=$CW+4:h=$CH+4:color=white:t=fill:enable='gte(t,$T+$REST)',\
drawtext=fontfile=$FONT:text=$CODE:fontsize=$SIZE:fontcolor=0x191419:x=$CX:y=$MID-(ascent-descent)/2:enable='gte(t,$T+$REST)'[v]" \
  -map '[v]' -map '0:a?' -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac \
  -movflags +faststart ad.mp4

ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height,codec_name,r_frame_rate -of default=noprint_wrappers=1 ad.mp4
