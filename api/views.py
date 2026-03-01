from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from .models import Student
from .user_model import User
from bson import ObjectId
from bson.errors import InvalidId
from django.conf import settings


# ── Temporary Debug (remove after fix) ────────────────────────────────────────

@csrf_exempt
def debug_files(request):
    """Temporary: list files on Vercel to debug path issues"""
    base = str(settings.BASE_DIR)
    result = {
        'BASE_DIR': base,
        'public_exists': os.path.exists(os.path.join(base, 'public')),
        'staticfiles_exists': os.path.exists(os.path.join(base, 'staticfiles')),
    }
    # List top-level files/dirs
    try:
        result['top_level'] = os.listdir(base)
    except:
        result['top_level'] = 'ERROR'
    # List public/ if exists
    pub = os.path.join(base, 'public')
    if os.path.exists(pub):
        result['public_contents'] = os.listdir(pub)
    # List staticfiles/ if exists
    sf = os.path.join(base, 'staticfiles')
    if os.path.exists(sf):
        result['staticfiles_contents'] = os.listdir(sf)
    return JsonResponse(result)


# ── Helper ────────────────────────────────────────────────────────────────────

def get_user(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None, 'Authentication required'
    return User.verify_token(token)


# ── Auth ──────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        user_id, error = User.create(username, email, password, is_admin=False)
        if error:
            return JsonResponse({'error': error}, status=400)

        user = User.get_by_id(user_id)
        token = User.generate_token(user)
        return JsonResponse({'message': 'User registered successfully', 'token': token, 'user': user}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        user, error = User.authenticate(username, password)
        if error:
            return JsonResponse({'error': error}, status=401)

        token = User.generate_token(user)
        return JsonResponse({'message': 'Login successful', 'token': token, 'user': user})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def current_user(request):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    return JsonResponse({'user': user})


# ── Students ──────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_list(request):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)

    if request.method == 'GET':
        try:
            is_admin = user.get('is_admin', False)
            students = Student.get_all(user_id=user['_id'], is_admin=is_admin)

            if is_admin:
                user_map = {u['id']: u['username'] for u in User.get_all()}
                for s in students:
                    s['username'] = user_map.get(s['user_id'], 'Unknown')

            return JsonResponse(students, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    try:
        data = json.loads(request.body)
        name, email, course = data.get('name'), data.get('email'), data.get('course')

        if not name or not email or not course:
            return JsonResponse({'error': 'All fields are required'}, status=400)

        Student.create(name, email, course, user_id=user['_id'])
        return JsonResponse({'message': 'Student added successfully!'}, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def student_detail(request, id):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)

    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid student ID'}, status=400)

    is_admin = user.get('is_admin', False)

    if request.method == 'GET':
        student = Student.get_by_id(id, user_id=user['_id'], is_admin=is_admin)
        if student:
            return JsonResponse(student)
        return JsonResponse({'error': 'Student not found or access denied'}, status=404)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            success, err = Student.update(id, user_id=user['_id'], is_admin=is_admin,
                                          name=data.get('name'), email=data.get('email'), course=data.get('course'))
            if success:
                return JsonResponse({'message': 'Student updated!'})
            return JsonResponse({'error': err or 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    try:
        success, err = Student.delete(id, user_id=user['_id'], is_admin=is_admin)
        if success:
            return JsonResponse({'message': 'Student deleted!'})
        return JsonResponse({'error': err or 'Student not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ── Admin ─────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(["GET"])
def admin_users(request):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    if not user.get('is_admin'):
        return JsonResponse({'error': 'Admin access required'}, status=403)

    try:
        users = User.get_all()
        for u in users:
            u['student_count'] = len(Student.get_all(user_id=u['id']))
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def admin_update_user(request, id):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    if not user.get('is_admin'):
        return JsonResponse({'error': 'Admin access required'}, status=403)

    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)

    try:
        data = json.loads(request.body)
        success, err = User.update_admin_status(id, data.get('is_admin', False))
        if success:
            return JsonResponse({'message': 'User updated!'})
        return JsonResponse({'error': err or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def admin_delete_user(request, id):
    user, error = get_user(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    if not user.get('is_admin'):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    if user['_id'] == id:
        return JsonResponse({'error': 'Cannot delete your own account'}, status=400)

    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)

    try:
        success, err = User.delete(id)
        if success:
            return JsonResponse({'message': 'User deleted!'})
        return JsonResponse({'error': err or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
