#!/usr/bin/env python3
# استدعاء المكتبات
import os
import queue # تنظيم قراءة الصوت لعدم ضياع البيانات
import sounddevice as sd # قراءة الصوت من الميكروفون
import vosk # تحويل الصوت إلى نص
import sys
import keyboard
import json

#from smbus import SMBus # ارسال واستقبال البيانات عن طريق البروتوكول I2C
 
addr = 0x8 # bus address for Arduino
#bus = SMBus(1) # تعريف مكتبة SMBUS

# تعريف مكتبة queue
q = queue.Queue()

# تعريف ال functions
def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    samplerate = 48000
    model = vosk.Model("model")
    results = []

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            rec.SetWords(True)

            while True:
                if keyboard.is_pressed('space'):
                    print('Start talking...')
                    break
            while keyboard.is_pressed('space'): # infinite loop
                # beginning
                data = q.get()
                if rec.AcceptWaveform(data):
                    sentence = rec.Result() # تم تحويل الصوت إلى نص
                    sentence = json.loads(sentence)
                    results.append(sentence.get("text", ""))
                else:
                    sentence = rec.PartialResult() # تم تحويل الصوت إلى نص
                # end of program
            results = " ".join(results)
            print(results)
            speech_file = open("speech.txt", "w")
            speech_file.write(results)
            speech_file.close()

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
