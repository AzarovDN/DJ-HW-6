from django import forms
from django.core.exceptions import ValidationError


class AnswerForm(forms.Form):
    answer = forms.IntegerField(label='Введите число от 1 до 10', min_value=0, max_value=10)


