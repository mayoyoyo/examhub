from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('student/register/', views.StudentRegistrationView.as_view(), name='student_register'),
    path('teacher/register/', views.TeacherRegistrationView.as_view(), name='teacher_register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(
        form_class=EmailAuthenticationForm,
        redirect_authenticated_user=True,
        template_name='registration/login.html'
    ), name='login'),
    path('academy/login/', views.AcademyLoginView.as_view(), name='academy_login'),
    path('logout/', views.logout_view, name='logout'),  # Updated to use custom logout view
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]