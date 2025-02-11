from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Teacher, Academy

class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    academy_code = forms.CharField(required=True, help_text="Enter your academy's secret code")
    
    class Meta(UserCreationForm.Meta):
        model = Student
        fields = ('email', 'first_name', 'last_name', 'grade_level')

    def clean_academy_code(self):
        code = self.cleaned_data.get('academy_code')
        try:
            academy = Academy.objects.get(secret_code=code)
            self.academy = academy
            return code
        except Academy.DoesNotExist:
            raise ValidationError("Invalid academy code. Please check with your academy administrator.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.academy_profile = self.academy
        if commit:
            user.save()
        return user

class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    academy_code = forms.CharField(required=True, help_text="Enter your academy's secret code")
    
    class Meta(UserCreationForm.Meta):
        model = Teacher
        fields = ('email', 'first_name', 'last_name')

    def clean_academy_code(self):
        code = self.cleaned_data.get('academy_code')
        try:
            academy = Academy.objects.get(secret_code=code)
            self.academy = academy
            return code
        except Academy.DoesNotExist:
            raise ValidationError("Invalid academy code. Please check with your academy administrator.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.academy_profile = self.academy
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}), label='Email')

    def clean(self):
        # Get the email value from the username field
        if self.cleaned_data.get('username'):
            self.cleaned_data['email'] = self.cleaned_data.get('username')
        return super().clean()