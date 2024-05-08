from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, StudentAnswer, StudentRating
from .forms import *
from django.contrib import messages
from django.db import models
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
                return redirect('home')
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
    is_student = course.students.filter(pk=request.user.pk).exists()
    return render(request, 'course_detail.html', {'course': course, 'lessons': lessons,"is_student":is_student})
def complete_course(request, course_id):
    course = Course.objects.get(pk=course_id)

    if request.user.is_authenticated and course.students.filter(pk=request.user.pk).exists():
        course.students.remove(request.user)
        messages.success(request, "Вы успешно завершили курс!")
        return redirect('course_detail', course_id=course.id)
    else:
        messages.error(request, "Вы не можете завершить этот курс.")
        return redirect('courses_list')
@login_required
def my_courses(request):
    user = request.user

    if user.user_type == 'student':
        # Check if student is enrolled in any courses
        enrolled_courses = Course.objects.filter(students=user)
        if enrolled_courses.exists():
            # Display enrolled courses
            return render(request, 'my_courses.html', {'courses': enrolled_courses})
        else:
            if request.method == 'POST':
                course_id = request.POST.get('course_id')
                course = get_object_or_404(Course, pk=course_id)
                course.students.add(user)  # Enroll student in the course
                return redirect('my_courses')
            else:
                # Display available courses for enrollment
                available_courses = Course.objects.exclude(students=user)
                return render(request, 'choose_course.html', {'courses': available_courses})

    elif user.user_type == 'teacher':
        # Get courses taught by this teacher (assuming a 'teachers' field in Course)
        taught_courses = Course.objects.filter(teacher=user)
        return render(request, 'my_courses.html', {'courses': taught_courses})

    else:
        # Handle invalid user types (optional, could raise an exception)
        return redirect('home')
def create_course(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.user, request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.save()
            return redirect('my_courses')
    else:
        form = CreateCourseForm(request.user)
    return render(request, 'create_course.html', {'form': form})
def lesson_detail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return render(request, 'lesson_detail.html', {'lesson': lesson})

def submit_answer(request, lesson_id):
    if request.method == 'POST':
        user = request.user
        lesson = Lesson.objects.get(id=lesson_id)
        answer_file = request.FILES['answer_file']  # use 'answer_file' key
        StudentAnswer.objects.create(student=user, lesson=lesson, answer_file=answer_file)
        return redirect('lesson_detail', lesson_id=lesson_id)
    else:
        return redirect('home')


def rate_answers(request, answer_id):
    answer = get_object_or_404(StudentAnswer, pk=answer_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']
            position = form.cleaned_data['position']
            # Проверка, существует ли уже запись рейтинга для студента
            rating, created = StudentRating.objects.get_or_create(student=answer.student)
            rating.score = score
            rating.position = position
            rating.save()
            return HttpResponseRedirect('/success/')  # Redirect to success page
    else:
        form = RatingForm()
    return render(request, 'rate_student.html', {'form': form, 'answer': answer})

def student_ranking(request):
    top_students = StudentRating.objects.order_by('-score')[:50]
    return render(request, 'student_ranking.html', {'top_students': top_students})
def user_profile(request):
    studentRating = StudentRating.objects.get(student=request.user)
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'rating': studentRating.score,
        'user': request.user,
    }
    return render(request, 'user_profile.html', context)
def create_lesson(request, course_id):

    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = lessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = lessonForm()
    return render(request, 'create_lesson.html', {'form': form, 'course': course})
def evaluate_student_answers(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)


    student_answers = StudentAnswer.objects.filter(lesson = lesson_id)


    context = {
        'lesson':lesson,
        'student_answers': student_answers,
        'lesson_id': lesson_id,  # Pass lesson ID for potential filtering in the template
    }

    return render(request, 'evaluate_answers.html', context)



def evaluate_answer(request, answer_id):
    answer = get_object_or_404(StudentAnswer, pk=answer_id)
    raiting = get_object_or_404(StudentRating, student=answer.student)

    if request.method == 'POST':
        score = request.POST.get('score')
        answer.score = score
        answer.save()
        raiting.score = int(score) + int(raiting.score)
        raiting.save()
        student = answer.student

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'error.html')


