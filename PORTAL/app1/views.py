from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import requests

def home_view(request):
    return render(request, 'home.html')

def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Redirecting to home page...")
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")

    return render(request, 'login.html')


def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')

        if password1 != password2:
            return HttpResponse("Your password and confirm password do not match.")
        
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        # Create the user
        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('login')  # Redirect to the login page after successful signup

    return render(request, 'signup.html')

def fetch_news(request):
    api_key = '421d25b85f06645b73a653c33eefd5e5'  # Your GNews API key
    url = f'https://gnews.io/api/v4/top-headlines?country=in&category=health&token={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print(response.json())  # Print the entire JSON response
        articles = response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        articles = []  # Set articles to an empty list in case of an error

    return render(request, 'new_list.html', {'articles': articles})

def Doctors(request):
    return render(request, 'General Practitioner.html')