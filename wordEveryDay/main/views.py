from django.shortcuts import render
from openai import OpenAI
from django.http import JsonResponse
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.utils.html import strip_tags
import random
import json
from data.models import Users
from django.shortcuts import redirect
import os

def home(request):
    return render(request,"home.html")

def lastWordWas():
    with open("R:/rayhan-drive/everyDay_Word_ChatGPTApi/wordEveryDay/main/lastWord.txt", "r") as file_object:
        content = file_object.read()
        return content
    
    
def newWord(request):
    
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )   

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {"role": "user", "content": f"""
            You are AI assistant.Your work is give me a random english word everyday with bangla meaning and also 2 examples.
            The difficulty level of the words are will go to beginner to hard and expert day by day. Your last word was {lastWordWas()} .
            Give me the word of today.
            
            Note : I need only the last given word on top line. Then you response.
        
        """}
    ]
    )

    respons = completion.choices[0].message.content
    word=""
    for i in respons:
        if i=='\n':
            break
        word+=i

    print(respons)
    with open("R:/rayhan-drive/everyDay_Word_ChatGPTApi/wordEveryDay/main/lastWord.txt", "w",encoding="utf-8") as file_object:
        file_object.writelines(word)
        
        
    response = {
        "main_word":word,
        "meaning":respons.split('\n')[1:],
    }
        
    return JsonResponse(response)
        

def contact(request):
    return render(request, 'contact.html')
def about(request):
    return render(request, 'about.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Here you would typically check the username and password against your database
        if username == 'admin' and password == 'password':  # Example check
            return render(request, 'home.html', {'message': 'Login successful!'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
 
def signin(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        enterd_code = data.get('confirm_code')
        code = data.get('code')
        if enterd_code != code:
            return render(request, 'signin.html', {'error': 'Invalid verification code. Please try again.'})   
         
        username = data.get('uname')
        password = data.get('password')
        email= data.get('email')
        confirmPassword = data.get('confirm_password')
        print("Username:", username)
        data=Users.objects.create(
            username=username,
            password=confirmPassword,
            Email=email
        )
        data.save()
        
        # Here you would typically save the new user to your database
        return redirect("login/")
    
    return render(request, 'signin.html')


def send_code(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_name = data.get('uname')
        email = data.get('email')
        code = random.randint(100000,999999)
        subject = 'R-TO-DO Email Verification.'
        message = f'''
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f2f6fc; padding: 20px;">
            <h1 style="text-align: center; color: #0077cc;">everydayWord Email Verification</h1>
            <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #0077cc; text-align: center;">Verify Your Email Address</h2>
                <p>Hi <strong>{user_name}</strong>,</p>
                <p>Thanks for joining <strong>everydayWord</strong>! Please use the verification code below to verify your email address and start learning a new word every day:</p>
                
                <div style="text-align: center; margin: 20px 0;">
                    <p style="background-color: #e6f0fa; padding: 15px; border-left: 4px solid #0077cc; font-size: 24px; font-weight: bold; letter-spacing: 5px;">
                        {code}
                    </p>
                </div>
                
                <p style="text-align: center;">If you didn’t sign up for everydayWord, feel free to ignore this message.</p>
                <p style="text-align: center;">This code will expire in 30 minutes.</p>
                
                <hr style="border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="text-align: center; font-size: 12px; color: #888;">This is an automated message from everydayWord. Please do not reply.</p>
            </div>
        </body>
        </html>
        '''


        email_from = 'therayhan009@gmail.com'
        recipient_list = [email]
        email = EmailMultiAlternatives(subject, strip_tags(message), email_from, recipient_list)
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
        
        return JsonResponse({"message": "Verification code sent to your email.","code": code}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=400)
        