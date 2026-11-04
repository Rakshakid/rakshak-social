"""Turn carousel slides (1080x1350) into a 1080x1920 reel with one continuous martial track.
Slide sits at y=170..1520 (above Instagram's bottom-20% overlay zone) over a blurred, darkened copy of itself.
Each slide: slow push-in; 0.5 s crossfades; audio trimmed to length with a 1.5 s fade-out.
usage: carousel_reel.py out.mp4 audio durs_csv slide1.jpg slide2.jpg ...
"""
import sys, subprocess
out, audio, durs = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(',')]
slides = sys.argv[4:]; assert len(slides) == len(durs)
XF = 0.5; Y = 170
total = sum(durs) - XF * (len(durs) - 1)
inp, fc = [], []
for i, (s, d) in enumerate(zip(slides, durs)):
    inp += ['-loop', '1', '-framerate', '30', '-t', f'{d}', '-i', s]
    fr = int(d * 30)
    fc.append(f"[{i}]split[a{i}][b{i}];"
              f"[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=40:2,eq=brightness=-0.30[bg{i}];"
              f"[b{i}]scale=2160:2700,zoompan=z='1+0.04*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1350:fps=30[fg{i}];"
              f"[bg{i}][fg{i}]overlay=0:{Y},trim=duration={d},setpts=PTS-STARTPTS,format=yuv420p,setsar=1[v{i}]")
chain = "[v0]"; off = 0.0
for i in range(1, len(slides)):
    off += durs[i - 1] - XF
    fc.append(f"{chain}[v{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]")
    chain = f"[x{i}]"
n = len(slides)
fc.append(f"[{n}:a]atrim=0:{total:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.3,afade=t=out:st={total-1.5:.3f}:d=1.5,loudnorm=I=-14:TP=-1.5[aout]")
cmd = ['ffmpeg', '-loglevel', 'error', '-y'] + inp + ['-i', audio, '-filter_complex', ';'.join(fc),
       '-map', chain, '-map', '[aout]', '-t', f'{total:.3f}', '-r', '30', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium',
       '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-ar', '44100', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True)
print('wrote', out, round(total, 2), 's')
