from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from .models import Student, Teacher, Academy
from .forms import StudentRegistrationForm, TeacherRegistrationForm, EmailAuthenticationForm

class StudentRegistrationView(CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'registration/student_register.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        # Log the user in after registration
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return redirect(self.success_url)

class TeacherRegistrationView(CreateView):
    model = Teacher
    form_class = TeacherRegistrationForm
    template_name = 'registration/teacher_register.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = form.save()
        # Log the user in after registration
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return redirect(self.success_url)

class AcademyLoginView(LoginView):
    template_name = 'registration/academy_login.html'
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_academy:
            raise PermissionDenied("This login is for academy administrators only.")
        return super().form_valid(form)

@login_required
def profile(request):
    context = {
        'user': request.user,
        'user_type': 'student' if request.user.is_student else 'teacher' if request.user.is_teacher else 'academy'
    }
    
    if request.user.is_student:
        student = Student.objects.get(id=request.user.id)
        context.update({
            'grade_level': student.grade_level,
            'total_tests_taken': student.total_tests_taken,
            'average_score': student.average_score,
            'academy_profile': student.academy_profile
        })
    elif request.user.is_teacher:
        teacher = Teacher.objects.get(id=request.user.id)
        context.update({
            'academy_profile': teacher.academy_profile
        })
    elif request.user.is_academy:
        academy = Academy.objects.get(id=request.user.id)
        context.update({
            'secret_code': academy.secret_code
        })
    
    return render(request, 'registration/profile.html', context)

def logout_view(request):
    """Custom logout view that supports GET requests"""
    logout(request)
    return redirect('accounts:login')
