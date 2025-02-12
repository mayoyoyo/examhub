from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.forms import modelformset_factory
from django.db.models import Avg, Max

from .models import Exam, ReadingPassage, Question, Choice, StudentExam, StudentAnswer
from .forms import ExamForm, PassageQuestionForm
from accounts.models import Student, Academy, User

class AcademyRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_academy

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_student

# Academy Views
class ExamListView(AcademyRequiredMixin, ListView):
    model = Exam
    template_name = 'exams/exam_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        academy = Academy.objects.get(id=self.request.user.id)
        return Exam.objects.filter(academy=academy)

class ExamCreateView(AcademyRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exams/exam_form.html'
    
    def form_valid(self, form):
        academy = Academy.objects.get(id=self.request.user.id)
        form.instance.academy = academy
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('exam_detail', kwargs={'pk': self.object.pk})

class ExamDetailView(AcademyRequiredMixin, DetailView):
    model = Exam
    template_name = 'exams/exam_detail.html'
    context_object_name = 'exam'

    def get_queryset(self):
        academy = Academy.objects.get(id=self.request.user.id)
        return Exam.objects.filter(academy=academy)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        academy = Academy.objects.get(id=self.request.user.id)
        students = Student.objects.filter(academy_profile=academy)
        
        # Get all student attempts for this exam
        attempts = StudentExam.objects.filter(exam=self.object)
        
        # Create a dict of student data including exam attempts
        student_data = []
        for student in students:
            student_attempts = attempts.filter(student=student)
            completed_attempts = student_attempts.filter(status='completed')
            
            data = {
                'student': student,
                'total_attempts': student_attempts.count(),
                'completed_attempts': completed_attempts.count(),
                'average_score': completed_attempts.aggregate(Avg('score'))['score__avg'] or 0,
                'highest_score': completed_attempts.aggregate(Max('score'))['score__max'] or 0,
                'latest_attempt': student_attempts.order_by('-completed_at').first()
            }
            student_data.append(data)
            
        context['students'] = students
        context['student_data'] = student_data
        return context

class QuestionCreateView(AcademyRequiredMixin, View):
    template_name = 'exams/passage_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        academy = Academy.objects.get(id=self.request.user.id)
        self.exam = get_object_or_404(Exam, pk=self.kwargs['exam_pk'], academy=academy)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        section = request.GET.get('section')
        if not section or section not in ['1', '2']:
            messages.error(request, 'Invalid section specified.')
            return redirect('exam_detail', pk=self.exam.pk)
            
        return render(request, self.template_name, {
            'form': PassageQuestionForm(),
            'exam': self.exam,
            'section': section
        })
    
    def post(self, request, *args, **kwargs):
        section = request.GET.get('section')
        if not section or section not in ['1', '2']:
            messages.error(request, 'Invalid section specified.')
            return redirect('exam_detail', pk=self.exam.pk)
            
        form = PassageQuestionForm(request.POST)
        if form.is_valid():
            try:
                passage = form.save(self.exam, int(section))
                messages.success(request, 'Question added successfully.')
                return redirect('exam_detail', pk=self.exam.pk)
            except ValueError as e:
                messages.error(request, str(e))
        return render(request, self.template_name, {
            'form': form,
            'exam': self.exam
        })

class QuestionDetailView(AcademyRequiredMixin, DetailView):
    model = ReadingPassage
    template_name = 'exams/passage_detail.html'
    context_object_name = 'passage'

    def get_queryset(self):
        academy = Academy.objects.get(id=self.request.user.id)
        return ReadingPassage.objects.filter(exam__academy=academy)

class AssignExamView(AcademyRequiredMixin, View):
    def post(self, request, pk):
        academy = Academy.objects.get(id=self.request.user.id)
        exam = get_object_or_404(Exam, pk=pk, academy=academy)
        student_id = request.POST.get('student_id')
        student = get_object_or_404(Student, pk=student_id, academy_profile=academy)
        
        # Check if student already has this exam
        if StudentExam.objects.filter(student=student, exam=exam).exists():
            messages.error(request, 'This exam has already been assigned to this student.')
            return redirect('exam_detail', pk=pk)
        
        StudentExam.objects.create(student=student, exam=exam)
        messages.success(request, f'Exam assigned to {student}')
        return redirect('exam_detail', pk=pk)

# Student Views
class StudentExamListView(StudentRequiredMixin, ListView):
    model = StudentExam
    template_name = 'exams/student_exam_list.html'
    context_object_name = 'student_exams'

    def get_queryset(self):
        return StudentExam.objects.filter(student=self.request.user)

class StartExamView(StudentRequiredMixin, View):
    def post(self, request, pk):
        student_exam = get_object_or_404(
            StudentExam,
            pk=pk,
            student=request.user,
            status='not_started'
        )
        
        student_exam.status = 'in_progress'
        student_exam.started_at = timezone.now()
        student_exam.save()
        
        return redirect('take_exam', pk=pk)

class TakeExamView(StudentRequiredMixin, DetailView):
    model = StudentExam
    template_name = 'exams/take_exam.html'
    context_object_name = 'student_exam'

    def get_queryset(self):
        return StudentExam.objects.filter(
            student=self.request.user,
            status='in_progress'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_remaining'] = self.get_time_remaining()
        return context

    def get_time_remaining(self):
        student_exam = self.get_object()
        elapsed = timezone.now() - student_exam.started_at
        total_seconds = student_exam.exam.time_limit * 60
        remaining = total_seconds - elapsed.total_seconds()
        return max(0, int(remaining))

class SubmitAnswerView(StudentRequiredMixin, View):
    def post(self, request, exam_pk):
        student_exam = get_object_or_404(
            StudentExam,
            pk=exam_pk,
            student=request.user,
            status='in_progress'
        )
        
        question_id = request.POST.get('question_id')
        choice_id = request.POST.get('choice_id')
        
        if not all([question_id, choice_id]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        question = get_object_or_404(Question, pk=question_id)
        choice = get_object_or_404(Choice, pk=choice_id, question=question)
        
        StudentAnswer.objects.update_or_create(
            student_exam=student_exam,
            question=question,
            defaults={'selected_choice': choice}
        )
        
        return JsonResponse({'success': True})

class SubmitExamView(StudentRequiredMixin, View):
    @transaction.atomic
    def post(self, request, pk):
        try:
            student_exam = StudentExam.objects.get(pk=pk)
            
            # Check if exam exists but doesn't belong to user
            if student_exam.student != request.user:
                messages.error(request, 'This exam does not belong to you.')
                return redirect('student_exam_list')
            
            # Check if exam exists but isn't in progress
            if student_exam.status != 'in_progress':
                messages.error(request, f'This exam cannot be submitted because its status is "{student_exam.status}".')
                if student_exam.status == 'completed':
                    return redirect('exam_results', pk=pk)
                return redirect('student_exam_list')
                
        except StudentExam.DoesNotExist:
            messages.error(request, 'The specified exam was not found.')
            return redirect('student_exam_list')
        
        # Calculate scores
        with transaction.atomic():
            # First, mark all answers as correct/incorrect
            for answer in student_exam.answers.all():
                answer.is_correct = answer.selected_choice.is_correct
                answer.save()

            # Then calculate totals
            answers = student_exam.answers.all()
            total_correct = answers.filter(is_correct=True).count()
            section1_correct = answers.filter(
                is_correct=True,
                question__passage__section=1
            ).count()
            section2_correct = answers.filter(
                is_correct=True,
                question__passage__section=2
            ).count()
            
            # Update student exam
            student_exam.status = 'completed'
            student_exam.completed_at = timezone.now()
            student_exam.score = total_correct
            student_exam.section1_score = section1_correct
            student_exam.section2_score = section2_correct
            student_exam.save()
        
        # Update student statistics
        student = Student.objects.get(id=request.user.id)
        student.total_tests_taken += 1
        if student.average_score is None:
            student.average_score = total_correct
        else:
            student.average_score = (
                (student.average_score * (student.total_tests_taken - 1) + total_correct)
                / student.total_tests_taken
            )
        student.save()
        
        return redirect('exam_results', pk=pk)

class ExamResultsView(StudentRequiredMixin, DetailView):
    model = StudentExam
    template_name = 'exams/exam_results.html'
    context_object_name = 'student_exam'

    def get_queryset(self):
        return StudentExam.objects.filter(
            student=self.request.user,
            status='completed'
        )

# API Views for exam timer
class ResetTimerView(StudentRequiredMixin, View):
    def post(self, request, pk):
        student_exam = get_object_or_404(
            StudentExam,
            pk=pk,
            student=request.user,
            status='in_progress'
        )
        
        # Reset the timer by updating started_at
        student_exam.started_at = timezone.now()
        student_exam.save()
        
        return JsonResponse({'success': True})

class CheckTimeRemainingView(StudentRequiredMixin, View):
    def get(self, request, pk):
        student_exam = get_object_or_404(
            StudentExam,
            pk=pk,
            student=request.user,
            status='in_progress'
        )
        
        elapsed = timezone.now() - student_exam.started_at
        total_seconds = student_exam.exam.time_limit * 60
        remaining = total_seconds - elapsed.total_seconds()
        
        if remaining <= 0:
            # Auto-submit if time is up
            return JsonResponse({
                'time_remaining': 0,
                'should_submit': True
            })
        
        return JsonResponse({
            'time_remaining': int(remaining),
            'should_submit': False
        })
