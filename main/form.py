from django import forms
from .models import Question

class QuizForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions = questions
        self.correct_answers = {}  # Store correct answers here
        for i, question in enumerate(questions):
            choices = [('1', question.option1), ('2', question.option2)]
            if question.option3:
                choices.append(('3', question.option3))
            if question.option4:
                choices.append(('4', question.option4))

            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                label=question.text,
                choices=choices,
                widget=forms.RadioSelect,
                required=False
            )
            self.correct_answers[str(question.id)] = question.correct_answer  # Storing the correct answer

    def clean(self):
        cleaned_data = super().clean()
        score = 0
        self.user_answers = {}  # Store user's answers
        for question in self.questions:
            correct_answer = self.correct_answers[str(question.id)]
            user_answer = cleaned_data.get(f'question_{question.id}')
            self.user_answers[str(question.id)] = user_answer
            if user_answer == correct_answer:
                score += 1
        self.score = score
        return cleaned_data

    def get_score(self):
        return getattr(self, 'score', 0)

    def get_correct_answers(self):
        return self.correct_answers

    def get_user_answers(self):
        return getattr(self, 'user_answers', {})