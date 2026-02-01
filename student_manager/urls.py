<<<<<<< HEAD
"""
URL configuration for student_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import FileResponse
import os

def serve_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'public', filename)
    if not os.path.exists(file_path):
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('File not found')
    if filename.endswith('.css'):
        content_type = 'text/css'
    elif filename.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'text/html'
    return FileResponse(open(file_path, 'rb'), content_type=content_type)

def serve_index(request):
    index_path = os.path.join(settings.BASE_DIR, 'public', 'index.html')
    return FileResponse(open(index_path, 'rb'), content_type='text/html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('style.css', lambda r: serve_file(r, 'style.css')),
    path('script.js', lambda r: serve_file(r, 'script.js')),
    path('login.html', lambda r: serve_file(r, 'login.html')),
    path('admin.html', lambda r: serve_file(r, 'admin.html')),
    path('index.html', serve_index, name='index-html'),
    path('', serve_index, name='index'),
]
=======
"""
URL configuration for student_manager project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.http import FileResponse
import os

def serve_file(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'public', filename)
    if not os.path.exists(file_path):
        from django.http import HttpResponseNotFound
        return HttpResponseNotFound('File not found')
    if filename.endswith('.css'):
        content_type = 'text/css'
    elif filename.endswith('.js'):
        content_type = 'application/javascript'
    else:
        content_type = 'text/html'
    return FileResponse(open(file_path, 'rb'), content_type=content_type)

def serve_index(request):
    index_path = os.path.join(settings.BASE_DIR, 'public', 'index.html')
    return FileResponse(open(index_path, 'rb'), content_type='text/html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('style.css', lambda r: serve_file(r, 'style.css')),
    path('script.js', lambda r: serve_file(r, 'script.js')),
    path('login.html', lambda r: serve_file(r, 'login.html')),
    path('admin.html', lambda r: serve_file(r, 'admin.html')),
    path('index.html', serve_index, name='index-html'),
    path('', serve_index, name='index'),
]
>>>>>>> 41616403719a7a8cd313d224c939fa3000bb6427
