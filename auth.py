"""Authentication module for the University Management System"""

import sqlite3
from config import DATABASE_NAME
from models import Student, Professor, Admin

def authenticate_user(username, password, role):
    """Authenticate user based on role"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        if role == "Student":
            cursor.execute("SELECT * FROM Student WHERE username=? AND password=?", 
                          (username, password))
            user_data = cursor.fetchone()
            if user_data:
                return Student(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
                
        elif role == "Professor":
            cursor.execute("SELECT * FROM Professor WHERE username=? AND password=?", 
                          (username, password))
            user_data = cursor.fetchone()
            if user_data:
                return Professor(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4], user_data[5])
                
        elif role == "Admin":
            cursor.execute("SELECT * FROM Admin WHERE username=? AND password=?", 
                          (username, password))
            user_data = cursor.fetchone()
            if user_data:
                return Admin(user_data[0], user_data[1], user_data[2])
                
    except Exception as e:
        print(f"Authentication error: {e}")
        return None
    finally:
        conn.close()
        
    return None