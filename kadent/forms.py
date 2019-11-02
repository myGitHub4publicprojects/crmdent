from django import forms

from .models import Image

class ImageCreateForm(forms.Form):
    note = forms.CharField(label='Note', max_length=100)
