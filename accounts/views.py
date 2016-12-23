from django.shortcuts import render
from django.http import HttpResponseRedirect
from accounts.forms import RegisterForm, LoginForm
from accounts.models import User
from accounts.functions import unsalt, manage_emailing
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profiles')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        register_form = RegisterForm(request.POST)
        # check whether it's valid:
        if register_form.is_valid():
            if register_form.cleaned_data['password'] == register_form.cleaned_data['password_repeat']:
                username = register_form.cleaned_data['username']
                email = register_form.cleaned_data['email']
                # check if username or email exists
                if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                    messages.error(request, "This Username or Email already exists")
                else:
                    password = register_form.cleaned_data['password']
                    user = User.objects.create_user(username, email, password)
                    user.is_active = False
                    user.save()
                    messages.success(request, "Correctly registered, we send you an Email to activate your account")
                    manage_emailing(username, email, request.META['HTTP_HOST'])
                    return HttpResponseRedirect('/accounts/register/')
            else:
                messages.error(request, "Passwords do not match")
    # if a GET (or any other method) we'll create a blank form
    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': register_form})


def activate(request, data):
    username = unsalt(data)
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    if user:
        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(request, username + ", your account has been activated")
            return HttpResponseRedirect('/profiles/')
        else:
            messages.success(request, username + ", your account is already activated !")
            return HttpResponseRedirect('/profiles/')
    else:
        messages.error(request, "This url is not valid")
        return HttpResponseRedirect('/accounts/signin/')


def signin(request):
    next_url = ""
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profiles')
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page.
                if request.POST["next_url"]:
                    return HttpResponseRedirect(request.POST["next_url"])
                else:
                    return HttpResponseRedirect('/profiles')

            else:
                # Return an 'invalid login' error message.
                messages.error(request, "User does not exist")
    else:
        login_form = LoginForm()
        if 'next' in request.GET:
            next_url = request.GET['next']
    return render(request, 'accounts/login.html', {'login_form': login_form, 'next_url': next_url})


def user_logout(request):
    if request.user.is_authenticated:
        messages.success(request, "Logged out | See you soon " + request.user.username + " !")
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/accounts/signin/')


def logged_out(request):
    return render(request, 'accounts/logout.html')

