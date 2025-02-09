from django.contrib.auth.models import AbstractUser
from django.db import models

class Academy(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Academies"

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
        ACADEMY_ADMIN = 'ACADEMY_ADMIN', 'Academy Admin'
        STUDENT = 'STUDENT', 'Student'
    
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    academy = models.ForeignKey(
        Academy,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    grade = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"