import re

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


def format_employer_name(value):
    cleaned = re.sub(r"[_-]+", " ", value or "")
    cleaned = " ".join(cleaned.split())
    if not cleaned:
        return ""
    return " ".join(word[:1].upper() + word[1:] for word in cleaned.split())


class Profile(models.Model):
    JOB_SEEKER = 'job_seeker'
    EMPLOYER = 'employer'
    ROLE_CHOICES = [
        (JOB_SEEKER, 'Job Seeker'),
        (EMPLOYER, 'Employer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=JOB_SEEKER)
    company_name = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    resume = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"

    @property
    def employer_name(self):
        return format_employer_name(self.company_name or self.user.username)

    @property
    def display_name(self):
        if self.role == self.EMPLOYER:
            return self.employer_name
        return self.user.username

    def is_job_seeker(self):
        return self.role == self.JOB_SEEKER

    def is_employer(self):
        return self.role == self.EMPLOYER

    def save(self, *args, **kwargs):
        if self.role == self.EMPLOYER and self.company_name:
            self.company_name = format_employer_name(self.company_name)
        super().save(*args, **kwargs)


class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    @property
    def employer_name(self):
        return self.employer.profile.employer_name


class Application(models.Model):
    STATUS_SUBMITTED = 'submitted'
    STATUS_REVIEWING = 'reviewing'
    STATUS_INTERVIEW = 'interview'
    STATUS_REJECTED = 'rejected'
    STATUS_HIRED = 'hired'

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, 'Submitted'),
        (STATUS_REVIEWING, 'Reviewing'),
        (STATUS_INTERVIEW, 'Interview'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_HIRED, 'Hired'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SUBMITTED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} -> {self.job.title}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.profile.display_name} to {self.receiver.profile.display_name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.profile.display_name}: {self.text}"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
