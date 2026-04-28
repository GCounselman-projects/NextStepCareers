from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Job, Profile


class TargetedFeatureTests(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username='green-tech-solutions',
            password='pass12345',
        )
        self.employer.profile.role = Profile.EMPLOYER
        self.employer.profile.company_name = 'Green Tech'
        self.employer.profile.save()

        self.seeker = User.objects.create_user(
            username='pythonista',
            password='pass12345',
            first_name='Ava',
            last_name='Stone',
        )
        self.seeker.profile.role = Profile.JOB_SEEKER
        self.seeker.profile.skills = 'Python, Django, REST APIs'
        self.seeker.profile.bio = 'Computer science student building web apps.'
        self.seeker.profile.experience = 'Internship using Django and SQL.'
        self.seeker.profile.save()

        self.other_seeker = User.objects.create_user(
            username='marketer1',
            password='pass12345',
        )
        self.other_seeker.profile.role = Profile.JOB_SEEKER
        self.other_seeker.profile.skills = 'Content strategy'
        self.other_seeker.profile.bio = 'Marketing major'
        self.other_seeker.profile.save()

        self.job = Job.objects.create(
            employer=self.employer,
            title='Backend Developer',
            description='Build Django features.',
            location='Remote',
            is_active=True,
        )

    def test_secondary_pages_show_contextual_back_links(self):
        job_detail_response = self.client.get(
            reverse('job_detail', args=[self.job.id]),
            {'next': reverse('dashboard')},
        )
        self.assertContains(job_detail_response, 'page-back-link')
        self.assertContains(job_detail_response, f'href="{reverse("dashboard")}"')

        self.client.login(username='pythonista', password='pass12345')
        application_response = self.client.get(
            reverse('apply_job', args=[self.job.id]),
            {'next': reverse('job_detail', args=[self.job.id])},
        )
        self.assertContains(application_response, 'page-back-link')
        self.assertContains(application_response, f'value="{reverse("job_detail", args=[self.job.id])}"')

        self.client.logout()
        self.client.login(username='green-tech-solutions', password='pass12345')
        message_response = self.client.get(
            reverse('send_message', args=[self.seeker.id]),
            {'next': reverse('messages')},
        )
        self.assertContains(message_response, 'page-back-link')
        self.assertContains(message_response, f'href="{reverse("messages")}"')

    def test_primary_pages_do_not_show_back_links(self):
        home_response = self.client.get(reverse('home'))
        self.assertNotContains(home_response, 'page-back-link')

        self.client.login(username='green-tech-solutions', password='pass12345')
        dashboard_response = self.client.get(reverse('dashboard'))
        self.assertNotContains(dashboard_response, 'page-back-link')

    def test_employer_can_search_job_seekers_by_keyword(self):
        self.client.login(username='green-tech-solutions', password='pass12345')
        response = self.client.get(reverse('dashboard'), {'seeker_q': 'Python'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Search job seekers')
        self.assertContains(response, 'pythonista')
        self.assertContains(response, 'Python, Django, REST APIs')
        self.assertNotContains(response, 'marketer1')

    def test_job_seeker_dashboard_does_not_expose_employer_search(self):
        self.client.login(username='pythonista', password='pass12345')
        response = self.client.get(reverse('dashboard'), {'seeker_q': 'Python'})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Search job seekers')
        self.assertNotContains(response, 'Keywords')
        self.assertNotContains(response, 'marketer1')
