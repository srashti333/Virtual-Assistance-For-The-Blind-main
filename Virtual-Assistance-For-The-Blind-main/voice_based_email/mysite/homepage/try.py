from winsound import PlaySound
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, duration=1)
    PlaySound('speak.mp3')
    audio = r.listen(source, phrase_time_limit=20)
    PlaySound(audio)