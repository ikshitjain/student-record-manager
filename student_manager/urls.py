"""
URL configuration for student_manager project.
"""
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('api/', include('api.urls')),
    # Root URL redirects to /index.html (served by WhiteNoise)
    path('', lambda r: HttpResponseRedirect('/index.html')),
]
