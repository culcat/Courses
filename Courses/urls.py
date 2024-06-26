from django.conf.urls.static import static
from django.urls import path

from django.contrib import admin

from Courses import settings
from CoursesApp.views import *

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',register,name='register'),
    path('courses/', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('my_courses/', my_courses, name='my_courses'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('submit_answer/<int:lesson_id>/', submit_answer, name='submit_answer'),
    path('rate_answers/', rate_answers, name='rate_answers'),
    path('student_ranking/', student_ranking, name='student_ranking'),
    path('profile/', user_profile, name='profile'),
    path('evaluate_course/<int:lesson_id>/', evaluate_student_answers, name='evaluate_course'),
    path('evaluate_answers/<int:answer_id>/', evaluate_answer, name='evaluate_answer'),
    path('create_course/', create_course, name='create_course'),
    path('create_lesson/<int:course_id>/', create_lesson, name='create_lesson'),
    path('complited_courses/<int:course_id>/', complete_course, name='complete_course'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)