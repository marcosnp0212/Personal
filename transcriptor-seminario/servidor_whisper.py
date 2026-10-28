"""Servidor local de transcripción (Whisper en la tarjeta NVIDIA) para transcriptor.html.

Arranca con arrancar.bat y abre http://127.0.0.1:8000 en Edge.
"""
import glob
import io
import wave
import os
import site
import subprocess
import sys
import threading

# En Windows, las librerías de NVIDIA instaladas con pip deben añadirse a mano a la ruta de DLL.
if os.name == "nt":
    for sp in site.getsitepackages():
        for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ["PATH"]

import numpy as np
import uvicorn
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from faster_whisper import WhisperModel

MODEL_NAME = os.environ.get("WHISPER_MODEL", "large-v3-turbo")
DEVICE = os.environ.get("WHISPER_DEVICE", "cuda")
HERE = os.path.dirname(os.path.abspath(__file__))
LANG_NAMES = {"es": "spanish", "gl": "galician", "pt": "portuguese", "en": "english", "ca": "catalan"}

print(f"Cargando Whisper {MODEL_NAME} en {DEVICE.upper()}... (la primera vez descarga ~1,6 GB)", flush=True)
if DEVICE == "cuda":
    model = WhisperModel(MODEL_NAME, device="cuda", compute_type="int8_float16")
else:
    model = WhisperModel(MODEL_NAME, device="cpu", compute_type="int8", cpu_threads=os.cpu_count() or 4)
# Prueba de arranque: si falta algo de NVIDIA, falla aquí y no en mitad de la ponencia.
list(model.transcribe(np.zeros(16000, dtype=np.float32), language="es")[0])
print("Whisper listo.", flush=True)

lock = threading.Lock()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "transcriptor.html"))


@app.get("/v1/models")
def models():
    return {"data": [{"id": MODEL_NAME, "device": DEVICE}]}


@app.post("/v1/audio/transcriptions")
def transcriptions(
    file: UploadFile = File(...),
    language: str = Form(None),
    prompt: str = Form(None),
    model_name: str = Form(None, alias="model"),
    response_format: str = Form("json"),
    temperature: str = Form("0"),
):
    # El WAV llega ya a 16 kHz mono: se lee sin PyAV (algunas versiones de av rompen decode_audio).
    audio = np.frombuffer(wave.open(io.BytesIO(file.file.read())).readframes(10**9), dtype=np.int16).astype(np.float32) / 32768.0
    with lock:
        segments, info = model.transcribe(
            audio,
            language=language or None,
            initial_prompt=prompt or None,
            beam_size=5,
            temperature=0,
            vad_filter=True,
            condition_on_previous_text=False,
        )
        segs = list(segments)
    return {
        "text": " ".join(s.text.strip() for s in segs),
        "language": LANG_NAMES.get(info.language, info.language),
        "segments": [
            {"text": s.text, "no_speech_prob": s.no_speech_prob, "avg_logprob": s.avg_logprob,
             "compression_ratio": s.compression_ratio}
            for s in segs
        ],
    }


if __name__ == "__main__":
    url = "http://127.0.0.1:8000"
    print(f"\nAbre {url} en Edge (se intenta abrir solo). NO cierres esta ventana durante el seminario.\n", flush=True)
    if os.name == "nt":
        threading.Timer(2, lambda: subprocess.Popen(["cmd", "/c", "start", "msedge", url])).start()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
