from django.urls import path
from . import views
from . import auth_views
from . import admin_views

urlpatterns = [
    # Authentication endpoints
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login, name='login'),
    path('user/', auth_views.get_current_user, name='current-user'),
    
    # Student endpoints
    path('students/', views.student_list, name='student-list'),
    path('students/<str:id>/', views.student_detail, name='student-detail'),
    
    # Admin endpoints
    path('admin/users/', admin_views.users_list, name='admin-users-list'),
    path('admin/users/<str:id>/', admin_views.update_user_admin, name='admin-update-user'),
    path('admin/users/<str:id>/delete/', admin_views.delete_user, name='admin-delete-user'),
]
