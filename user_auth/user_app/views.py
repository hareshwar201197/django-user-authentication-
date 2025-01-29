from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import User

from .SignupForm import SignupForm
from .models import User

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Create the user
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # User is inactive until email is verified
            user.save()

            # Send verification email
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(user.pk.encode())
            verification_link = f'http://{get_current_site(request).domain}/verify-email/{uid}/{token}/'
            send_mail(
                'Verify your email',
                f'Click the following link to verify your email: {verification_link}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('email_verification_sent')  # Show confirmation page
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
        return render(request, 'email_verification_failed.html')



def email_verification_sent(request):
    return render(request, 'email_verification_sent.html')


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_verified:  # Only allow login if verified
                login(request, user)
                return redirect('about')
            else:
                form.add_error(None, "Your email is not verified yet.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



@login_required
def about(request):
    return render(request, 'about.html')


