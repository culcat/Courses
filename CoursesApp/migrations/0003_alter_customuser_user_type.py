# Generated by Django 5.0.4 on 2024-04-25 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoursesApp', '0002_customuser_organization_alter_customuser_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Админ'), ('teacher', 'Преподаватель'), ('student', 'Ученик')], max_length=20),
        ),
    ]
