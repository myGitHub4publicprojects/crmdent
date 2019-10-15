# -*- coding: utf-8 -*-
import os
import pytest
import shutil
import tempfile
from django.core.exceptions import ValidationError

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
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(dir=settings.BASE_DIR)
        settings.MEDIA_ROOT = self.test_dir

        # copy file to temp dir inside media to avoid SuspiciousFileOperation error
        src = os.getcwd() + '/kadent/tests/test_files/08MB.jpg'
        os.mkdir(self.test_dir + '/xxx')
        shutil.copyfile(src, self.test_dir + '/xxx/08MB.jpg')


    # def test_with_empty_file(self):
    #     '''the test file is empty - should not be allowed'''

    #     # create object
        # f = File(open(
        #     self.test_dir + '/xxx/empty.jpg', 'rb'))  # use 'rb' to read as bytes, no decoding
        # s = mixer.blend('kadent.Image', file=f)

    #     # validate
    #     s.full_clean()

    #     # filename should be 'empty.xls'
    #     self.assertEqual(s.filename(), 'empty.jpg')

    def test_with_file(self):
        '''should create an Image object with a file field'''
        # create object
        f = File(open(
            self.test_dir + '/xxx/08MB.jpg', 'rb')) # use 'rb' to read as bytes, no decoding
        s = mixer.blend('kadent.Image', file=f)


        self.assertEqual(s.file.name, '08MB.jpg')

        # filename should be '08MB.jpg'
        self.assertEqual(os.path.basename(s.file.name), '08MB.jpg')
        

    # def test_with_oversided_file(self):
    # pass

    # def test_with_unaccepted_extensions(self):
    #     pass

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)
