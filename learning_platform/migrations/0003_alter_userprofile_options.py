# Generated by Django 5.1 on 2024-08-18 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_platform', '0002_alter_userprofile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': [('change_own_userprofile', 'Can change own user profile'), ('view_own_userprofile', 'Can view own user profile'), ('delete_own_userprofile', 'Can delete own user profile')]},
        ),
    ]
