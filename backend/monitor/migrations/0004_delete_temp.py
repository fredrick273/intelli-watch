# Generated by Django 4.1.7 on 2023-09-15 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_systemdatainstance_installed_softwares'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Temp',
        ),
    ]
