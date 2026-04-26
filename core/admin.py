from django.contrib import admin
from .models import Application, Job, Message, Notification, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'company_name', 'updated_at')
    search_fields = ('user__username', 'user__email', 'company_name', 'skills')


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'created_at', 'is_active')
    list_filter = ('is_active', 'location')
    search_fields = ('title', 'description', 'employer__username')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('job__title', 'applicant__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at', 'read')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'text')
