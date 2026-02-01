from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .user_model import User

@csrf_exempt
@require_http_methods(["POST"])
def register(request):
    """Register a new user"""
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
        
        # Get user data and generate token
        user = User.get_by_id(user_id)
        token = User.generate_token(user)
        
        return JsonResponse({
            'message': 'User registered successfully',
            'token': token,
            'user': user
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    """Login user"""
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
        
        return JsonResponse({
            'message': 'Login successful',
            'token': token,
            'user': user
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_current_user(request):
    """Get current user from token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return JsonResponse({'error': 'Token required'}, status=401)
        
        user, error = User.verify_token(token)
        if error:
            return JsonResponse({'error': error}, status=401)
        
        return JsonResponse({'user': user})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
