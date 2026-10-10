"""Background music for animated-text reels (replaces the plain sine drone).

Warm piano-like arpeggio over a soft string pad, D major, I-V-vi-IV-I,
one chord per reel scene (scene change every 2.8 s). Fully synthesised, royalty free.

Usage: python3 reel_music.py out.wav [duration_seconds]
Mux:   ffmpeg -i reel.mp4 -i out.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest new.mp4
"""
import sys, wave
import numpy as np

SR = 44100
def hz(midi): return 440.0 * 2 ** ((midi - 69) / 12)

# D, A, Bm, G, D  (midi roots in octave 3/4)
CHORDS = [[50, 54, 57, 62], [45, 52, 57, 61], [47, 54, 59, 62], [43, 50, 55, 59], [50, 54, 57, 62]]

def pluck(f, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    env = np.exp(-t * 2.6) * (1 - np.exp(-t * 300))
    tone = sum((0.55 ** k) * np.sin(2 * np.pi * f * (k + 1) * t) for k in range(5))
    return amp * env * tone

def pad(freqs, dur, amp):
    t = np.arange(int(dur * SR)) / SR
    att = np.minimum(1, t / 0.9); rel = np.minimum(1, (dur - t) / 0.9)
    x = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5 * t)) + 0.5 * np.sin(2 * np.pi * f * 1.003 * t) for f in freqs)
    return amp * att * rel * x / len(freqs)

def reverb(x):
    out = x.copy()
    for d, g in [(0.031, .35), (0.047, .3), (0.071, .25), (0.113, .2), (0.167, .15), (0.241, .1)]:
        n = int(d * SR); out[n:] += g * x[:-n]
    return out

def make(duration=14.6, step=2.8):
    n = int((duration + 3) * SR); mix = np.zeros(n)
    beat = step / 8  # eight arpeggio notes per chord
    for ci, ch in enumerate(CHORDS):
        start = ci * step
        if start >= duration: break
        seg = min(step + 0.9, duration - start + 0.9)
        p = pad([hz(m - 12) for m in ch[:2]] + [hz(m) for m in ch[1:]], seg, 0.11)
        i = int(start * SR); mix[i:i + len(p)] += p[: n - i]
        pattern = [0, 1, 2, 3, 2, 1, 2, 3] if ci < len(CHORDS) - 1 else [0, 1, 2, 3]
        for k, idx in enumerate(pattern):
            ts = start + k * beat
            if ts >= duration - 0.3: break
            note = ch[idx] + 12
            pl = pluck(hz(note), 2.2, 0.16 if k == 0 else 0.11)
            j = int(ts * SR); mix[j:j + len(pl)] += pl[: n - j]
    mix = reverb(mix)[: int(duration * SR)]
    t = np.arange(len(mix)) / SR
    mix *= np.minimum(1, t / 1.0) * np.minimum(1, (duration - t) / 2.0)
    mix = mix / np.max(np.abs(mix)) * 0.5  # about -6 dBFS peak, sits under silence-friendly viewing
    return (mix * 32767).astype(np.int16)

if __name__ == "__main__":
    out = sys.argv[1]; dur = float(sys.argv[2]) if len(sys.argv) > 2 else 14.6
    a = make(dur)
    st = np.repeat(a[:, None], 2, axis=1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
    print("wrote", out, dur, "s")
