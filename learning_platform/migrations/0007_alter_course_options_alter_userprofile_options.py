# Generated by Django 5.1 on 2024-08-29 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_platform', '0006_alter_userprofile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'permissions': [('change_own_course', 'Can change own course'), ('delete_own_course', 'Can delete own course')]},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': [('change_own_userprofile', 'Can change own user profile'), ('delete_own_userprofile', 'Can delete own user profile')]},
        ),
    ]
