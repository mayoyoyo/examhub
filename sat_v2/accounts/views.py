from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Student
from .forms import StudentRegistrationForm

class StudentRegistrationView(CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return response

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {
        'student': request.user
    })
