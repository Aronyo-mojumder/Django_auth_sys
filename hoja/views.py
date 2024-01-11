from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import TokenGenerator  # Assuming TokenGenerator is correctly implemented
from please import settings

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        email = request.POST['email']

        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        myuser = User.objects.create_user(username=username, email=email, password=pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request, 'Your account has been created!')

        current_site = get_current_site(request)
        uidb64 = urlsafe_base64_encode(force_bytes(myuser.pk))
        token = TokenGenerator().make_token(myuser)
        activation_link = f"http://{current_site.domain}/activate/{uidb64}/{token}/"

        subject = "Welcome to Education bd Login"
        message = f"Hello {myuser.first_name}!\nWelcome to education bd!!\nThank you for registering.\nPlease confirm your email by clicking the link below:\n\n{activation_link}\n\nThank you,\nAronyo Mojumder"

        send_mail(subject, message, settings.EMAIL_HOST_USER, [myuser.email], fail_silently=True)

        return redirect('conf_email_sent', uidb64=uidb64, token=token)

    return render(request, 'signup.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and TokenGenerator().check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        auth_login(request, myuser)
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')


def conf_email_sent(request, uidb64, token):
    return render(request, 'conf_email.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def home(request):
    username = request.user.username if request.user.username else None
    return render(request, 'home.html', {'username': username})


def user_logout(request):
    auth_logout(request)
    return redirect('login')
