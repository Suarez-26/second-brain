import os
import shutil
import subprocess
import sys
import wave
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)

try:
    import imageio_ffmpeg
    FFMPEG_BIN = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_BIN = "ffmpeg"

BASE_DIR = Path(__file__).resolve().parent.parent
VID_DIR = BASE_DIR / "04_videos_y_audios"


def main():
    mp4_files = sorted(VID_DIR.glob("*.mp4"))
    print(f"Encontrados {len(mp4_files)} videos para procesar con Faster-Whisper...")
    if not mp4_files:
        return

    print("Cargando modelo Faster-Whisper ('small', int8)...")
    model = WhisperModel("small", device="cpu", compute_type="int8")

    for video_path in mp4_files:
        post_id = video_path.stem
        raw_out = VID_DIR / f"{post_id}_raw_transcript.txt"
        if raw_out.exists() and raw_out.stat().st_size > 10:
            print(f"Omitiendo {video_path.name} (ya transcrito en {raw_out.name})")
            continue
        audio_path = VID_DIR / f"{post_id}.wav"
        frames_dir = VID_DIR / f"{post_id}_frames"
        frames_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n=== Procesando {video_path.name} ===")
        # 1. Extraer audio en WAV 16kHz mono
        subprocess.run(
            [
                FFMPEG_BIN,
                "-y",
                "-i",
                str(video_path),
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "16000",
                "-ac",
                "1",
                str(audio_path),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 2. Extraer 1 fotograma cada 5 segundos
        subprocess.run(
            [
                FFMPEG_BIN,
                "-y",
                "-i",
                str(video_path),
                "-vf",
                "fps=1/5",
                str(frames_dir / "frame_%03d.jpg"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 3. Transcribir con Faster-Whisper pasando numpy float32 array directamente (evita incompatibilidad de PyAV 19)
        with wave.open(str(audio_path), "rb") as wf:
            audio_np = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
        segments, info = model.transcribe(audio_np, beam_size=5)
        print(f"Idioma detectado ({post_id}): {info.language} (prob: {info.language_probability:.2f})")

        with open(raw_out, "w", encoding="utf-8") as f:
            for seg in segments:
                mins, secs = divmod(int(seg.start), 60)
                end_m, end_s = divmod(int(seg.end), 60)
                line = f"[{mins:02d}:{secs:02d} - {end_m:02d}:{end_s:02d}] {seg.text.strip()}"
                f.write(line + "\n")
                print("  ", line)

        print(f"OK: {raw_out.name} guardado.")

    print("\n¡Todos los videos han sido procesados y transcritos!")


if __name__ == "__main__":
    main()
