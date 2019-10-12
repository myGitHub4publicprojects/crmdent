# -*- coding: utf-8 -*-
from django.test import TestCase, Client
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator
from django.contrib.messages import get_messages
from mixer.backend.django import mixer

import os
import pytest
import shutil
import tempfile

from django.conf import settings
from django.core.files import File
from datetime import datetime, timedelta
from django.contrib.staticfiles.templatetags.staticfiles import static

from kadent.models import (Patient, Visit, Image)

pytestmark = pytest.mark.django_db
today = datetime.today().date()
now = datetime.now()


class TestCreteView(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', password='glassonion')

    def test_anonymous(self):
        url = reverse('kadent:patient_create')
        expected_url = reverse('login') + '?next=/patient_create'
        response = self.client.post(url, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)
                             
    def test_logged_in(self):
        self.client.login(username='john', password='glassonion')
        data = {'first_name': 'Adam',
                'last_name': 'Atkins',
                }

        url = reverse('kadent:patient_create')
        # id of new patient should be 1
        expected_url = reverse('kadent:patient_edit', args=(1,))
        response = self.client.post(url, data, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                     status_code=302, target_status_code=200)
        patients = Patient.objects.all()
        self.assertEqual(patients.count(), 1)
        self.assertEqual(patients.first().created_by.username, 'john')

class TestPatientUpdate(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', password='glassonion')

    def test_anonymous(self):
        url = reverse('kadent:patient_edit', args=(1,))
        expected_url = reverse('login') + '?next=/1/patient_edit/'
        response = self.client.post(url, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)


    def test_edit_fname_lname_note(self):
        self.client.login(username='john', password='glassonion')
        mixer.blend('kadent.Patient', first_name='A', last_name='B', notes='ąć')
        url = reverse('kadent:patient_edit', args=(1,))
        expected_url = reverse('kadent:patient_edit', args=(1,))
        data = {
            'first_name': 'ć',
            'last_name': 'łź',
            'notes': 'ó'
        }
        response = self.client.post(url, data, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)

        patient = Patient.objects.all().first()
        self.assertEqual(patient.first_name, 'ć')
        self.assertEqual(patient.last_name, 'łź')
        self.assertEqual(patient.notes, 'ó')
