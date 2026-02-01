<<<<<<< HEAD
# Student Record Manager - Authentication System

## Features

✅ **User Authentication**
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt

✅ **Data Isolation**
- Each user can only see and modify their own student records
- Users cannot access or change other users' data

✅ **Admin Access**
- Admin users can view and modify ALL users' data
- Admin badge displayed in the UI

✅ **MongoDB Storage**
- All user data and student records stored in MongoDB Atlas
- Separate collections for users and students

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB
Ensure your `.env` file has:
```
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=student_records
DJANGO_SECRET_KEY=your-secret-key-here
```

### 3. Create Admin User
```bash
python create_admin.py
```
Enter username, email, and password for the admin account.

### 4. Run Server
```bash
python manage.py runserver
```

## Usage

### For Regular Users:
1. Go to `http://localhost:8000/login.html`
2. Register a new account or login
3. Add, view, update, and delete your own student records
4. You can only see and modify your own data

### For Admin Users:
1. Login with admin credentials
2. You will see an "ADMIN" badge
3. You can view and modify ALL users' student records
4. Full access to all data in the system

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/user` - Get current user info

### Student Records (Requires Authentication)
- `GET /api/students` - Get all students (filtered by user)
- `POST /api/students` - Add new student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

**Note:** All student endpoints require `Authorization: Bearer <token>` header.

## MongoDB Collections

- **users**: Stores user accounts (username, email, password hash, is_admin)
- **students**: Stores student records (name, email, course, user_id)

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- User ownership validation on all operations
- Admin privilege checks
- CORS enabled for frontend

## Frontend Pages

- `login.html` - Login/Register page
- `index.html` - Main application (requires login)
=======
# Student Record Manager - Authentication System

## Features

✅ **User Authentication**
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt

✅ **Data Isolation**
- Each user can only see and modify their own student records
- Users cannot access or change other users' data

✅ **Admin Access**
- Admin users can view and modify ALL users' data
- Admin badge displayed in the UI

✅ **MongoDB Storage**
- All user data and student records stored in MongoDB Atlas
- Separate collections for users and students

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure MongoDB
Ensure your `.env` file has:
```
MONGO_URI=your_mongodb_connection_string
MONGO_DB_NAME=student_records
DJANGO_SECRET_KEY=your-secret-key-here
```

### 3. Create Admin User
```bash
python create_admin.py
```
Enter username, email, and password for the admin account.

### 4. Run Server
```bash
python manage.py runserver
```

## Usage

### For Regular Users:
1. Go to `http://localhost:8000/login.html`
2. Register a new account or login
3. Add, view, update, and delete your own student records
4. You can only see and modify your own data

### For Admin Users:
1. Login with admin credentials
2. You will see an "ADMIN" badge
3. You can view and modify ALL users' student records
4. Full access to all data in the system

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/user` - Get current user info

### Student Records (Requires Authentication)
- `GET /api/students` - Get all students (filtered by user)
- `POST /api/students` - Add new student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

**Note:** All student endpoints require `Authorization: Bearer <token>` header.

## MongoDB Collections

- **users**: Stores user accounts (username, email, password hash, is_admin)
- **students**: Stores student records (name, email, course, user_id)

## Security Features

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- User ownership validation on all operations
- Admin privilege checks
- CORS enabled for frontend

## Frontend Pages

- `login.html` - Login/Register page
- `index.html` - Main application (requires login)
>>>>>>> 41616403719a7a8cd313d224c939fa3000bb6427
