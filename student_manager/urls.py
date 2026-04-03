"""
URL configuration for student_manager project.
"""
from django.urls import path, include, re_path
from django.http import HttpResponseRedirect, FileResponse, Http404
from django.conf import settings
import os

def serve_public_file(request, file_path=""):
    if not file_path or file_path == "":
        file_path = "index.html"
        
    full_path = os.path.join(settings.BASE_DIR, 'public', file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(open(full_path, 'rb'))
    raise Http404("File not found")

urlpatterns = [
    path('api/', include('api.urls')),
    
    # In development, serve directly from public folder.
    re_path(r'^(?P<file_path>.*\.(html|css|js|png|jpg|jpeg|gif|ico|svg))$', serve_public_file),
    path('', lambda r: serve_public_file(r, 'index.html')),
]
