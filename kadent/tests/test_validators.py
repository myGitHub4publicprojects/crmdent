import tempfile
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core.files import File

from kadent.validators import accepted_size


class TestAcceptedSize(TestCase):
    def test_size_0kb(self):
        '''size is below 1kb - should raise ValidationError'''
        t_f = tempfile.NamedTemporaryFile(suffix=".jpg")
        t_f.flush()
        t_f.size = 1
        
        f = File(t_f)
        self.assertRaises(ValidationError, accepted_size, f)

        with self.assertRaises(ValidationError) as v:
            accepted_size(f)
        
        exp_msg = 'This seems to be empty file. Use a file with size over 1kb'
        self.assertEqual(v.exception.message, exp_msg)

    def test_size_5mb(self):
        '''file size is 5MB, should pass with no errors'''
        t_f = tempfile.NamedTemporaryFile(suffix=".jpg")
        t_f.flush()
        t_f.size = 5*1024*1024
        f = File(t_f)

        # should pass with no errors
        self.assertIsNone(accepted_size(f))

    def test_size_30mb(self):
        '''file size is 30MB, should raise ValidationError'''
        t_f = tempfile.NamedTemporaryFile(suffix=".jpg")
        t_f.flush()
        t_f.size = 30*1024*1024
        f = File(t_f)
        self.assertRaises(ValidationError, accepted_size, f)

        with self.assertRaises(ValidationError) as v:
            accepted_size(f)

        exp_msg = 'This file is too large. Use a file with size under 20MB'
        self.assertEqual(v.exception.message, exp_msg)