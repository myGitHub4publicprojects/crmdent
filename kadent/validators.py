from django.core.exceptions import ValidationError
from django.conf import settings

# unused in this version
def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError('This seems to be empty file. Use a file with size over 1kb')
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError('This file is too large. Use a file with size under 20MB')

# unused in this version
def accepted_extensions():
    pass

def validate_extension(file):
    ext = file.name.split('.')[-1]
    if ext.lower() in settings.ACCEPTED_EXTENSIONS:
        return True
    return False


def validate_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        return  '''Próbujesz dodać plik który jest zbyt mały: {0}. 
        Użyj pliku o wielkości powyżej {1} kb'''.format(
            file.name, str(int(settings.MIN_UPLOAD_SIZE/1024))
        )
    if file.size > settings.MAX_UPLOAD_SIZE:
        return '''Próbujesz dodać plik który jest zbyt duży: {0}. 
        Użyj pliku o wielkości poniżej {1} MB'''.format(
            file.name, str(settings.MAX_UPLOAD_SIZE/(1024*1024))
        )
    return True
