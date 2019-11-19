import tempfile
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files import File

from kadent.validators import accepted_size, accepted_extensions


class TestAcceptedSize(TestCase):
    def test_size_0kb(self):
        '''size is below 1kb - should raise ValidationError'''
        t_f = tempfile.NamedTemporaryFile()
        t_f.flush()
        t_f.name = 'small.jpg'
        t_f.size = 1
        
        f = File(t_f)
        self.assertRaises(ValidationError, accepted_size, f)

        with self.assertRaises(ValidationError) as v:
            accepted_size(f)
        
        exp_msg = 'Plik small.jpg jest pusty. Użyj pliku większego od 1kb'
        self.assertEqual(v.exception.message, exp_msg)

    def test_size_5mb(self):
        '''file size is 5MB, should pass with no errors'''
        t_f = tempfile.NamedTemporaryFile()
        t_f.flush()
        t_f.size = 5*1024*1024
        t_f.name = '5mb.jpg'
        f = File(t_f)

        # should pass with no errors
        self.assertIsNone(accepted_size(f))

    def test_size_30mb(self):
        '''file size is 30MB, should raise ValidationError'''
        t_f = tempfile.NamedTemporaryFile()
        t_f.flush()
        t_f.size = 30*1024*1024
        t_f.name = '30mb.jpg'
        f = File(t_f)
        self.assertRaises(ValidationError, accepted_size, f)

        with self.assertRaises(ValidationError) as v:
            accepted_size(f)

        exp_msg = 'Plik 30mb.jpg jest za duży. Użyj pliku o wielkości do 20MB'
        self.assertEqual(v.exception.message, exp_msg)


class TestAcceptedExtension(TestCase):
    def test_extension_gif(self):
        '''gif is not in settings.ALLOWED_EXTENSIONS - should raise ValidationError'''
        t_f = tempfile.NamedTemporaryFile()
        t_f.flush()
        t_f.name = 'incorrect.gif'
        f = File(t_f)
        self.assertRaises(ValidationError, accepted_extensions, f)

        with self.assertRaises(ValidationError) as v:
            accepted_extensions(f)

        exp_msg = 'Plik incorrect.gif jest niedowolony. Dozwolone pliki to: .jpg, .jpeg, .png'
        self.assertEqual(v.exception.message, exp_msg)

    def test_extension_jpg(self):
        '''should pass'''
        t_f = tempfile.NamedTemporaryFile()
        t_f.flush()
        t_f.name = 'correct.jpg'
        f = File(t_f)

        # should pass with no errors
        self.assertIsNone(accepted_extensions(f))