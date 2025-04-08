from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Question
from .form import QuizForm

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page (e.g., user's dashboard)
            return redirect('Home')  # Replace 'dashboard' with your actual URL name
        else:
            # Display an error message to the user
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        # If it's a GET request, just render the login form
        return render(request, 'login.html')

def quiz_view(request):
    questions = Question.objects.all()
    if request.method == 'POST': #POST is used to submit the form
        # Check if the form is submitted with POST method
        form = QuizForm(questions, request.POST)
        if form.is_valid():
            score = form.get_score()
            total_questions = len(questions)
            correct_answers = form.get_correct_answers()
            user_answers = form.get_user_answers()
            results = [] #results list to store question details
            # Looping through each question and get the user's answer and correct answer
            for question in questions:
                question_id = str(question.id)
                user_answer_key = user_answers.get(question_id)
                user_answer_text = 'Not answered'
                correct_answer_text = ''

                # Get user's answer text
                if user_answer_key == '1':
                    user_answer_text = question.option1
                elif user_answer_key == '2':
                    user_answer_text = question.option2
                elif user_answer_key == '3' and question.option3:
                    user_answer_text = question.option3
                elif user_answer_key == '4' and question.option4:
                    user_answer_text = question.option4

                # Get correct answer text
                if correct_answers.get(question_id) == '1':
                    correct_answer_text = question.option1
                elif correct_answers.get(question_id) == '2':
                    correct_answer_text = question.option2
                elif correct_answers.get(question_id) == '3' and question.option3:
                    correct_answer_text = question.option3
                elif correct_answers.get(question_id) == '4' and question.option4:
                    correct_answer_text = question.option4

                results.append({
                    'question_text': question.text,
                    'correct_answer_text': correct_answer_text,
                    'user_answer_text': user_answer_text,
                    'is_correct': user_answer_key == correct_answers.get(question_id),
                })

            context = {
                'score': score,
                'total_questions': total_questions,
                'results': results,
            }
            return render(request, 'results.html', context)
    else:
        form = QuizForm(questions)
    context = {'form': form}
    return render(request, 'quiz.html', context)