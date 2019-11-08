from django.core.exceptions import ValidationError
from django.conf import settings

def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError('''Próbujesz dodać plik który jest zbyt mały: {0}. 
        Użyj pliku o wielkości powyżej {1} kb'''.format(
            file.name, str(int(settings.MIN_UPLOAD_SIZE/1024))
        ))
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('''Próbujesz dodać plik który jest zbyt duży: {0}. 
        Użyj pliku o wielkości poniżej {1} MB'''.format(
            file.name, str(settings.MAX_UPLOAD_SIZE/(1024*1024))
        ))

def accepted_extensions():
    pass