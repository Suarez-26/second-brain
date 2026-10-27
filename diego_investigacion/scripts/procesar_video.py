import os
import shutil
import subprocess
import sys
import wave
import numpy as np

from faster_whisper import WhisperModel

try:
    import imageio_ffmpeg
    FFMPEG_BIN = shutil.which("ffmpeg") or imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_BIN = "ffmpeg"


def procesar(video_path: str, post_id: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.join(output_dir, f"{post_id}.wav")
    frames_dir = os.path.join(output_dir, f"{post_id}_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # 1. Extraer audio en WAV 16kHz mono para Whisper
    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            "-ac",
            "1",
            audio_path,
        ],
        check=True,
    )

    # 2. Extraer 1 fotograma cada 5 segundos para análisis visual de Claude
    subprocess.run(
        [
            FFMPEG_BIN,
            "-y",
            "-i",
            video_path,
            "-vf",
            "fps=1/5",
            os.path.join(frames_dir, "frame_%03d.jpg"),
        ],
        check=True,
    )

    # 3. Transcribir con Faster-Whisper
    model = WhisperModel("small", device="cpu", compute_type="int8")
    with wave.open(str(audio_path), "rb") as wf:
        audio_np = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segments, _ = model.transcribe(audio_np, language="es", beam_size=5)

    raw_out = os.path.join(output_dir, f"{post_id}_raw_transcript.txt")
    with open(raw_out, "w", encoding="utf-8") as f:
        for seg in segments:
            mins, secs = divmod(int(seg.start), 60)
            end_m, end_s = divmod(int(seg.end), 60)
            f.write(
                f"[{mins:02d}:{secs:02d} - {end_m:02d}:{end_s:02d}] {seg.text.strip()}\n"
            )

    print(
        f"OK: Transcripción guardada en {raw_out} y fotogramas extraídos en {frames_dir}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python procesar_video.py <video_path> <post_id> <output_dir>")
        sys.exit(1)
    procesar(sys.argv[1], sys.argv[2], sys.argv[3])
