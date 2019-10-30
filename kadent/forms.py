from django import forms

from kadent.models import Image


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('file', )
