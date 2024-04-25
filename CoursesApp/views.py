from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, StudentAnswer, StudentRating
from .forms import *
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Замените 'home' на URL вашей главной страницы
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Замените 'home' на URL вашей главной страницы
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('home')

def home(request):
    popular_courses = Course.objects.all()[:5]
    return render(request, 'home.html', {'popular_courses': popular_courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course)
    return render(request, 'course_detail.html', {'course': course, 'lessons': lessons})

@login_required
def my_courses(request):
    user = request.user
    if user.user_type == 'student':
        courses = Course.objects.filter(student=user)
        return render(request, 'my_courses.html', {'courses': courses})
    else:
        return redirect('home')

@login_required
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

@login_required
def submit_answer(request, lesson_id):
    if request.method == 'POST':
        user = request.user
        lesson = Lesson.objects.get(id=lesson_id)
        answer_file = request.FILES['answer']
        StudentAnswer.objects.create(student=user, lesson=lesson, answer_file=answer_file)
        return redirect('lesson_detail', lesson_id=lesson_id)
    else:
        return redirect('home')

@login_required
def rate_answers(request):
    if request.user.user_type == 'teacher':
        if request.method == 'POST':
            lesson_id = request.POST.get('lesson_id')
            lesson = Lesson.objects.get(id=lesson_id)
            if lesson.course.teacher != request.user:
                return redirect('home')

            # Получаем данные из POST-запроса
            answer_id = request.POST.get('answer_id')
            score = int(request.POST.get('score'))

            # Находим ответ студента и выставляем баллы
            student_answer = StudentAnswer.objects.get(id=answer_id)
            student_answer.score = score
            student_answer.save()

            # Рассчитываем общий балл ученика и обновляем его рейтинг
            student = student_answer.student
            total_score = StudentAnswer.objects.filter(student=student).aggregate(total_score=models.Sum('score'))['total_score']
            student_rating, created = StudentRating.objects.get_or_create(student=student)
            student_rating.score = total_score
            student_rating.save()
            pass
        else:
            user = request.user
            courses_taught = Course.objects.filter(teacher=user)
            student_answers = StudentAnswer.objects.filter(lesson__course__in=courses_taught)
            return render(request, 'rate_answers.html', {'student_answers': student_answers})
    else:
        return redirect('home')

def student_ranking(request):
    top_students = StudentRating.objects.order_by('-score')[:50]
    return render(request, 'student_ranking.html', {'top_students': top_students})
