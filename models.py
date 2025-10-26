"""Data models for the University Management System"""

class User:
    """Base User class"""
    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password

class Student(User):
    """Student model"""
    def __init__(self, student_id, name, email, dob, username, password):
        super().__init__(student_id, name, username, password)
        self.student_id = student_id
        self.email = email
        self.dob = dob

class Professor(User):
    """Professor model"""
    def __init__(self, professor_id, name, email, dept_id, username, password):
        super().__init__(professor_id, name, username, password)
        self.professor_id = professor_id
        self.email = email
        self.dept_id = dept_id

class Admin(User):
    """Admin model"""
    def __init__(self, admin_id, username, password):
        super().__init__(admin_id, "Admin", username, password)
        self.admin_id = admin_id

class Department:
    """Department model"""
    def __init__(self, dept_id, dept_name, location):
        self.dept_id = dept_id
        self.dept_name = dept_name
        self.location = location

class Course:
    """Course model"""
    def __init__(self, course_id, course_name, credits, semester, dept_id, professor_id):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits
        self.semester = semester
        self.dept_id = dept_id
        self.professor_id = professor_id

class Section:
    """Section model"""
    def __init__(self, section_id, course_id, room_no, time_slot):
        self.section_id = section_id
        self.course_id = course_id
        self.room_no = room_no
        self.time_slot = time_slot

class Enrollment:
    """Enrollment model"""
    def __init__(self, enrollment_id, student_id, section_id, grade):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.section_id = section_id
        self.grade = grade