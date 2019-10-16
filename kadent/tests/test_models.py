# -*- coding: utf-8 -*-
import os
import pytest
import shutil
import tempfile
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.conf import settings
from django.test import TestCase
from mixer.backend.django import mixer
from django.core.files import File
from kadent.models import Patient, Visit, Image


class TestPatient(TestCase):
    def test_patient_full_name(self):
        p = mixer.blend('kadent.Patient',
                        first_name = 'Olo',
                        last_name = 'Smith')
        self.assertEqual(p.full_name(), 'Olo Smith')

    def test_patient_str(self):
        p = mixer.blend('kadent.Patient',
                        first_name='Olo',
                        last_name='Smith')
        self.assertEqual(str(p), 'Olo Smith')


class Test_Image(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_dir = tempfile.mkdtemp(dir=settings.BASE_DIR)
        settings.MEDIA_ROOT = cls.test_dir


    @classmethod
    def tearDownClass(cls):
        # Remove the directory after the test
        shutil.rmtree(cls.test_dir)


    def test_with_empty_file(self):
        '''the test file size is under 1kb - should not be allowed'''
        src = os.getcwd() + '/kadent/tests/test_files/empty.jpg'
        shutil.copyfile(src, self.test_dir + '/empty.jpg')
        # create object
        f = File(open(
            self.test_dir + '/empty.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding
        s = mixer.blend('kadent.Image', file=f)

        self.assertRaises(ValidationError, s.full_clean)


    def test_with_file(self):
        '''should create an Image object with a file field'''
        # copy file to temp dir inside media to avoid SuspiciousFileOperation error
        src = os.getcwd() + '/kadent/tests/test_files/08MB.jpg'
        shutil.copyfile(src, self.test_dir + '/08MB.jpg')

        p = mixer.blend('kadent.Patient')
        u = User.objects.create_user(username='john', password='glassonion')
        # create object
        f = File(open(
            self.test_dir + '/08MB.jpg', 'rb')) # use 'rb' to read as bytes, no decoding
        s = Image.objects.create(
            file=f,
            note='some note',
            uploaded_by=u,
            patient=p,
        )
        # validate
        s.full_clean()

        i = Image.objects.all()
        self.assertTrue(i.exists())
        self.assertEqual(i.count(), 1)
        self.assertEqual(i.first().note, 'some note')
        

    def test_with_oversided_file(self):
        src = os.getcwd() + '/kadent/tests/test_files/30MB.jpg'
        shutil.copyfile(src, self.test_dir + '/30MB.jpg')
        # create object
        f = File(open(
            self.test_dir + '/30MB.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding
        s = mixer.blend('kadent.Image', file=f)

        self.assertRaises(ValidationError, s.full_clean)

    def test_with_unaccepted_extensions(self):
        '''.txt file should not be allowed'''
        src = os.getcwd() + '/kadent/tests/test_files/1.txt'
        shutil.copyfile(src, self.test_dir + '/1.txt')
        # create object
        f = File(open(
            self.test_dir + '/1.txt', 'rb'))  # use 'rb' to read as bytes, no decoding
        s = mixer.blend('kadent.Image', file=f)

        self.assertRaises(ValidationError, s.full_clean)