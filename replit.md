# Flask App

## Overview
A Flask web application with user authentication, using a proper package structure.

## Project Structure
```
.
├── main.py              # Application entry point
├── app/
│   ├── __init__.py      # App factory with create_app()
│   ├── models.py        # Database models (User)
│   ├── forms.py         # WTForms for SignIn/SignUp
│   ├── routes.py        # Route blueprints
│   ├── templates/       # HTML templates
│   │   ├── index.html   # Base template with navbar
│   │   ├── home.html    # Home page
│   │   ├── signin.html  # Sign in form
│   │   ├── signup.html  # Registration form
│   │   └── archive.html # Protected page
│   └── static/          # CSS, JS, images
│       ├── css/
│       └── js/
├── requirements.txt     # Frozen dependencies
├── pyproject.toml       # Python dependencies
└── poetry.lock          # Locked dependencies
```

## Routes
- `/` - Redirects to home
- `/home` - Home page
- `/signin` - Sign in form (GET/POST)
- `/signup` - Registration form (GET/POST)
- `/archive` - Protected page (requires login)
- `/logout` - Sign out

## Running the App
The app runs on port 5000 using `python main.py`.

## Database
Uses PostgreSQL with Flask-SQLAlchemy. User model stores username, email, and hashed password.

## Recent Changes
- December 8, 2025: Added user authentication with Flask-Login
- December 8, 2025: Created User model with Flask-SQLAlchemy
- December 8, 2025: Added routes for home, signin, signup, logout, archive
- December 8, 2025: Created Flask package structure with app factory pattern
