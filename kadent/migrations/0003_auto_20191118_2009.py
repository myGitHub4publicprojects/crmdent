# Generated by Django 2.2.6 on 2019-11-18 20:09

from django.db import migrations, models
import kadent.validators


class Migration(migrations.Migration):

    dependencies = [
        ('kadent', '0002_auto_20191022_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='documents/', validators=[kadent.validators.accepted_size, kadent.validators.accepted_extensions]),
        ),
    ]