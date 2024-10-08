# Generated by Django 5.1 on 2024-09-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_platform', '0008_alter_course_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='course',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
