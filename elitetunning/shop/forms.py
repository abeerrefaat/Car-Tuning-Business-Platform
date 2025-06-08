
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    phone = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

