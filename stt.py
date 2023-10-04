import vosk
import sys
import sounddevice as sd
import queue
import json
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

model = vosk.Model(config['Audio']['model_in'])
samplerate = int(config['Audio']['samplerate'])
device = int(config['Audio']['audio_in'])

q = queue.Queue()

def q_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def va_listen(callback):
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device, dtype='int16',
                           channels=1, callback=q_callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                callback(json.loads(rec.Result())["text"])