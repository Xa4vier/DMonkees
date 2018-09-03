import datetime

from django import forms
from django.core.exceptions import ValidationError


class loginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()