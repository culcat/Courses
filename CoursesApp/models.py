from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from django.utils.translation import gettext as _

class EducationalOrganization(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Админ'),
        ('teacher', 'Преподаватель'),
        ('student', 'Ученик'),
    ]
    organization = models.ForeignKey('EducationalOrganization', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_users')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users',
        help_text=_(
            'Specific permissions for this user.'
            'Be careful when assigning the "unlimited" permission.'
        ),
    )





class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses_taught')
    organization = models.ForeignKey(EducationalOrganization, on_delete=models.CASCADE, related_name='courses')
    max_score = models.IntegerField(default=10)
    students = models.ManyToManyField(CustomUser, related_name='courses_enrolled', blank=True)
    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    material = models.TextField()
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    def __str__(self):
        return self.title

class StudentAnswer(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='answers')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='answers')
    answer_file = models.FileField(upload_to='answers/')
    score = models.IntegerField(default=0,null=False,blank=False)



class StudentRating(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='rating',null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
