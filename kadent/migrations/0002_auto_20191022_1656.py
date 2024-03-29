# Generated by Django 2.2.6 on 2019-10-22 16:56

import django.core.validators
from django.db import migrations, models
import kadent.validators


class Migration(migrations.Migration):

    dependencies = [
        ('kadent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='documents/', validators=[kadent.validators.accepted_size, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
        ),
    ]
