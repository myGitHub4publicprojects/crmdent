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


class MyTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', password='glassonion')


class TestPatientCreteView(MyTestCase):
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


class TestPatientUpdate(MyTestCase):
    
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


class VisitCreate(MyTestCase):
    def test_anonymous(self):
        url = reverse('kadent:visit_create', args=(1,))
        expected_url = reverse('login') + '?next=/1/visit_create/'
        response = self.client.post(url, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)


    def test_create(self):
        self.client.login(username='john', password='glassonion')
        p = mixer.blend('kadent.Patient', first_name='A', last_name='B', notes='ąć')
        url = reverse('kadent:visit_create', args=(1,))
        expected_url = reverse('kadent:visit_edit', args=(1,))
        data = {'note': 'ó'}
        response = self.client.post(url, data, follow=True)
        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)

        v = Visit.objects.all()
        # should create one Visit
        self.assertEqual(v.count(), 1)
        # Visit.doctor should be logged in user
        self.assertEqual(v.first().doctor.username, 'john')


class TestImageCreateFromPatient(MyTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_dir = tempfile.mkdtemp(dir=settings.BASE_DIR)
        settings.MEDIA_ROOT = cls.test_dir

    @classmethod
    def tearDownClass(cls):
        # Remove the directory after the test
        shutil.rmtree(cls.test_dir)


    def test_image_08MB_jpg(self):
        '''one file, image has 0.8MB and extension = .jpg'''
        self.client.login(username='john', password='glassonion')
        p = mixer.blend('kadent.Patient')
        # copy file to temp dir inside media to avoid SuspiciousFileOperation error
        src = os.getcwd() + '/kadent/tests/test_files/08MB.jpg'
        shutil.copyfile(src, self.test_dir + '/08MB.jpg')
        # create File
        f = File(open(
            self.test_dir + '/08MB.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding
        url = reverse('kadent:image_create_from_patient', args=(p.id,))
        expected_url = reverse('kadent:patient_edit', args=(p.id,))
        data = {
                # formset management data
                'form-TOTAL_FORMS': 1,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,

                # test data
                'images': [f,],
                '08MB.jpg': 'test notęŁ'

                }
        response = self.client.post(url, data, follow=True)

        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)
        images = Image.objects.all()
        self.assertEqual(images.count(), 1)
        self.assertEqual(images.first().note, 'test notęŁ')


    def test_two_images(self):
        '''both images are 0.8MB and extension = .jpg'''
        self.client.login(username='john', password='glassonion')
        p = mixer.blend('kadent.Patient')
        # copy file to temp dir inside media to avoid SuspiciousFileOperation error
        src = os.getcwd() + '/kadent/tests/test_files/08MB.jpg'
        shutil.copyfile(src, self.test_dir + '/08MB.jpg')
        # create File
        f = File(open(
            self.test_dir + '/08MB.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding
        src2 = os.getcwd() + '/kadent/tests/test_files/08MB2.jpg'
        shutil.copyfile(src2, self.test_dir + '/08MB2.jpg')
        # create File
        f2 = File(open(
            self.test_dir + '/08MB2.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding

        url = reverse('kadent:image_create_from_patient', args=(p.id,))
        expected_url = reverse('kadent:patient_edit', args=(p.id,))
        data = {
                # formset management data
                'form-TOTAL_FORMS': 2,
                'form-INITIAL_FORMS': 0,
                'form-MIN_NUM_FORMS': 0,
                'form-MAX_NUM_FORMS': 1000,

                # test data
                'images': [f,f2],
                '08MB.jpg': 'test notęŁ',
                '08MB2.jpg': '08MB2 test note'
                }
        response = self.client.post(url, data, follow=True)

        # should give code 200 as follow is set to True
        assert response.status_code == 200
        self.assertRedirects(response, expected_url,
                             status_code=302, target_status_code=200)
        images = Image.objects.all()
        self.assertEqual(images.count(), 2)
        self.assertEqual(images.first().note, 'test notęŁ')
        self.assertEqual(images.last().note, '08MB2 test note')

# class TestImageCreateFromVisit(TestImageCreateFromPatient):
#     @classmethod
#     def setUpTestData(cls):
#         cls.test_dir = tempfile.mkdtemp(dir=settings.BASE_DIR)
#         settings.MEDIA_ROOT = cls.test_dir

#     @classmethod
#     def tearDownClass(cls):
#         # Remove the directory after the test
#         shutil.rmtree(cls.test_dir)

#     def test_image_08MB_jpg(self):
#         '''image has 0.8MB and extension = .jpg'''
#         self.client.login(username='john', password='glassonion')
#         mixer.blend('kadent.Visit')
#         # copy file to temp dir inside media to avoid SuspiciousFileOperation error
#         src = os.getcwd() + '/kadent/tests/test_files/08MB.jpg'
#         shutil.copyfile(src, self.test_dir + '/08MB.jpg')
#         # create File
#         f = File(open(
#             self.test_dir + '/08MB.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding

#         url = reverse('kadent:image_create_from_visit', args=(1,))
#         expected_url = reverse('kadent:image_edit', args=(1,))
#         data = {'file': f, 'note': 'test notęŁ'}
#         response = self.client.post(url, data, follow=True)

#         # should give code 200 as follow is set to True
#         assert response.status_code == 200
#         self.assertRedirects(response, expected_url,
#                              status_code=302, target_status_code=200)
#         images = Image.objects.all()
#         self.assertEqual(images.count(), 1)
#         self.assertEqual(images.first().note, 'test notęŁ')


# class TestImageDelete(MyTestCase):
#     def test_img(self):
#                 # message = 'Usunięto obraz'
#         pass
