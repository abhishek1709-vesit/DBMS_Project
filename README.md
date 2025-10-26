# University Management System

A modularized University Management System built with Python, Tkinter, and SQLite.

## Project Structure

```
DBMS/
├── __init__.py              # Package initialization
├── config.py               # Configuration settings
├── database.py             # Database setup and management
├── models.py               # Data models
├── auth.py                 # Authentication module
├── ui_components.py        # Reusable UI components
├── main.py                 # Main application entry point
├── student_dashboard.py    # Student dashboard UI
├── professor_dashboard.py  # Professor dashboard UI
├── admin_dashboard.py      # Admin dashboard UI
├── university.db           # SQLite database file
└── README.md              # This file
```

## Features

### Authentication
- Role-based login system (Student, Professor, Admin)
- Default admin account: `admin` / `admin123`

### Student Features
- View available courses
- Enroll in courses
- View enrolled courses and grades

### Professor Features
- View assigned courses
- View enrolled students and their grades

### Admin Features
- Full management capabilities for all entities
- Assign courses to professors
- Manage students, professors, courses, departments, sections, and enrollments

## Installation

1. Ensure you have Python 3.x installed
2. No additional packages are required (uses only standard library)

## Running the Application

```bash
python main.py
```

## Database

The application automatically creates a SQLite database file named `university.db` with the following tables:
- Department
- Professor
- Course
- Student
- Section
- Enrollment
- Admin

## Modules

### config.py
Contains configuration settings for the application.

### database.py
Handles database creation and initialization.

### models.py
Defines data models for all entities in the system.

### auth.py
Handles user authentication and authorization.

### ui_components.py
Provides reusable UI components for consistent interface design.

### main.py
Main application entry point with login functionality.

### student_dashboard.py
Student-specific dashboard and functionality.

### professor_dashboard.py
Professor-specific dashboard and functionality.

### admin_dashboard.py
Admin-specific dashboard with full management capabilities.