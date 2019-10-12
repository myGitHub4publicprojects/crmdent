# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.urls import reverse

from .validators import accepted_extensions, accepted_size

class Patient(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_absolute_url(self):
        return reverse('kadent:patient_edit', kwargs={'pk': self.pk})

    def __str__(self):
        return self.full_name()


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('kadent:visit_detail', kwargs={'pk': self.pk})


class Image(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.ImageField(
        upload_to='documents/', validators=[accepted_extensions, accepted_size])
    note = models.TextField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    visit = models.ForeignKey(
        Visit, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('kadent:image_detail', kwargs={'pk': self.pk})

