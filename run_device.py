#!/usr/bin/env python3
# استدعاء المكتبات
import os
import queue # تنظيم قراءة الصوت لعدم ضياع البيانات
import sounddevice as sd # قراءة الصوت من الميكروفون
import vosk # تحويل الصوت إلى نص
import sys

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

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, dtype='int16', channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while True: # infinite loop
                # beginning
                data = q.get()
                if rec.AcceptWaveform(data):
                    sentence = rec.Result().split() # تم تحويل الصوت إلى نص
                    # sentence = [i.strip('"') for i in sentence] # تقسيم الجملة إلى كلمات
                    print(sentence)
                else:
                    sentence = rec.PartialResult().split() # تم تحويل الصوت إلى نص
                    # sentence = [i.strip('"') for i in sentence] # تقسيم الجملة إلى كلمات
                    print(sentence)
                # end of program

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
