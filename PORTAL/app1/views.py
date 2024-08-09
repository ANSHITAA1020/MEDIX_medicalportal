from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def HomePage(request):
    return render(request, 'homepage.html')

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
