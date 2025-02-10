from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student

class StudentAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'grade_level', 'total_tests_taken', 'average_score')
    list_filter = ('grade_level',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'grade_level')}),
        ('Test Information', {'fields': ('total_tests_taken', 'average_score')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'grade_level', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(Student, StudentAdmin)
