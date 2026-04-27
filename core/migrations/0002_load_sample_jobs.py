from django.contrib.auth.hashers import make_password
from django.db import migrations


def create_sample_jobs(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')
    Job = apps.get_model('core', 'Job')

    employers = [
        {
            'username': 'green-tech',
            'email': 'contact@greentech.com',
            'first_name': 'Green',
            'last_name': 'Tech',
            'company_name': 'Green Tech',
        },
        {
            'username': 'bright-edge',
            'email': 'hello@brightedge.com',
            'first_name': 'Bright',
            'last_name': 'Edge',
            'company_name': 'Bright Edge',
        },
        {
            'username': 'horizon-retail',
            'email': 'jobs@horizonretail.com',
            'first_name': 'Horizon',
            'last_name': 'Retail',
            'company_name': 'Horizon Retail',
        },
        {
            'username': 'finpath',
            'email': 'careers@finpath.com',
            'first_name': 'Fin',
            'last_name': 'Path',
            'company_name': 'FinPath',
        },
        {
            'username': 'connect-care',
            'email': 'team@connectcare.com',
            'first_name': 'Connect',
            'last_name': 'Care',
            'company_name': 'Connect Care',
        },
    ]

    sample_jobs = [
        {
            'title': 'Software Engineer',
            'employer': 'green-tech',
            'location': 'Remote',
            'description': 'Build and maintain scalable web applications using Python and Django.',
        },
        {
            'title': 'Marketing Coordinator',
            'employer': 'bright-edge',
            'location': 'Austin, TX',
            'description': 'Support digital marketing campaigns, content creation, and performance tracking.',
        },
        {
            'title': 'Sales Representative',
            'employer': 'horizon-retail',
            'location': 'Chicago, IL',
            'description': 'Develop leads, close deals, and manage strong customer relationships.',
        },
        {
            'title': 'Data Analyst',
            'employer': 'finpath',
            'location': 'New York, NY',
            'description': 'Analyze financial data to produce insights, dashboards, and reports.',
        },
        {
            'title': 'Customer Success Specialist',
            'employer': 'connect-care',
            'location': 'Denver, CO',
            'description': 'Help customers onboard, answer support requests, and drive product satisfaction.',
        },
        {
            'title': 'HR Generalist',
            'employer': 'bright-edge',
            'location': 'Miami, FL',
            'description': 'Manage recruiting, onboarding, employee records, and HR policy support.',
        },
        {
            'title': 'Project Manager',
            'employer': 'horizon-retail',
            'location': 'Seattle, WA',
            'description': 'Plan commercial projects, manage schedules, budgets, and team communication.',
        },
        {
            'title': 'UX/UI Designer',
            'employer': 'green-tech',
            'location': 'San Francisco, CA',
            'description': 'Design user interfaces, prototypes, and conduct user research.',
        },
        {
            'title': 'Operations Manager',
            'employer': 'connect-care',
            'location': 'Atlanta, GA',
            'description': 'Oversee daily operations, logistics, and process improvements.',
        },
        {
            'title': 'Content Writer',
            'employer': 'bright-edge',
            'location': 'Remote',
            'description': 'Produce marketing content, blog posts, and website copy for client campaigns.',
        },
        {
            'title': 'Quality Assurance Tester',
            'employer': 'green-tech',
            'location': 'Boston, MA',
            'description': 'Test web and mobile applications, write test plans, and report defects.',
        },
        {
            'title': 'Social Media Specialist',
            'employer': 'bright-edge',
            'location': 'Los Angeles, CA',
            'description': 'Create and publish social media content while monitoring audience engagement.',
        },
        {
            'title': 'Business Analyst',
            'employer': 'finpath',
            'location': 'Charlotte, NC',
            'description': 'Document workflows, analyze requirements, and support process improvements.',
        },
        {
            'title': 'System Administrator',
            'employer': 'green-tech',
            'location': 'Phoenix, AZ',
            'description': 'Maintain servers, networks, and cloud infrastructure with a focus on reliability.',
        },
        {
            'title': 'Graphic Designer',
            'employer': 'bright-edge',
            'location': 'Portland, OR',
            'description': 'Design marketing materials, logos, and digital assets for creative campaigns.',
        },
        {
            'title': 'Account Manager',
            'employer': 'horizon-retail',
            'location': 'Dallas, TX',
            'description': 'Manage client relationships and ensure campaign deliverables are met.',
        },
        {
            'title': 'Mobile App Developer',
            'employer': 'green-tech',
            'location': 'Remote',
            'description': 'Develop iOS and Android applications using cross-platform technologies.',
        },
        {
            'title': 'Email Marketing Manager',
            'employer': 'bright-edge',
            'location': 'Philadelphia, PA',
            'description': 'Create email campaigns and optimize open rates and conversions.',
        },
        {
            'title': 'Financial Planner',
            'employer': 'finpath',
            'location': 'Orlando, FL',
            'description': 'Guide clients on budgets, investments, and retirement planning.',
        },
        {
            'title': 'Logistics Coordinator',
            'employer': 'horizon-retail',
            'location': 'Houston, TX',
            'description': 'Coordinate shipments, inventory, and carrier communications.',
        },
        {
            'title': 'Recruiter',
            'employer': 'bright-edge',
            'location': 'Remote',
            'description': 'Source candidates, manage interview scheduling, and support hiring pipelines.',
        },
        {
            'title': 'Technical Support Specialist',
            'employer': 'connect-care',
            'location': 'Newark, NJ',
            'description': 'Troubleshoot customer issues and document resolutions clearly.',
        },
        {
            'title': 'Product Manager',
            'employer': 'finpath',
            'location': 'Austin, TX',
            'description': 'Define product roadmaps and collaborate with cross-functional teams.',
        },
        {
            'title': 'Event Coordinator',
            'employer': 'connect-care',
            'location': 'Denver, CO',
            'description': 'Plan corporate events, manage vendors, and coordinate attendee logistics.',
        },
        {
            'title': 'Junior Web Developer',
            'employer': 'green-tech',
            'location': 'Remote',
            'description': 'Support website development using HTML, CSS, and JavaScript.',
        },
    ]

    employer_map = {}
    for employer_data in employers:
        user, created = User.objects.get_or_create(
            username=employer_data['username'],
            defaults={
                'email': employer_data['email'],
                'first_name': employer_data['first_name'],
                'last_name': employer_data['last_name'],
                'password': make_password('Password123!'),
            }
        )
        if not created:
            user.email = employer_data['email']
            user.first_name = employer_data['first_name']
            user.last_name = employer_data['last_name']
            user.save()

        profile, _ = Profile.objects.get_or_create(user=user)
        profile.role = 'employer'
        profile.company_name = employer_data['company_name']
        profile.save()
        employer_map[employer_data['username']] = user

    for job_data in sample_jobs:
        employer = employer_map.get(job_data['employer'])
        if not employer:
            continue
        Job.objects.get_or_create(
            title=job_data['title'],
            employer=employer,
            defaults={
                'description': job_data['description'],
                'location': job_data['location'],
                'is_active': True,
            }
        )


def reverse_func(apps, schema_editor):
    Job = apps.get_model('core', 'Job')
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')

    Job.objects.filter(title__in=[
        'Software Engineer',
        'Marketing Coordinator',
        'Sales Representative',
        'Data Analyst',
        'Customer Success Specialist',
        'HR Generalist',
        'Project Manager',
        'UX/UI Designer',
        'Operations Manager',
        'Content Writer',
        'Quality Assurance Tester',
        'Social Media Specialist',
        'Business Analyst',
        'System Administrator',
        'Graphic Designer',
        'Account Manager',
        'Mobile App Developer',
        'Email Marketing Manager',
        'Financial Planner',
        'Logistics Coordinator',
        'Recruiter',
        'Technical Support Specialist',
        'Product Manager',
        'Event Coordinator',
        'Junior Web Developer',
    ]).delete()

    employer_usernames = ['green-tech', 'bright-edge', 'horizon-retail', 'finpath', 'connect-care']
    for username in employer_usernames:
        try:
            user = User.objects.get(username=username)
            Profile.objects.filter(user=user).delete()
            user.delete()
        except User.DoesNotExist:
            pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_jobs, reverse_func),
    ]
