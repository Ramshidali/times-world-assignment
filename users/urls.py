from django.conf.urls import include
from django.urls import path, re_path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('registration', views.user_registration, name='user_registration'),

    re_path(r'^admin-dashboard/$', views.admin_dashboard, name='admin_dashboard'),
    re_path(r'^staff-dashboard/$', views.staff_dashboard, name='staff_dashboard'),
    re_path(r'^student-dashboard/$', views.student_dashboard, name='student_dashboard'),
    re_path(r'^editor-dashboard/$', views.editor_dashboard, name='editor_dashboard'),
]