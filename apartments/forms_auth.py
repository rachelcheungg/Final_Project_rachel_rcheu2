from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="We'll use this email if we need to contact you."
    )

    class Meta:

        model = User
        fields = ["username", "email", "password1", "password2"]