from django.forms import modelformset_factory
from .models import Image


ImageFormSet = modelformset_factory(Image, fields=('note', 'file'))