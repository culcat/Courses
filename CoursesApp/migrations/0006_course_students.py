# Generated by Django 5.0.4 on 2024-04-26 19:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0005_lesson_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(blank=True, related_name='courses_enrolled', to=settings.AUTH_USER_MODEL),
        ),
    ]
