# Flask App

## Overview
A Flask web application using a proper package structure.

## Project Structure
```
.
├── main.py           # Application entry point
├── app/
│   ├── __init__.py   # App factory with create_app()
│   ├── routes.py     # Route blueprints
│   ├── templates/    # HTML templates
│   └── static/       # CSS, JS, images
├── pyproject.toml    # Python dependencies
└── poetry.lock       # Locked dependencies
```

## Running the App
The app runs on port 5000 using `python main.py`.

## Recent Changes
- December 8, 2025: Created Flask package structure with app factory pattern
