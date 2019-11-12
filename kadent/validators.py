from django.core.exceptions import ValidationError
from django.conf import settings

def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError(
            'Plik {0} jest pusty. Użyj pliku większego od 1kb'.format(file.name))
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            'Plik {0} jest za duży. Użyj pliku o wielkości do 20MB'.format(file.name))


def accepted_extensions():
    pass
