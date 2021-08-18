from django import forms
from django.contrib.auth.models import User

class user_edit_form(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name' , 'email' , 'is_active' , 'is_staff' , 'is_superuser']