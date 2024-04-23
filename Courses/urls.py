from django.urls import path

from django.contrib import admin
from CoursesApp.views import home, course_list, course_detail, my_courses, lesson_detail, submit_answer, rate_answers, student_ranking

urlpatterns = [
    path('', home, name='home'),
    path('/admin', admin.site.urls),
    path('courses/', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('my_courses/', my_courses, name='my_courses'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('submit_answer/<int:lesson_id>/', submit_answer, name='submit_answer'),
    path('rate_answers/', rate_answers, name='rate_answers'),
    path('student_ranking/', student_ranking, name='student_ranking'),
]
