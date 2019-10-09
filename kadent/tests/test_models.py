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