"""Database module for the University Management System"""

import sqlite3
from config import DATABASE_NAME

def create_database():
    """Create SQLite database and tables if they don't exist"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Create Department table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Department (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL,
            location TEXT
        )
    """)
    
    # Create Professor table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Professor (
            professor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            dept_id INTEGER,
            username TEXT UNIQUE,
            password TEXT,
            FOREIGN KEY (dept_id) REFERENCES Department(dept_id)
        )
    """)
    
    # Create Course table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Course (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            credits INTEGER,
            semester TEXT,
            dept_id INTEGER,
            professor_id INTEGER,
            FOREIGN KEY (dept_id) REFERENCES Department(dept_id),
            FOREIGN KEY (professor_id) REFERENCES Professor(professor_id)
        )
    """)
    
    # Create Student table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            dob TEXT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    
    # Create Section table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Section (
            section_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id INTEGER,
            room_no TEXT,
            time_slot TEXT,
            FOREIGN KEY (course_id) REFERENCES Course(course_id)
        )
    """)
    
    # Create Enrollment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Enrollment (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            section_id INTEGER,
            grade TEXT,
            FOREIGN KEY (student_id) REFERENCES Student(student_id),
            FOREIGN KEY (section_id) REFERENCES Section(section_id)
        )
    """)
    
    # Create Admin table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM Admin WHERE username = ?", (DEFAULT_ADMIN_USERNAME,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO Admin (username, password) VALUES (?, ?)", 
                      (DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD))
        conn.commit()
    
    conn.commit()
    conn.close()

# Default admin credentials (imported from config)
from config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD