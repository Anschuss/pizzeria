# Generated by Django 3.1.7 on 2021-03-09 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='infopizzerie',
            old_name='adres',
            new_name='address',
        ),
    ]
