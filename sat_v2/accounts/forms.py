from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Student

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ('email', 'first_name', 'last_name', 'grade_level')