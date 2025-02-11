from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student, Teacher, Academy

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_student', 'is_teacher', 'is_academy')
    list_filter = ('is_student', 'is_teacher', 'is_academy', 'is_staff', 'is_superuser')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')

class AcademyAdmin(CustomUserAdmin):
    list_display = ('email', 'first_name', 'secret_code')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Academy Info', {'fields': ('first_name', 'secret_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'secret_code', 'password1', 'password2'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if form.base_fields.get('first_name'):
            form.base_fields['first_name'].label = 'Academy Name'
        return form

class StudentAdmin(CustomUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'academy_profile', 'grade_level')
    list_filter = ('academy_profile', 'grade_level')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'grade_level')}),
        ('Academy', {'fields': ('academy_profile',)}),
        ('Test Information', {'fields': ('total_tests_taken', 'average_score')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'academy_profile', 'grade_level', 'password1', 'password2'),
        }),
    )

class TeacherAdmin(CustomUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'academy_profile')
    list_filter = ('academy_profile',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Academy', {'fields': ('academy_profile',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'academy_profile', 'password1', 'password2'),
        }),
    )

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Academy, AcademyAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
