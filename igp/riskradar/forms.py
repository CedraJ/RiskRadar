from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import UserProfile, Asset

class SignUpForm(UserCreationForm):
    SECURITY_QUESTION_CHOICES_1 = [
        ('birth_place', 'What is the name of the town where you were born?'),
        ('sibling_name', 'What is your oldest sibling\'s middle name?'),
        ('first_school', 'What is the name of the school you attended?')
    ]
    
    SECURITY_QUESTION_CHOICES_2 = [
        ('parents_city', 'In what city did your parents meet?'),
        ('first_car', 'What was the make and model of your first car?'),
        ('first_concert', 'What was the first concert you attended?')
    ]

    email = forms.EmailField(required=True, help_text="Enter a valid email address.")
    security_question_1 = forms.ChoiceField(choices=SECURITY_QUESTION_CHOICES_1, label="Security Question 1")
    security_answer_1 = forms.CharField(required=True, widget=forms.TextInput, label="Answer 1")
    security_question_2 = forms.ChoiceField(choices=SECURITY_QUESTION_CHOICES_2, label="Security Question 2")
    security_answer_2 = forms.CharField(required=True, widget=forms.TextInput, label="Answer 2")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'security_question_1', 'security_answer_1', 'security_question_2', 'security_answer_2')

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'owner', 'value', 'status', 'risk_level', 'priority', 'control_measures_effectiveness']
