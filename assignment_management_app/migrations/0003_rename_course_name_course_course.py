# Generated by Django 5.1 on 2024-08-20 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_management_app', '0002_alter_user_course'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course_name',
            new_name='course',
        ),
    ]
