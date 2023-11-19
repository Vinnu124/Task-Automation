from django.shortcuts import render, redirect
from .models import autho
# from django.contrib.auth import authenticate, login
from .forms import login_form, signup_form
from django.contrib import messages


def base_view(request):
    return render(request, 'base_home.html')


def login_view(request):
    if request.method == 'POST':
        form = login_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Remove 'email' parameter when calling authenticate
            # user = authenticate(request, username=username, password=password)
            filtered = autho.objects.filter(
                username=username, password=password)
            if filtered.exists():
                request.session['username'] = username
                print("Success: Valid credentials")
                return redirect('http://localhost:8000/authorization/base_home/')
            # if user is not None:
            #     login(request, user)
            #     return redirect('admin')
            else:
                return redirect('http://localhost:8000/authorization/signup/')

    form = login_form()

    context = {
        'form': form

    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = signup_form(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = form.cleaned_data['create_password']
            user.username = form.cleaned_data['create_username']
            user.email = form.cleaned_data['enter_email']
            if autho.objects.filter(username=user.username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            elif autho.objects.filter(email=user.email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')

            user.save()
        return redirect('login')

    form = signup_form()
    context = {'form': form}
    return render(request, 'signup.html', context)
# Create your views here.
