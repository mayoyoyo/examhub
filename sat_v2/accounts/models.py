from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    """Base user model for all user types"""
    username = None  # Remove username field
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=150)
    last_name = models.CharField('last name', max_length=150)
    
    # User type flags
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_academy = models.BooleanField(default=False)
    
    # Academy relationship (null for academy users)
    academy_profile = models.ForeignKey(
        'Academy',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='members'
    )
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        if self.is_academy:
            return self.first_name  # For academy users, first_name stores the name
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Academy(User):
    """Model for academy administrators"""
    secret_code = models.CharField(max_length=20, unique=True)
    
    def save(self, *args, **kwargs):
        self.is_academy = True
        self.is_staff = True  # Academies get staff access
        self.academy_profile = None  # Academy users don't belong to an academy
        self.last_name = ''  # Empty last_name for academies
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.first_name  # first_name stores the academy name
    
    class Meta:
        verbose_name = 'Academy'
        verbose_name_plural = 'Academies'

class Student(User):
    """Model for student users"""
    grade_level = models.IntegerField(null=True, blank=True)
    total_tests_taken = models.IntegerField(default=0)
    average_score = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.is_student = True
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

class Teacher(User):
    """Model for teacher users"""
    def save(self, *args, **kwargs):
        self.is_teacher = True
        self.is_staff = True  # Teachers get staff access
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'