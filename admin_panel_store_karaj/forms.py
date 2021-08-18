from django import forms
from admin_panel_store_karaj import models
# from django.forms import inlineformset_factory
class product_edit_form(forms.ModelForm):

    class Meta:
        model = models.product
        fields = ['id', 'name']
        widgets = {'id': forms.NumberInput(attrs={'readonly':True}),}
    
class product_add_form(forms.ModelForm):

    class Meta:
        model = models.product
        fields = ['id', 'name']

class journal_edit_form_helper_product(forms.ModelForm):

    class Meta:
        model = models.product
        fields = ['id', 'name']


class journal_edit_form(forms.ModelForm):

    class Meta:
        model = models.journal
        fields = ['product','description', 'debtor' , 'creditor']
