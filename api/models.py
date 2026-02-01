# MongoDB models using pymongo
from .mongodb import get_students_collection
from bson import ObjectId
from datetime import datetime

class Student:
    """Student model for MongoDB"""
    
    @staticmethod
    def create(name, email, course, user_id):
        """Create a new student with user ownership"""
        collection = get_students_collection()
        student_data = {
            'name': name,
            'email': email,
            'course': course,
            'user_id': user_id,  # Owner of this student record
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = collection.insert_one(student_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all(user_id=None, is_admin=False):
        """Get all students - filtered by user_id if not admin"""
        collection = get_students_collection()
        if is_admin:
            # Admin can see all students
            students = collection.find()
        else:
            # Regular users can only see their own students
            students = collection.find({'user_id': user_id})
        return [Student._to_dict(student) for student in students]
    
    @staticmethod
    def get_by_id(id, user_id=None, is_admin=False):
        """Get student by ID - check ownership if not admin"""
        collection = get_students_collection()
        try:
            student = collection.find_one({'_id': ObjectId(id)})
            if not student:
                return None
            
            # Admin can access any student, regular users can only access their own
            if not is_admin and student.get('user_id') != user_id:
                return None
            
            return Student._to_dict(student)
        except:
            return None
    
    @staticmethod
    def update(id, user_id=None, is_admin=False, name=None, email=None, course=None):
        """Update student - check ownership if not admin"""
        collection = get_students_collection()
        
        # First check if student exists and user has permission
        student = collection.find_one({'_id': ObjectId(id)})
        if not student:
            return False, 'Student not found'
        
        # Admin can update any student, regular users can only update their own
        if not is_admin and student.get('user_id') != user_id:
            return False, 'Permission denied'
        
        update_data = {'updated_at': datetime.now()}
        if name:
            update_data['name'] = name
        if email:
            update_data['email'] = email
        if course:
            update_data['course'] = course
        
        result = collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )
        return result.modified_count > 0, None
    
    @staticmethod
    def delete(id, user_id=None, is_admin=False):
        """Delete student - check ownership if not admin"""
        collection = get_students_collection()
        
        # First check if student exists and user has permission
        student = collection.find_one({'_id': ObjectId(id)})
        if not student:
            return False, 'Student not found'
        
        # Admin can delete any student, regular users can only delete their own
        if not is_admin and student.get('user_id') != user_id:
            return False, 'Permission denied'
        
        result = collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0, None
    
    @staticmethod
    def _to_dict(student):
        """Convert MongoDB document to dictionary"""
        return {
            '_id': str(student['_id']),
            'id': str(student['_id']),
            'name': student.get('name', ''),
            'email': student.get('email', ''),
            'course': student.get('course', ''),
            'user_id': student.get('user_id', ''),
        }
