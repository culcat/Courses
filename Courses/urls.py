from django.urls import path

from django.contrib import admin
from CoursesApp.views import *

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',register_user,name='register'),
    path('courses/', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('my_courses/', my_courses, name='my_courses'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('submit_answer/<int:lesson_id>/', submit_answer, name='submit_answer'),
    path('rate_answers/', rate_answers, name='rate_answers'),
    path('student_ranking/', student_ranking, name='student_ranking'),
]
