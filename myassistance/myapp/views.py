from django.shortcuts import render, redirect
from .models import myai
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
        adminn = request.POST.get('name')
        passw = request.POST.get('password')
        if adminn and passw:
            myai.objects.create(admin=adminn, password=passw)
            messages.success(request, "Registered successfully!")
            return redirect('login')
    return render(request, 'r.html')

# ---------------------- Login ----------------------
def login(request):
    if request.method == 'POST':
        adminn = request.POST.get('name')
        passw = request.POST.get('password')
        myadmin = myai.objects.filter(admin=adminn, password=passw).first()
        if myadmin:
            request.session['my'] = adminn
            return redirect('ui')
        else:
            messages.error(request, "Login failed")
    return render(request, 'login.html')

# ---------------------- UI ----------------------
def ui(request):
    if 'my' in request.session:
        m = request.session['my']
        return render(request, 'ui.html', {'p': m})
    return redirect('login')

# ---------------------- Ask AI from OpenRouter ----------------------
def ask_openrouter_ai(message):
    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": message}]
        )
        return completion.choices[0].message.content.strip()
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

            else:
                # ✅ AI fallback
                bot_reply = ask_openrouter_ai(user_message)

            return JsonResponse({'reply': bot_reply})

        except json.JSONDecodeError:
            return JsonResponse({'reply': "Invalid JSON format."}, status=400)

    return JsonResponse({'reply': "Method not allowed."}, status=405)
