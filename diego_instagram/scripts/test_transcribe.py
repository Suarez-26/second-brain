import os
import shutil
import subprocess
import sys
from pathlib import Path
import imageio_ffmpeg
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

FFMPEG_BIN = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()

def test_transcribe(video_path, post_id, out_dir):
    out_dir = Path(out_dir)
    audio_path = out_dir / f"{post_id}.wav"
    frames_dir = out_dir / f"{post_id}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)

    print("1. Extrayendo audio con ffmpeg...")
    subprocess.run([
        FFMPEG_BIN, "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(audio_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("2. Extrayendo fotogramas dinámicos (1 cada 2 seg)...")
    subprocess.run([
        FFMPEG_BIN, "-y", "-i", str(video_path),
        "-vf", "fps=1/2", str(frames_dir / "frame_%03d.jpg")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("3. Transcribiendo con Faster-Whisper (small, int8)...")
    model = WhisperModel("small", device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio_path), language="es", beam_size=5)

    trans_file = out_dir / f"{post_id}_raw_transcript.txt"
    lines = []
    for s in segments:
        m1, s1 = divmod(int(s.start), 60)
        m2, s2 = divmod(int(s.end), 60)
        lines.append(f"[{m1:02d}:{s1:02d} - {m2:02d}:{s2:02d}] {s.text.strip()}")
    
    trans_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"Transcripción guardada en {trans_file}")
    for l in lines[:5]:
        print(" ", l)

if __name__ == "__main__":
    test_transcribe("diego_instagram/04_reels_y_videos/test_reel.mp4", "test_reel", "diego_instagram/04_reels_y_videos")
