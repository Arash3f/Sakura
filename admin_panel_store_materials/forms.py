from django import forms
from admin_panel_store_materials import models
# from django.forms import inlineformset_factory
class materials_edit_form(forms.ModelForm):

    class Meta:
        model = models.materials
        fields = ['id', 'name']
        widgets = {'id': forms.NumberInput(attrs={'readonly':True}),}
    
class materials_add_form(forms.ModelForm):

    class Meta:
        model = models.materials
        fields = ['id', 'name']

class journal_edit_form_helper_materials(forms.ModelForm):

    class Meta:
        model = models.materials
        fields = ['id', 'name']


class journal_edit_form(forms.ModelForm):

    class Meta:
        model = models.journal
        fields = ['materials','description', 'debtor' , 'creditor']
