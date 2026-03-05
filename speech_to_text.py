import sounddevice as sd
import vosk
import queue
import sys
import json
import threading

MODEL_PATH = "C:/Users/acer/OneDrive/Desktop/Project/vosk-model-en-in-0.5"  # put your path
model = vosk.Model(MODEL_PATH)

q = queue.Queue()
stop_listening_flag = threading.Event()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def record_voice(prompt="🎙 I'm listening, sir..."):
    """
    Blocking call, returns the first recognized sentence.
    """
    print(prompt)
    rec = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        while not stop_listening_flag.is_set():
            try:
                data = q.get(timeout=0.1)
            except queue.Empty:
                continue
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text.strip():
                    print("👤 You:", text)
                    return text
    return ""
