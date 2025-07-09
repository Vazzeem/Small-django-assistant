from django.shortcuts import render, redirect
from .models import myai
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
import openai
import json
import datetime

# ✅ Correct: use OPENAI API key from Django settings
openai.api_key = settings.OPENAI_API_KEY

# ---------------------- Register ----------------------
def r(request):
    if request.method == 'POST':
        adminn = request.POST['name']
        passw = request.POST['password']
        myai.objects.create(admin=adminn, password=passw)
    return render(request, 'r.html')

# ---------------------- Login ----------------------
def login(request):
    if request.method == 'POST':
        adminn = request.POST['name']
        passw = request.POST['password']
        myadmin = myai.objects.filter(admin=adminn, password=passw)
        if myadmin:
            request.session['my'] = adminn
            return redirect('ui')
        else:
            messages.info(request, "Login failed")
    return render(request, 'login.html')

# ---------------------- UI ----------------------
def ui(request):
    if 'my' in request.session:
        m = request.session['my']
        return render(request, 'ui.html', {'p': m})
    return render(request, 'ui.html')

# ---------------------- OpenAI Reply ----------------------
def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return "Sorry, I couldn't process your request right now."

# ---------------------- Chatbot View (AI + Rule-Based) ----------------------
@csrf_exempt
def chatbot_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()

        # ✅ Rule-based responses first
        if "who is your creator" in user_message or "who created you" in user_message:
            bot_reply = "I was created by my sir and developer Vazeem 👨‍💻"
        elif "what is your name" in user_message:
            bot_reply = "My name is AI Assistander 🤖"
        elif "how old are you" in user_message:
            bot_reply = "I was born on July 6, 2025 😄"
        elif "do you know malayalam" in user_message:
            bot_reply = "Yes, I can understand simple Malayalam 😊"
        elif "what is the date" in user_message:
            bot_reply = f"Today's date is {datetime.date.today()} 📅"
        elif "what is the time" in user_message:
            now = timezone.localtime().strftime("%I:%M %p")
            bot_reply = f"The current time is {now} ⏰"
        else:
            # ✅ Fallback to OpenAI
            bot_reply = ask_openai(user_message)

        return JsonResponse({'reply': bot_reply})
