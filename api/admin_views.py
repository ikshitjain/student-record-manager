<<<<<<< HEAD
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .user_model import User
from bson import ObjectId
from bson.errors import InvalidId
from .models import Student

def get_user_from_request(request):
    """Extract user from request token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None, 'Authentication required'
    
    user, error = User.verify_token(token)
    if error:
        return None, error
    return user, None

def check_admin(user):
    """Check if user is admin"""
    if not user or not user.get('is_admin', False):
        return False
    return True

@csrf_exempt
@require_http_methods(["GET"])
def users_list(request):
    """Get all users - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        users = User.get_all()
        # Add student count to each user
        for u in users:
            students = Student.get_all(user_id=u['id'])
            u['student_count'] = len(students)
            
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user_admin(request, id):
    """Update user admin status - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)
    
    try:
        data = json.loads(request.body)
        is_admin = data.get('is_admin', False)
        
        success, error_msg = User.update_admin_status(id, is_admin)
        if success:
            return JsonResponse({'message': 'User admin status updated!'})
        return JsonResponse({'error': error_msg or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to update user: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, id):
    """Delete user - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    # Prevent admin from deleting themselves
    if user['_id'] == id:
        return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
    
    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)
    
    try:
        success, error_msg = User.delete(id)
        if success:
            return JsonResponse({'message': 'User deleted!'})
        return JsonResponse({'error': error_msg or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to delete user: {str(e)}'}, status=500)
=======
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .user_model import User
from bson import ObjectId
from bson.errors import InvalidId
from .models import Student

def get_user_from_request(request):
    """Extract user from request token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None, 'Authentication required'
    
    user, error = User.verify_token(token)
    if error:
        return None, error
    return user, None

def check_admin(user):
    """Check if user is admin"""
    if not user or not user.get('is_admin', False):
        return False
    return True

@csrf_exempt
@require_http_methods(["GET"])
def users_list(request):
    """Get all users - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        users = User.get_all()
        # Add student count to each user
        for u in users:
            students = Student.get_all(user_id=u['id'])
            u['student_count'] = len(students)
            
        return JsonResponse(users, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user_admin(request, id):
    """Update user admin status - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)
    
    try:
        data = json.loads(request.body)
        is_admin = data.get('is_admin', False)
        
        success, error_msg = User.update_admin_status(id, is_admin)
        if success:
            return JsonResponse({'message': 'User admin status updated!'})
        return JsonResponse({'error': error_msg or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to update user: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, id):
    """Delete user - Admin only"""
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if not check_admin(user):
        return JsonResponse({'error': 'Admin access required'}, status=403)
    
    # Prevent admin from deleting themselves
    if user['_id'] == id:
        return JsonResponse({'error': 'Cannot delete your own account'}, status=400)
    
    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid user ID'}, status=400)
    
    try:
        success, error_msg = User.delete(id)
        if success:
            return JsonResponse({'message': 'User deleted!'})
        return JsonResponse({'error': error_msg or 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': f'Failed to delete user: {str(e)}'}, status=500)
>>>>>>> 41616403719a7a8cd313d224c939fa3000bb6427
