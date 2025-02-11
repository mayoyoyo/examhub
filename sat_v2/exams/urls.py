from django.urls import path
from . import views

urlpatterns = [
    # Academy URLs
    path('exams/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('exams/<int:pk>/assign/', views.AssignExamView.as_view(), name='assign_exam'),
    
    # Question management
    path('exams/<int:exam_pk>/questions/add/',
         views.QuestionCreateView.as_view(), name='passage_create'),
    path('exams/<int:exam_pk>/questions/<int:pk>/',
         views.PassageDetailView.as_view(), name='passage_detail'),
    
    # Student URLs
    path('my-exams/', views.StudentExamListView.as_view(), name='student_exam_list'),
    path('my-exams/<int:pk>/start/', views.StartExamView.as_view(), name='start_exam'),
    path('my-exams/<int:pk>/take/', views.TakeExamView.as_view(), name='take_exam'),
    path('my-exams/<int:pk>/submit/', views.SubmitExamView.as_view(), name='submit_exam'),
    path('my-exams/<int:pk>/results/', views.ExamResultsView.as_view(), name='exam_results'),
    
    # API endpoints
    path('my-exams/<int:exam_pk>/submit-answer/', 
         views.SubmitAnswerView.as_view(), name='submit_answer'),
    path('my-exams/<int:pk>/check-time/', 
         views.CheckTimeRemainingView.as_view(), name='check_time'),
]