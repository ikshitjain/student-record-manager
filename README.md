# Student Record Manager

A Django REST API for managing student records with MongoDB Atlas, JWT authentication, and role-based access control.

## Tech Stack

- **Backend:** Django 5.0, Python
- **Database:** MongoDB Atlas (via PyMongo)
- **Auth:** JWT (PyJWT) + bcrypt
- **Deploy:** Vercel (serverless)

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
MONGO_URI=mongodb+srv://your-connection-string
SECRET_KEY=your-secret-key
DEBUG=True
```

Run locally:

```bash
python manage.py runserver
```

## Deploy to Vercel

1. Push to GitHub
2. Import project on [vercel.com](https://vercel.com)
3. Add environment variables: `MONGO_URI`, `SECRET_KEY`, `DEBUG=False`
4. Deploy!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/register/` | Register new user |
| POST | `/api/login/` | Login |
| GET | `/api/user/` | Get current user |
| GET/POST | `/api/students/` | List / Add students |
| GET/PUT/DELETE | `/api/students/<id>/` | Student detail |
| GET | `/api/admin/users/` | List all users (admin) |
| PUT | `/api/admin/users/<id>/` | Update user role (admin) |
| DELETE | `/api/admin/users/<id>/delete/` | Delete user (admin) |