from django.contrib import admin

from CoursesApp.models import Course,EducationalOrganization,Lesson

admin.site.register(Course)
admin.site.register(EducationalOrganization)
admin.site.register(Lesson)