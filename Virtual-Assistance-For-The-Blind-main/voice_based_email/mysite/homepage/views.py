
from django.shortcuts import render, redirect
from .models import Details
import imaplib
from gtts import gTTS
import os
from playsound import playsound
import speech_recognition as sr
import smtplib
from django.http import JsonResponse

file = "good"
i="0"
passwrd = ""
addr = ""
item =""
subject = ""
body = ""

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = 'C:/Users/srashti shukla/Desktop'

def texttospeech(text, filename):
    filename = filename + '.mp3'
    flag = True
    while flag:
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filename)
            flag = False
        except:
            print('Trying again')
    playsound(filename)
    os.remove(filename)
    return

def speechtotext(duration):
    global i, addr, passwrd
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        playsound('speak.mp3')
        audio = r.listen(source, phrase_time_limit=duration)
    try:
        response = r.recognize_google(audio)
    except:
        response = 'N'
    return response

def convert_special_char(text):
    temp=text
    special_chars = ['attherate','dot','underscore','dollar','hash','star','plus','minus','space','dash']
    for character in special_chars:
        while(True):
            pos=temp.find(character)
            if pos == -1:
                break
            else :
                if character == 'attherate':
                    temp=temp.replace('attherate','@')
                elif character == 'dot':
                    temp=temp.replace('dot','.')
                elif character == 'underscore':
                    temp=temp.replace('underscore','_')
                elif character == 'dollar':
                    temp=temp.replace('dollar','$')
                elif character == 'hash':
                    temp=temp.replace('hash','#')
                elif character == 'star':
                    temp=temp.replace('star','*')
                elif character == 'plus':
                    temp=temp.replace('plus','+')
                elif character == 'minus':
                    temp=temp.replace('minus','-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp=temp.replace('dash','-')
    return temp



def login_view(request):
    global i, addr, passwrd 

    if request.method == 'POST':
        text1 = "Welcome to our Voice Based Email. Login with your email account in order to continue. "
        texttospeech(text1, file + i)
        i = i + str(1)

        flag = True
        while (flag):
            texttospeech("Enter your Email", file + i)
            i = i + str(1)
            addr = speechtotext(10)
            
            if addr != 'N':
                texttospeech("You meant " + addr + " say done to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'done' or say == 'Done':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        addr = addr.strip()
        addr = addr.replace(' ', '')
        addr = addr.lower()
        addr = convert_special_char(addr)
        print(addr)
        # request.email = addr

        flag = True
        while (flag):
            texttospeech("Enter your password", file + i)
            i = i + str(1)
            passwrd = speechtotext(10)
            
            if passwrd != 'N':
                texttospeech("You meant " + passwrd + " say done to confirm or no to enter again", file + i)
                i = i + str(1)
                say = speechtotext(3)
                if say == 'done' or say == 'Done':
                    flag = False
            else:
                texttospeech("could not understand what you meant:", file + i)
                i = i + str(1)
        passwrd = passwrd.strip()
        passwrd = passwrd.replace(' ', '')
        passwrd = passwrd.lower()
        passwrd = convert_special_char(passwrd)
        print(passwrd)

        imap_url = 'imap.gmail.com'
        passwrd = 'srashtigaytri@gmail.com'
        addr = 'Srashti@33'
        conn = imaplib.IMAP4_SSL(imap_url)
        try:
            conn.login(addr, passwrd)
            s.login(addr, passwrd)
            texttospeech("Congratulations. You have logged in successfully. You will now be redirected to the menu page.", file + i)
            i = i + str(1)
            return JsonResponse({'result' : 'success'})
        except:
            texttospeech("Invalid Login Details. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
        
    detail  = Details()
    detail.email = addr
    detail.password = passwrd
    return render(request, 'homepage/login.html', {'detail' : detail}) 

def options_view(request):
    global i, addr, passwrd
    if request.method == 'POST':
        flag = True
        texttospeech("You are logged into your account. What would you like to do ?", file + i)
        i = i + str(1)
        while(flag):
            texttospeech("To compose an email say compose. To open Inbox folder say Inbox. To open Sent folder say Sent. To open Trash folder say Trash. To Logout say Logout. Do you want me to repeat?", file + i)
            i = i + str(1)
            say = speechtotext(3)
            if say == 'No' or say == 'no':
                flag = False
        texttospeech("Enter your desired action", file + i)
        i = i + str(1)
        act = speechtotext(5)
        act = act.lower()
        if act == 'compose':
            return JsonResponse({'result' : 'compose'})
        elif act == 'inbox':
            return JsonResponse({'result' : 'inbox'})
        elif act == 'sent':
            return JsonResponse({'result' : 'sent'})
        elif act == 'trash':
            return JsonResponse({'result' : 'trash'})
        elif act == 'log out':
            addr = ""
            passwrd = ""
            texttospeech("You have been logged out of your account and now will be redirected back to the login page.",file + i)
            i = i + str(1)
            return JsonResponse({'result': 'logout'})
        else:
            texttospeech("Invalid action. Please try again.", file + i)
            i = i + str(1)
            return JsonResponse({'result': 'failure'})
    elif request.method == 'GET':
        return render(request, 'homepage/options.html')

