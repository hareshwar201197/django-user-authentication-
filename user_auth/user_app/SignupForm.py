from django import forms
from .models import User

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if len(mobile) != 10:  # Simple validation for mobile number length
            raise forms.ValidationError('Mobile number must be 10 digits.')
        return mobile