from django.contrib import admin
from .models import Application, Job, Message, Notification, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'role', 'company_name', 'updated_at')
    search_fields = ('user__username', 'user__email', 'company_name', 'skills')

    @admin.display(ordering='user__username', description='User')
    def user_display(self, obj):
        return obj.display_name


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer_display', 'location', 'created_at', 'is_active')
    list_filter = ('is_active', 'location')
    search_fields = ('title', 'description', 'employer__username')

    @admin.display(ordering='employer__username', description='Employer')
    def employer_display(self, obj):
        return obj.employer_name


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('job__title', 'applicant__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_display', 'receiver_display', 'created_at', 'read')
    search_fields = ('sender__username', 'receiver__username', 'content')

    @admin.display(ordering='sender__username', description='Sender')
    def sender_display(self, obj):
        return obj.sender.profile.display_name

    @admin.display(ordering='receiver__username', description='Receiver')
    def receiver_display(self, obj):
        return obj.receiver.profile.display_name


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'text', 'created_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('user__username', 'text')

    @admin.display(ordering='user__username', description='User')
    def user_display(self, obj):
        return obj.user.profile.display_name
