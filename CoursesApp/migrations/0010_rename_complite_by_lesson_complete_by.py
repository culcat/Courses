# Generated by Django 5.0.4 on 2024-04-28 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0009_lesson_complite_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='complite_by',
            new_name='complete_by',
        ),
    ]
