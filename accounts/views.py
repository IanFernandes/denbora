from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from accounts.forms import RegisterForm, LoginForm
from accounts.models import User
from django.core.mail import EmailMultiAlternatives
from accounts.functions import generate_salt, unsalt
from django.contrib.auth import authenticate, login, logout


def register(request):
    message = ""
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
                    message = "This Username or Email already exists"
                else:
                    password = register_form.cleaned_data['password']
                    user = User.objects.create_user(username, email, password)
                    user.is_active = False
                    user.save()
                    # manage_emailing(username, email, request.META['HTTP_HOST'])
                    return HttpResponseRedirect('/accounts/thanks/')
            else:
                message = "Passwords do not match"
    # if a GET (or any other method) we'll create a blank form
    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {'register_form': register_form, 'message': message})


def thanks(request):
    return HttpResponse("Correctly registered, we send you an Email to activate your account")


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
            message = username + ", your account has been activated"
        else:
            message = username + ", your account is already activated !"
    else:
        message = "This url is not valid"
    return render(request, 'accounts/activate.html', {'message': message})


def signin(request):
    next_url = ""
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profiles')
    message = ""
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
                message = "User does not exist"

    else:
        login_form = LoginForm()
        if 'next' in request.GET:
            next_url = request.GET['next']
    return render(request, 'accounts/login.html', {'login_form': login_form, 'message': message, 'next_url': next_url})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/accounts/logged_out/')
    else:
        return HttpResponseRedirect('/accounts/signin/')


def logged_out(request):
    return render(request, 'accounts/logout.html')


def manage_emailing(username, email, host):
    host = "http://" + host
    logo_url = "http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/glossy-black-icons-business/080807-glossy-black-icon-business-hourglass.png"
    data = generate_salt(username)
    subject, from_email, to = 'Activate your account', 'jonazkue.f@gmail.com', email
    text_content = 'Welcome to Denbora.'
    html_content = '<img src="' + logo_url + '" width="42" height="42">' \
                    '<h2>Denbora</h2>' \
                    '<p>Welcome to Denbora ' + username + '</p>' \
                    '<a href="' + host + '/accounts/activate/q=' + data + '"> Click Here to activate you account</a>' \
                    '<p>Thank You</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

