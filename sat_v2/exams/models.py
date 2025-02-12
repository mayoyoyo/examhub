from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import Academy, Student

class Exam(models.Model):
    """Model for SAT practice exams"""
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='created_exams')
    is_active = models.BooleanField(default=True)
    time_limit = models.IntegerField(default=32, help_text='Time limit in minutes')
    
    def __str__(self):
        return f"{self.title} - {self.academy.first_name}"

class ReadingPassage(models.Model):
    """Model for reading passages/blurbs"""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='passages')
    text = models.TextField()
    section = models.IntegerField(choices=[(1, 'Section 1'), (2, 'Section 2')])
    
    class Meta:
        ordering = ['section']
    
    def __str__(self):
        return f"Section {self.section} - {self.exam.title}"

class Question(models.Model):
    """Model for multiple choice questions"""
    passage = models.OneToOneField(ReadingPassage, on_delete=models.CASCADE, related_name='question')
    text = models.TextField()
    
    def __str__(self):
        return f"Question for {self.passage}"

class Choice(models.Model):
    """Model for answer choices"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Choice for {self.question}"

class StudentExam(models.Model):
    """Model for tracking student exam attempts"""
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_attempts')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_attempts')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(null=True, blank=True)
    section1_score = models.IntegerField(null=True, blank=True)
    section2_score = models.IntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'exam']
    
    def __str__(self):
        return f"{self.student} - {self.exam}"

class StudentAnswer(models.Model):
    """Model for storing student answers"""
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student_exam', 'question']
    
    def save(self, *args, **kwargs):
        self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Answer by {self.student_exam.student} for {self.question}"
