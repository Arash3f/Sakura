from django import forms
from django.contrib.auth.models import User
from accounts.models import users

class user_edit_form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' , 'email' , 'is_active' , 'is_staff' , 'is_superuser']

class users_edit_form(forms.ModelForm):
    user = user_edit_form()

    class Meta:
        model = users
        fields = ['user', 'accessibility' ]