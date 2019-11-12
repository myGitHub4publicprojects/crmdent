from django import forms
from django.forms import modelformset_factory
from .models import Image, Patient


ImageFormSet = modelformset_factory(Image, fields=('note', 'file'))


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 60, 'rows': 2}),
        }