import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np
import imageio_ffmpeg
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

FFMPEG_BIN = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()

def procesar(video_path, post_id, output_dir, model=None):
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    audio_path = output_dir / f"{post_id}.wav"
    frames_dir = output_dir / f"{post_id}_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    raw_out = output_dir / f"{post_id}_raw_transcript.txt"

    # 1. Extraer audio en WAV 16kHz mono
    subprocess.run([
        FFMPEG_BIN, "-y", "-i", str(video_path),
        "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(audio_path)
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Extraer 1 fotograma cada 2 segundos
    subprocess.run([
        FFMPEG_BIN, "-y", "-i", str(video_path),
        "-vf", "fps=1/2", str(frames_dir / "frame_%03d.jpg")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Transcribir con Faster-Whisper vía numpy array (evita incompatibilidad PyAV)
    if model is None:
        model = WhisperModel("small", device="cpu", compute_type="int8")

    with wave.open(str(audio_path), "rb") as wf:
        audio_np = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

    segments, info = model.transcribe(audio_np, beam_size=5)
    
    lines = []
    for seg in segments:
        m1, s1 = divmod(int(seg.start), 60)
        m2, s2 = divmod(int(seg.end), 60)
        lines.append(f"[{m1:02d}:{s1:02d} - {m2:02d}:{s2:02d}] {seg.text.strip()}")

    raw_out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[{post_id}] Transcripción completada ({len(lines)} segmentos).")
    return lines

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python procesar_reel.py <video_path> <post_id> <output_dir>")
        sys.exit(1)
    procesar(sys.argv[1], sys.argv[2], sys.argv[3])
