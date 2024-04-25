from django.contrib import admin

from CoursesApp.models import Course, EducationalOrganization, Lesson, CustomUser

admin.site.register(Course)
admin.site.register(EducationalOrganization)
admin.site.register(Lesson)
admin.site.register(CustomUser)