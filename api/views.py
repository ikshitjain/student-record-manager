from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Student
from .user_model import User
from bson import ObjectId
from bson.errors import InvalidId

def get_user_from_request(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None, 'Authentication required'
    
    user, error = User.verify_token(token)
    if error:
        return None, error
    return user, None

@csrf_exempt
@require_http_methods(["GET", "POST"])
def student_list(request):
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    if request.method == 'GET':
        try:
            students = Student.get_all(user_id=user['_id'], is_admin=user.get('is_admin', False))
            
            # Append user details if admin
            if user.get('is_admin', False):
                all_users = User.get_all()
                user_map = {u['id']: u['username'] for u in all_users}
                for student in students:
                    student['username'] = user_map.get(student['user_id'], 'Unknown')
            
            return JsonResponse(students, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            course = data.get('course')
            
            if not name or not email or not course:
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            Student.create(name, email, course, user_id=user['_id'])
            return JsonResponse({'message': 'Student added successfully!'}, status=201)
        except Exception as e:
            return JsonResponse({'error': f'Failed to add student: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def student_detail(request, id):
    user, error = get_user_from_request(request)
    if error:
        return JsonResponse({'error': error}, status=401)
    
    try:
        ObjectId(id)
    except (InvalidId, TypeError):
        return JsonResponse({'error': 'Invalid student ID'}, status=400)
    
    if request.method == 'GET':
        try:
            student = Student.get_by_id(id, user_id=user['_id'], is_admin=user.get('is_admin', False))
            if student:
                return JsonResponse(student)
            return JsonResponse({'error': 'Student not found or access denied'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            course = data.get('course')
            
            success, error_msg = Student.update(
                id, 
                user_id=user['_id'], 
                is_admin=user.get('is_admin', False),
                name=name, 
                email=email, 
                course=course
            )
            if success:
                return JsonResponse({'message': 'Student updated!'})
            return JsonResponse({'error': error_msg or 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Failed to update student: {str(e)}'}, status=500)
    
    elif request.method == 'DELETE':
        try:
            success, error_msg = Student.delete(id, user_id=user['_id'], is_admin=user.get('is_admin', False))
            if success:
                return JsonResponse({'message': 'Student deleted!'})
            return JsonResponse({'error': error_msg or 'Student not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'Failed to delete student: {str(e)}'}, status=500)
