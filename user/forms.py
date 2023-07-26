from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import User
from django.contrib.auth import get_user_model
from .models import User


User = get_user_model()

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ['email', 'password']