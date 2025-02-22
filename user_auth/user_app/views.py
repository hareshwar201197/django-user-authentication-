from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from .models import User
from .SignupForm import SignupForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.urls import reverse


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered. Please log in.')
            else:
                user = form.save(commit=False)
                user.username = email
                user.set_password(form.cleaned_data['password'])
                user.is_active = False  # Require email verification
                user.save()
                send_verification_email(request, user)

                messages.success(request, "Signup successful! Please check your email to verify your account.")
                return redirect('verification_sent')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.is_active = True  # Now the user can log in
        user.save()
        return redirect('login')  # Redirect to login page after successful verification
    else:
        messages.error(request, "Invalid verification link. Please sign up again.")
    return redirect('signup')


def email_verification_sent(request):
    return render(request, 'verification_sent.html')


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user and user.is_active:
                login(request, user)
                return redirect('about')
            else:
                messages.error(request, "Your email is not verified yet.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def about(request):
    return render(request, 'about.html')


def send_verification_email(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uidb64, 'token': token})
    )

    subject = "Verify Your Email"
    message = f"Hi {user.first_name},\n\nClick the link below to verify your email:\n{verification_link}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )


def delete_user():
    User.objects.filter(email__in=['hareshwarmali20@gmail.com']).delete()
