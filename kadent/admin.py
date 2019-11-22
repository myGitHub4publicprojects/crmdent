from django.contrib import admin

from .models import Patient, Visit, Image


admin.site.register(Patient)
admin.site.register(Visit)
admin.site.register(Image)