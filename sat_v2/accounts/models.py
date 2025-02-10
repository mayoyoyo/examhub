from django.contrib.auth.models import AbstractUser
from django.db import models

class Student(AbstractUser):
    """Custom user model for SAT test takers"""
    username = None  # Remove username field
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    grade_level = models.IntegerField(null=True, blank=True)
    
    # Add any additional fields needed for SAT testing
    total_tests_taken = models.IntegerField(default=0)
    average_score = models.FloatField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'