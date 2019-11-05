from django.core.exceptions import ValidationError
from django.conf import settings

def accepted_size(file):
    if file.size < settings.MIN_UPLOAD_SIZE:
        raise ValidationError(
            '{0} seems to be an empty file. Use a file with size over 1kb'.format(file.name))
    if file.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            '{0} file is too large. Use a file with size under 20MB'.format(file.name))


def accepted_extensions():
    pass
