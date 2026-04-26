from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ApplicationForm, JobForm, MessageForm, ProfileForm, SignUpForm, UserForm
from .models import Application, Job, Message, Notification, Profile


def home(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    jobs = Job.objects.filter(is_active=True).order_by('-created_at')

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    return render(request, 'core/home.html', {
        'jobs': jobs,
        'query': query,
        'location': location,
    })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


def logout_view(request):
    if request.method in ('GET', 'POST'):
        logout(request)
        return redirect('home')
    return HttpResponseForbidden('Logout not allowed.')


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == 'POST':
        action = request.POST.get('action')
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)

        if action == 'update_profile':
            password_form = PasswordChangeForm(request.user)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('profile_edit')
        else:
            password_form = PasswordChangeForm(request.user, request.POST)
            if action == 'change_password' and password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been changed.')
                return redirect('profile_edit')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'core/profile_form.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
    })


@login_required
def dashboard(request):
    profile = request.user.profile
    notifications = request.user.notifications.order_by('-created_at')[:5]

    if profile.role == Profile.EMPLOYER:
        jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
        applications = Application.objects.filter(job__employer=request.user).order_by('-created_at')
        return render(request, 'core/employer_dashboard.html', {
            'jobs': jobs,
            'applications': applications,
            'notifications': notifications,
        })

    applications = Application.objects.filter(applicant=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {
        'applications': applications,
        'notifications': notifications,
    })


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()

    return render(request, 'core/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
    })


@login_required
def job_create(request):
    if request.user.profile.role != Profile.EMPLOYER:
        return HttpResponseForbidden('Only employers may create job listings.')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job listing created successfully.')
            return redirect('dashboard')
    else:
        form = JobForm()
    return render(request, 'core/job_form.html', {'form': form, 'title': 'Create Job'})


@login_required
def job_edit(request, job_id):
    job = get_object_or_404(Job, pk=job_id, employer=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job listing updated successfully.')
            return redirect('dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'core/job_form.html', {'form': form, 'title': 'Edit Job'})


@login_required
def job_delete(request, job_id):
    job = get_object_or_404(Job, pk=job_id, employer=request.user)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job listing deleted successfully.')
        return redirect('dashboard')
    return render(request, 'core/job_confirm_delete.html', {'job': job})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, is_active=True)
    if request.user.profile.role != Profile.JOB_SEEKER:
        return HttpResponseForbidden('Only job seekers may apply to jobs.')

    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You have already applied to this job.')
        return redirect('job_detail', job_id=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            Notification.objects.create(
                user=job.employer,
                text=f'{request.user.username} applied to {job.title}.',
            )
            messages.success(request, 'Your application has been submitted.')
            return redirect('dashboard')
    else:
        form = ApplicationForm()

    return render(request, 'core/application_form.html', {'form': form, 'job': job})


@login_required
def applications_list(request):
    if request.user.profile.role != Profile.EMPLOYER:
        return HttpResponseForbidden('Only employers can manage applications.')

    applications = Application.objects.filter(job__employer=request.user).order_by('-created_at')
    return render(request, 'core/application_list.html', {'applications': applications})


@login_required
def messages_view(request):
    inbox = Message.objects.filter(receiver=request.user).order_by('-created_at')
    sent_items = Message.objects.filter(sender=request.user).order_by('-created_at')
    users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'core/message_list.html', {
        'inbox': inbox,
        'sent_items': sent_items,
        'users': users,
    })


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, pk=receiver_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            Notification.objects.create(
                user=receiver,
                text=f'New message from {request.user.username}.',
            )
            messages.success(request, 'Message sent successfully.')
            return redirect('messages')
    else:
        form = MessageForm()
    return render(request, 'core/message_form.html', {
        'form': form,
        'receiver': receiver,
    })


@login_required
def notifications(request):
    notifications = request.user.notifications.order_by('-created_at')
    notifications.update(is_read=True)
    return render(request, 'core/notifications.html', {'notifications': notifications})
