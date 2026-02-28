from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('user/', views.current_user, name='current-user'),

    # Students
    path('students/', views.student_list, name='student-list'),
    path('students/<str:id>/', views.student_detail, name='student-detail'),

    # Admin
    path('admin/users/', views.admin_users, name='admin-users'),
    path('admin/users/<str:id>/', views.admin_update_user, name='admin-update-user'),
    path('admin/users/<str:id>/delete/', views.admin_delete_user, name='admin-delete-user'),
]
