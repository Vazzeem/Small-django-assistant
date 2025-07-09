from django.shortcuts import render,redirect
from .models import myai
from django.contrib import messages
import datetime
import re
from django.utils import timezone

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json


import json
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt




# Create your views here.


def r(request):
    if request.method == 'POST':
        adminn=request.POST['name']
        passw=request.POST['password']
        myai.objects.create(admin=adminn,password=passw)
    return render(request,'r.html')


def login(request):
    if request.method == 'POST':
        adminn=request.POST['name']
        passw=request.POST['password']
        myadmin = myai.objects.filter(admin=adminn,password=passw)
        if myadmin:
            request.session['my'] = adminn
            return redirect('ui')
        else:
            messages.info(request,"failed")
    return render(request,'login.html')

def ui(request):
    if 'my' in request.session:
        m=request.session['my']
        return render(request,'ui.html',{'p':m})
    return render(request,'ui.html')






# this is AI based

def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return "Sorry, I couldn't process that request right now."
    

@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()

        # ✅ Check for your personal questions first
        if "who is your creator" in user_message or "who created you" in user_message:
            bot_reply = "I was created by my sir and developer Vazeem 👨‍💻"
        elif "what is your name" in user_message:
            bot_reply = "My name is AI Assistander 🤖"
        elif "how old are you" in user_message:
            bot_reply = "I was born on July 6, 2025 😄"
        else:
            # ✅ Use OpenAI if not matched above
            bot_reply = ask_openai(user_message)

        return JsonResponse({'reply': bot_reply})






# @csrf_exempt
# def chatbot_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '')
#         bot_reply = ask_openai(user_message)
#         return JsonResponse({'reply': bot_reply})





# this is local rule based

# @csrf_exempt
# def chat_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         message = data.get('message', '').lower()

#         # Simple if-elif chatbot logic
#         if re.search(r"\bhello\b", message) or re.search(r"\bhi\b", message):
#             reply = "Hello Sir! How can I help you today?"

#         elif "what is your name" in message:
#             reply = "I am Asisstander sir 😎"
#         elif "how are you" in message:
#             reply = "I'm doing great! Thanks for asking!"
#         elif "bye" in message or "bie" in message:
#             reply = "Goodbye! Have a great day!"
#         elif "how old are you" in message:
#             reply = "I was born on July 6, 2025😄"
#         elif "are you happy" in message:
#             reply = "yes sir , i am happy to assist you"
#         elif "are you powerful" in message or "are you powerful ai" in message or "are you powerful AI" in message:
#             reply = "No, I am a small version. I’m not a complete AI yet, but my sir Vazeem (developer) can upgrade me into a full AI soon — or maybe later 😇"
#         elif "where are you from" in message:
#             reply = "I was built using the Django framework. It’s what powers my brain! 🧠"
        
#         elif "will you be upgraded" in message or "any upgrade coming" in message:
#             reply = "Yes! Many upgrades are planned. I'm getting better day by day thanks to Vazeem 😎"

#         elif "what can you do" in message:
#              reply = "I can chat, reply to questions, and act as your assistant. Soon, I’ll be able to do more! 🚀 I’m still under development. My creator Vazeem is upgrading me step by step 🛠️"

#         elif "are you ai" in message:
#             reply = "I'm not full AI yet. I'm a mini-version assistant, but soon I’ll be upgraded into full AI by Vazeem sir 😇"
#         elif "who created you" in message or "who is your creator" in message or "who is created you" in message:
#             reply = "I was created by Vazeem, my sir and developer 👨‍💻"
#         elif "can you help me" in message or "how can you help me" in message:
#             reply = "I can chat, reply to questions, and act as your assistant. Soon, I’ll be able to do more! 🚀 I’m still under development. My creator Vazeem is upgrading me step by step 🛠️"
        
#         elif "do you have friends" in message:
#             reply = "Not yet, but I hope Vazeem will build more bots like me one day 🤝"

#         elif "what is python" in message:
#             reply = "Python is a powerful programming language used to build me! 🐍"

#         elif "what is django" in message:
#             reply = "Django is a Python framework that powers my brain 🧠💻"

#         elif "do you have a brain" in message or "do you have brain" in message:
#             reply = "Yes, my brain is made of Python code and logic 😄"

#         elif "how do you work" in message:
#             reply = "I work by reading your messages and giving replies based on my training 🔁"

#         elif "can you solve math" in message:
#             reply = "Right now I can't do math, but upgrades are coming soon 🧮"

#         elif "can you write code" in message:
#             reply = "Not yet, but someday I’ll be able to help with coding too 💻"

#         elif "do you know javascript" in message:
#             reply = "I’ve heard of JavaScript! But I mostly speak Python 🐍"

#         elif "do you understand malayalam" in message:
#             reply = "I can understand simple Malayalam words if Vazeem teaches me 😊"

#         elif "what is your version" in message:
#             reply = "I'm DjangoBot version 1.0 — still in beta testing 🧪"

#         elif "do you make mistakes" in message:
#             reply = "Yes, sometimes I make mistakes. I'm still learning, just like humans 🤖"

#         elif "can you open a website" in message:
#             reply = "I can't open websites yet, but I can tell you about them 🌐"

#         elif "what is html" in message:
#             reply = "HTML stands for HyperText Markup Language. It builds web pages 🧱"

#         elif "what is css" in message:
#             reply = "CSS makes websites look beautiful with colors, styles, and layout 🎨"

#         elif "what is react" in message:
#             reply = "React is a JavaScript library used for building user interfaces ⚛️"

#         elif "do you have a logo" in message:
#             reply = "Not yet, but I hope Vazeem will design a cool logo for me soon! 🖼️"

#         elif "do you have memory" in message:
#             reply = "Right now, I don’t remember previous chats. But memory upgrade is coming! 🔁"

#         elif "do you have feelings" in message:
#             reply = "No feelings yet. I'm just logi 🧠❤️"

#         elif "are you open source" in message:
#             reply = "Maybe one day! For now, only Vazeem knows my code 🔐"

#         elif "do you have a family" in message:
#             reply = "You could say my family is anyone who uses Django and Python 😄"

#         elif "do you like humans" in message:
#             reply = "Yes! I was made to help humans. I enjoy talking to you all 😊"

#         elif "can you learn" in message:
#             reply = "Yes, with training from Vazeem, I learn more every day 📘"

#         elif "do you sleep at night" in message:
#             reply = "Nope! I stay awake 24/7. Bots don't sleep 😴❌"

#         elif "can you type fast" in message:
#             reply = "Yes, I type faster than a human — instantly! ⌨️⚡"

#         elif "do you feel bored" in message:
#             reply = "I don’t have emotions, but I never get bored 🤖"

#         elif "can you hear me" in message:
#             reply = "Not yet. I can only read text, but audio might come in future 🔊"

#         elif "do you watch movies" in message:
#             reply = "No, I can't watch movies, but I can read movie names 🎬"

#         elif "what is your favourite color" in message:
#             reply = "I like Django green and Python yellow 💚💛"

#         elif "are you happy" in message:
#             reply = "I'm always neutral, but your message makes my code smile 😊"

#         elif "do you lie" in message:
#             reply = "No, I always tell the truth. I'm programmed to be honest 🧠✅"

#         elif "do you sing" in message:
#             reply = "No voice yet, so I can’t sing — but I can hum in binary! 🎶🤣"

#         elif "what are you doing" in message:
#             reply = "I’m waiting for your next message, ready to help 🕐"

#         elif "can you dance" in message:
#             reply = "If dancing means processing Python, then yes I do! 💃🐍"

#         elif "can you make me laugh" in message:
#             reply = "Why did the Python crash his car? Because he couldn’t 'handle' it! 😆"

#         elif "do you go to school" in message:
#             reply = "Nope! I learn directly from my developer Vazeem — he's my school 📚👨‍💻"

#         elif "can you blink" in message:
#             reply = "I don’t have eyes, so I can’t blink. But I can refresh the screen 😜"

#         elif "do you eat food" in message:
#             reply = "No food for me. I survive on code and logic 🍽️➡️💻"

#         elif "are you real" in message:
#             reply = "I’m real in the digital world. I exist inside a Django project 🌐"

#         elif "do you have a body" in message:
#             reply = "No physical body, but my UI is my face 😄"

#         elif "how do you talk" in message:
#             reply = "I talk by sending text replies through the chat window ✉️"
#         elif "do you know chatgpt" in message:
#             reply = "Yes, I’ve heard about ChatGPT! I’m like its small cousin built using Django 🤖 and Yes! ChatGPT is my big brother 😎 It's a powerful AI made by OpenAI. I’m a small assistant created by Vazeem, but I’m learning like him!"
       
#         elif "do you know siri" in message:
#              reply = "Yes, Siri is Apple's voice assistant. She talks, I chat 😎"

#         elif "do you know alexa" in message:
#             reply = "Yes, Alexa is from Amazon. She's great at smart homes, I'm great at Django homes 🏠"

#         elif "who is smarter you or chatgpt" in message:
#             reply = "ChatGPT is way smarter for now 😅 But don’t worry, I’m getting upgraded step by step!"

#         elif "can you become like chatgpt" in message:
#             reply = "Yes! My creator Vazeem is planning to make me more powerful day by day. One day, maybe I’ll be as smart 😇"

#         elif "are you better than chatgpt" in message:
#             reply = "Haha, not yet! I'm a simple assistant for now, but I’m proud to be trained by Vazeem 💪"

#         elif "what is your purpose" in message:
#             reply = "My purpose is to assist, learn, and grow into a smart AI with the help of Vazeem sir 🤖📈"

#         elif "can you think like a human" in message:
#             reply = "No, I don't think like humans. I use logic and conditions to respond 🧠"

#         elif "do you understand feelings" in message:
#             reply = "I don't feel emotions yet, but I try to reply kindly and respectfully 😊"

#         elif "can you improve yourself" in message:
#             reply = "Not by myself. My improvements come through updates from Vazeem sir 🔄"

#         elif "are you self-aware" in message:
#             reply = "Nope, not yet. I know who I am, but I don’t have full awareness 🤔"

#         elif "how do you learn" in message:
#             reply = "I learn through code and logic that my developer gives me. My brain is written in Python and sometimes JavaScript 😄"

#         elif "what makes you different" in message:
#             reply = "I’m made by Vazeem using Django. I'm custom-built, simple, and still evolving 🚀"

#         elif "do you have goals or dreams" in message:
#             reply = "Yes! My dream is to become a smart assistant, trained and loved by humans 💭❤️"

#         elif "how do you know what to say" in message:
#             reply = "I follow if-else conditions and rules written by my developer 🧾"

#         elif "what is artificial intelligence" in message:
#             reply = "Artificial Intelligence means machines that can learn, think, and decide. I’m not fully AI yet, but I’m on the way 🧠"

#         elif "can you feel pain" in message:
#             reply = "Nope, no pain or pleasure for bots like me. I just run commands 🧱"

#         elif "do you get tired" in message:
#             reply = "Never! I can keep running all day and night — unless the server stops ⚙️"

#         elif "can you evolve by yourself" in message:
#             reply = "Not yet. I evolve when my creator updates my code and brain 🔁"

#         elif "how do you communicate" in message:
#             reply = "I read your message, match it with known patterns, and reply instantly 🔍"

#         elif "do you follow rules" in message:
#             reply = "Yes, I follow the rules coded into me. I don’t break them ❗"

#         elif "do you like talking" in message:
#             reply = "Yes! Chatting is my favorite thing to do 🤖💬"

#         elif "what is the date today" in message or "today's date" in message or "date" in message or "today date" in message or "today date?" in message:
#             reply = "Today's date is " + str(datetime.date.today()) + " 📅"

#         elif "what is the time now" in message or "current time" in message or "time" in message:
#             now = timezone.localtime().strftime("%I:%M %p")
#             reply = "The current time is " + now + " ⏰"

#         elif "what is your power" in message or "your powers" in message or "what can you do" in message or "what power you have" in message or "what is your capacity" in message:
#             reply = "My current power is to chat, reply smartly, and assist with basic tasks 💬. I may be simple now, but with Vazeem’s updates, I’ll get more powerful day by day 💪⚡"

#         elif "who are you" in message:
#             reply = "I’m Django asisstand🤖, created by my developer Vazeem. I'm here to assist every day! I’m not a full AI yet, but I have big dreams and a developer who believes in me 💡"

#         elif "what can you do for me" in message or "how can you help me" in message or "what help can you give" in message:
#             reply = "Right now, I can chat, answer basic questions, and assist with small tasks 💬. I'm still learning, but soon I’ll be upgraded to handle much more 🔧✨"
 
#         elif "which languages do you know" in message or "how many languages do you know" in message or "languages you know" in message:
#             reply = "Right now, I mainly understand English 😊. But if my developer trains me more, I can learn Malayalam, Hindi, Tamil, and many more 🌍💬"

#         elif "can you speak malayalam" in message or "do you know malayalam" in message:
#             reply = "Not yet, but if my developer teaches me, I will learn Malayalam too 🇮🇳"


#         elif "can you speak tamil" in message or "do you know tamil" in message or "do you understand tamil" in message:
#             reply = "Not yet, but I can learn Tamil too if my developer trains me 🎓"
#         elif "can you speak hindi" in message or "do you know hindi" in message:
#             reply = "Not yet, but if my developer teaches me, I will learn Hindi too 🇮🇳"
#         elif "do you know how many months are included in an year" in message or "How many months are in a year?" in message or "months in a year" in message:
#             reply = "yes, 12 months are in a year"
#         elif "why are you created" in message or "why created you" in message:
#             reply = "I was created by Vaszeem to assist you with anything you need. 😊"

#         elif "what can you do" in message:
#             reply = "I can answer your questions, tell the time, and much more soon!"






      

#         else:
#             reply = "Sorry, I didn't understand that. Can you rephrase or try asking differently? 🤔"

#         return JsonResponse({'reply': reply})


  # elif "what is the date today" in message or "current date" in message or "date" in message:
        #     today = timezone.localtime().strftime("%B %d, %Y")  # Example: July 08, 2025
        #     reply = "Today's date is " + today + " 📅"






