from django import forms
from admin_panel_accounting import models
# from django.forms import inlineformset_factory
class account_edit_form(forms.ModelForm):

    class Meta:
        model = models.account
        fields = ['id', 'name']
        widgets = {'id': forms.NumberInput(attrs={'readonly':True}),}
    
class account_add_form(forms.ModelForm):

    class Meta:
        model = models.account
        fields = ['id', 'name']

class journal_edit_form_helper_account(forms.ModelForm):

    class Meta:
        model = models.account
        fields = ['id', 'name']


class journal_edit_form(forms.ModelForm):

    # account  = inlineformset_factory(models.account, fields=('id', 'name'))

    class Meta:
        model = models.journal2
        fields = ['account','description', 'debtor' , 'creditor']
