from django.urls import path
from .views import signup, verify_email, email_verification_sent, user_login, about


urlpatterns = [
    path('signup/', signup, name='signup'),
    path('verify_email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('email_verification_sent/', email_verification_sent, name='email_verification_sent'),
    path('login/', user_login, name='login'),
    path('about/', about, name='about'),
]
