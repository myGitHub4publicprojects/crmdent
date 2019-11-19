from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.conf import settings

def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError(
            'Plik {0} jest pusty. Użyj pliku większego od 1kb'.format(file.name))
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            'Plik {0} jest za duży. Użyj pliku o wielkości do 20MB'.format(file.name))


def accepted_extensions(file):

    f = file.name.split('.')
    extension = f[-1]
    if extension.lower() not in settings.ACCEPTED_EXTENSIONS:
        allowed_extensions_str = ['.' + i for i in settings.ACCEPTED_EXTENSIONS]
        allowed_extensions_str = ', '.join(allowed_extensions_str)
        raise ValidationError(
            'Plik {0} jest niedowolony. Dozwolone pliki to: {1}'.format(
                file.name, allowed_extensions_str)
    )

