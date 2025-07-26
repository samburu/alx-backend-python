# Messaging App API
A Django-based messaging API allowing users to manage conversations and messages, with authentication via Django REST Framework.

## Features
* User registration and management (based on Django’s User model)

* Token-based and session authentication

* Conversations and nested message handling

* RESTful API endpoints with Django REST Framework

* Secure and modular project structure

## Project Structure
```bash
messaging_app/
├── chats/                   # Messaging app (conversations, messages)
├── messaging_app/           # Django project settings
├── manage.py
└── requirements.txt
```

## Installation

Clone the repository:

```bash
git clone <repo_url>
cd messaging_app
```

Set up virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Required Packages Include:

* Django

* djangorestframework

* djangorestframework-simplejwt (optional for JWT)

* drf-nested-routers

Configuration
In messaging_app/settings.py, ensure:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'chats',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## Authentication Setup
Create a superuser:

```bash
python manage.py createsuperuser
```


## Running the Application
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Access the browsable API at:

```bash
http://127.0.0.1:8000/api/
📖 API Endpoints
Method	Endpoint	Description
GET	/api/conversations/	List conversations
POST	/api/conversations/	Create a new conversation
GET	/api/conversations/{id}/messages/	List messages in conversation
POST	/api/conversations/{id}/messages/	Send message in conversation
```