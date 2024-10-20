# tasks/forms.py
from django import forms
from .models import Task
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'due_date', 'category', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Task Title', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email' , 'password1' , 'password2']