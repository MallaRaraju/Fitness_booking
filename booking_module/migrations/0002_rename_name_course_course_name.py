# Generated by Django 5.2.2 on 2025-06-10 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_module', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='name',
            new_name='course_name',
        ),
    ]
