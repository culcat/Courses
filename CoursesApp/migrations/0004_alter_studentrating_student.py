# Generated by Django 5.0.4 on 2024-04-25 21:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0003_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentrating',
            name='student',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL),
        ),
    ]
