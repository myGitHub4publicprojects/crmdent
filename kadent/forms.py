from django import forms

from .models import Image, Patient

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['file', 'note']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'cols': 60, 'rows': 2}),
        }
