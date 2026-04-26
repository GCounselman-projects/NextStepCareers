from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    applications_list,
    apply_job,
    dashboard,
    home,
    job_create,
    job_delete,
    job_detail,
    job_edit,
    logout_view,
    messages_view,
    notifications,
    profile_edit,
    send_message,
    signup,
)

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_edit, name='profile_edit'),
    path('dashboard/', dashboard, name='dashboard'),
    path('jobs/create/', job_create, name='job_create'),
    path('jobs/<int:job_id>/', job_detail, name='job_detail'),
    path('jobs/<int:job_id>/edit/', job_edit, name='job_edit'),
    path('jobs/<int:job_id>/delete/', job_delete, name='job_delete'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('applications/', applications_list, name='applications_list'),
    path('messages/', messages_view, name='messages'),
    path('messages/send/<int:receiver_id>/', send_message, name='send_message'),
    path('notifications/', notifications, name='notifications'),
]
