# Generated by Django 5.2.1 on 2025-07-01 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='persona',
            old_name='contraseña',
            new_name='contrasena',
        ),
    ]
