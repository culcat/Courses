# Generated by Django 5.0.4 on 2024-04-26 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0006_course_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentrating',
            name='position',
        ),
    ]
