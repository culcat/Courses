from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Lesson, StudentAnswer, StudentRating
from .forms import *
from django.db import models
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
        # Check if the student is already enrolled in a course
        enrolled_courses = Course.objects.filter(students=user)
        if enrolled_courses.exists():
            # If the student is already enrolled, display their enrolled courses
            return render(request, 'my_courses.html', {'courses': enrolled_courses})
        else:
            if request.method == 'POST':
                course_id = request.POST.get('course_id')
                course = get_object_or_404(Course, pk=course_id)
                course.students.add(user)  # Enroll the student in the course
                return redirect('my_courses')
            else:
                # If the student is not enrolled, provide the option to choose a course
                available_courses = Course.objects.exclude(students=user)
                return render(request, 'choose_course.html', {'courses': available_courses})
    else:
        return redirect('home')


@login_required
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
    """
    Личный кабинет пользователя.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    context = {
        'user': request.user,
    }
    return render(request, 'user_profile.html', context)

def evaluate_student_answers(request, lesson_id):



    student_answers = StudentAnswer.objects.filter(lesson = lesson_id)


    context = {
        'student_answers': student_answers,
        'lesson_id': lesson_id,  # Pass lesson ID for potential filtering in the template
    }

    return render(request, 'evaluate_answers.html', context)



def evaluate_answer(request, answer_id):
    answer = get_object_or_404(StudentAnswer, pk=answer_id)

    if request.method == 'POST':
        score = request.POST.get('score')

        # Validate score
        try:
            score = int(score)
            if score < 0 or score > answer.lesson.course.max_score:
                raise ValueError("Score must be between 0 and the maximum course score.")
        except ValueError:
            context = {'error_message': "Invalid score. Please enter a number between 0 and the maximum course score."}
            return render(request, 'error.html', context)

        # Update answer score
        answer.score = score
        answer.save()  # Save the updated answer score

        # Calculate and update StudentRating score
        student = answer.student
        student_rating, created = StudentRating.objects.get_or_create(student=student)

        # Update score if the StudentRating object exists
        if not created:
            student_rating.score = calculate_overall_score(student)
            student_rating.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, 'error.html')



def calculate_overall_score(student):
    total_score = 0
    num_answers = 0
    student_answers = StudentAnswer.objects.filter(student=student)

    # Calculate total score from graded answers
    for answer in student_answers:
        if answer.score is not None:  # Only consider graded answers
            total_score += answer.score
            num_answers += 1

    # Calculate average score if there are graded answers
    if num_answers > 0:
        return total_score / num_answers
    else:
        return 0  # Default score if no graded answers exist