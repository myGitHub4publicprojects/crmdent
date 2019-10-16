from django.core.exceptions import ValidationError
from django.conf import settings

def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError('This seems to be empty file. Use a file with size over 1kb')
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('This file is too large. Use a file with size under 20MB')
