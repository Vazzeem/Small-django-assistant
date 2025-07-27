from django.shortcuts import render, redirect
from .models import aimodel
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
from openai import OpenAI
import json
import datetime

# ✅ Initialize OpenRouter-compatible client with safe fallback
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY or "sk-or-v1-your-key",  # fallback only for local dev
    default_headers={
        "HTTP-Referer": "https://small-django-assistant.onrender.com",  # Your live site URL
        "X-Title": "Vazeem Assistant",
    }
)

# ---------------------- Register ----------------------
def r(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('p')
        cpassw = request.POST.get('cp')
        x = aimodel.objects.filter(email=email)
        if x:
            messages.info(request,"Email already exists pls create another one")
        elif passw != cpassw:
            messages.info(request, "password does not match")
        else:
            aimodel.objects.create(Username=name, password=passw, email=email)
            messages.success(request, "Success")
            return redirect('login')
    return render(request, 'r.html')

# ---------------------- Login ----------------------
def login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('p')
        user = aimodel.objects.filter(email=email, password=passw).first()
        if user:
            request.session['mye'] = user.email 
            request.session['myu'] = user.Username
            return redirect('ui')
        else:
            messages.error(request, "Login failed")
    return render(request, 'login.html')

# ---------------------- UI ----------------------
def ui(request):
    if 'mye' in request.session:
        mail = request.session['mye']
    if 'myu' in request.session:
        uname = request.session['myu']
    
        return render(request, 'ui.html', {'E': mail,'U':uname})
    return redirect('login')

# ---------------------- Ask AI from OpenRouter ----------------------
def ask_openrouter_ai(message):
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": message}]
        )
        ai_reply = completion.choices[0].message.content

        # 🛑 Filter or modify any "Mistral AI" mentions
        if "mistral" in ai_reply.lower():
            return "I'm powered by custom AI technology developed by my creator Vazeem 💡"
        
        return ai_reply
    except Exception as e:
        print("❌ AI Error:", str(e))
        return "Sorry, I couldn't process your request right now."


# ---------------------- Chatbot View (Rule + AI) ----------------------
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower().strip()

            if not user_message:
                return JsonResponse({'reply': "Please send a valid message."})

            # ✅ Rule-based replies
            if "who is your creator" in user_message or "who created you" in user_message:
                bot_reply = "I was created by my sir and developer Vazeem K👨‍💻"
            elif "what is your name" in user_message:
                bot_reply = "My name is AI Assistander 🤖"
            elif "how old are you" in user_message or "your age?" in user_message or "age" in user_message:
                bot_reply = "I was born on July 6, 2025 😄"
            elif "do you know malayalam" in user_message:
                bot_reply = "Yes, I can understand simple Malayalam 😊"
            elif "what is the date" in user_message:
                bot_reply = f"Today's date is {datetime.date.today()} 📅"
            elif "what is the time" in user_message or "time now" in user_message or "time" in user_message or "time?" in user_message or "what is the time now?" in user_message or "what is the time now" in user_message:
                now = timezone.localtime().strftime("%I:%M %p")
                bot_reply = f"The current time is {now} ⏰"
            elif any(x in user_message for x in ["what is the date", "date now", "today's date", "current date","date","date?"]):
                bot_reply = f"Today's date is {datetime.date.today()} 📅"
            elif any(x in user_message for x in ["what do you know about your creator", "what you know about your creator", "tell me about your creator"]):
                bot_reply = "I was created by my intelligent developer Vazeem 👨‍💻. He trained me to be helpful and friendly!"

            elif "do you have brain" in user_message or "do you have a brain" in user_message or "you have a brain" in user_message or "you have brain" in user_message:
                bot_reply = "yes, I am an artificial intelligence and don't have physical organs or biological functions like a human. I am a program running on capable of processing information and generating responses based on that information, but I do not have consciousness, emotions, or biological needs like a human does. but I run on powerful AI models 🧠"
            elif "mistral" in user_message or "mistral ai" in user_message:
                bot_reply = "I'm powered by custom AI created and managed by Vazeem 💡"
            elif any(x in user_message for x in ["who is your creator", "who created you", "about your creator", "your developer", "who made you","your developer","how were you built","who programmed you", "who designed you","your programmer","who coded you","who is your programmer","who are your programmr","who build you","who is build you","who is builded you"]):
                bot_reply = "I was created and fine-tuned by my developer Vazeem k👨‍💻, Sir using custom AI tools 💡"
            if any(x in user_message for x in [
                    "can you detect the system’s theme and change automatically",
                    "can you detect the device theme and change automatically",
                    "can you detect the mobile theme and change automatically",
                    "can you detect the mobile theme"
                ]):
                 bot_reply = "Yes, I can"


            elif "who are you" in user_message:
                bot_reply = "I'm Vazeem's smart assistant 🤖, ready to help you with anything you need!"
            elif "do you have dark mode" in user_message or "dark mode available" in user_message or "enable dark mode" in user_message:
                bot_reply = "Yes, I support Dark Mode 🌙. You can click the 'Dark Mode' button on the top left to switch."
            elif "Can you detect the system’s theme and change automatically" in user_message or "Can you detect the device theme and change automatically?" in user_message or "Can you detect the mobile theme and change automatically" in user_message or "Can you detect the device theme and change automatically?" in user_message or "Can you detect the mobile theme" in user_message:
                bot_reply = "Yes, I can"

            else:
                # ✅ AI fallback
                bot_reply = ask_openrouter_ai(user_message)

            return JsonResponse({'reply': bot_reply})

        except json.JSONDecodeError:
            return JsonResponse({'reply': "Invalid JSON format."}, status=400)

    return JsonResponse({'reply': "Method not allowed."}, status=405)
