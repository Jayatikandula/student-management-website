from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from .forms import RegistrationForm, ProfileUpdateForm
from .models import StudentProfile
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html')
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            password = form.cleaned_data.get('password')  # Correct way to get the password
            user = User.objects.create_user(
                username=profile.roll_number,
                password=password
            )
            profile.user = user
            profile.save()
            
            send_mail(
                'Registration Successful',
                'You have been successfully registered! Please log in.',
                'kandula.jayati@gmail.com',
                [profile.email],
                fail_silently=False,  # This will raise an error if sending fails
            )

            messages.success(request, 'Registration successful! Check your email.')
            return redirect('login')
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})


def display_data(request):
    data = StudentProfile.objects.all()
    return render(request, 'display_data.html', {'data': data})

def profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
