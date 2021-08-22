from django import forms
from django.contrib.auth.models import User
from accounts.models import users

class users_edit_form(forms.ModelForm):

    class Meta:
        model = users
        fields = ['user', 'accessibility' ]