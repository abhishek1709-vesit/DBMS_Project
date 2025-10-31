"""Professor dashboard module for the University Management System"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from config import DATABASE_NAME
from ui_components import create_label, create_entry, create_combobox, create_button
from ui_components import create_treeview, create_form_frame, create_tree_frame

class ProfessorDashboard:
    def __init__(self, root, user):
        self.root = root
        self.current_user = user
        self.logout_callback = None
        self.create_dashboard()
        
    def set_logout_callback(self, callback):
        """Set the callback function for logout"""
        self.logout_callback = callback
        
    def create_dashboard(self):
        """Create professor dashboard"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        welcome_label = tk.Label(header_frame, text=f"Welcome, {self.current_user.name} (Professor)", 
                                font=("Arial", 16, "bold"))
        welcome_label.pack(side=tk.LEFT)
        
        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        self.my_courses_tab = ttk.Frame(self.notebook)
        self.my_students_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.my_courses_tab, text="My Courses")
        self.notebook.add(self.my_students_tab, text="My Students")
        
        # Create content for each tab
        self.create_professor_courses_tab()
        self.create_professor_students_tab()
        
    def logout(self):
        """Logout and return to login screen"""
        if self.logout_callback:
            self.logout_callback()
        
    def create_professor_courses_tab(self):
        """Create the courses tab for professors"""
        # Create tree frame
        tree_frame = create_tree_frame(self.my_courses_tab, "My Courses")
        
        # Create treeview
        columns = ("ID", "Name", "Credits", "Semester", "Department")
        headings = ("ID", "Course Name", "Credits", "Semester", "Department")
        widths = (50, 200, 70, 100, 150)
        self.professor_courses_tree = create_treeview(tree_frame, columns, headings, widths)
        self.load_professor_courses()
        
    def load_professor_courses(self):
        """Load courses assigned to professor"""
        # Clear existing data
        for item in self.professor_courses_tree.get_children():
            self.professor_courses_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.credits, c.semester, d.dept_name
            FROM Course c
            LEFT JOIN Department d ON c.dept_id = d.dept_id
            WHERE c.professor_id = ?
        """, (self.current_user.professor_id,))
        courses = cursor.fetchall()
        
        # Insert data
        for course in courses:
            self.professor_courses_tree.insert("", tk.END, values=course)
            
        conn.close()
            
    def create_professor_students_tab(self):
        """Create the students tab for professors"""
        # Create tree frame
        tree_frame = create_tree_frame(self.my_students_tab, "My Students")
        
        # Create treeview
        columns = ("ID", "Name", "Email", "Course", "Grade")
        headings = ("ID", "Student Name", "Email", "Course", "Grade")
        widths = (50, 150, 200, 200, 70)
        self.professor_students_tree = create_treeview(tree_frame, columns, headings, widths)
        self.load_professor_students()
        
    def load_professor_students(self):
        """Load students enrolled in professor's courses"""
        # Clear existing data
        for item in self.professor_students_tree.get_children():
            self.professor_students_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.student_id, st.name, st.email, c.course_name, e.grade
            FROM Enrollment e
            JOIN Section sec ON e.section_id = sec.section_id
            JOIN Course c ON sec.course_id = c.course_id
            JOIN Student st ON e.student_id = st.student_id
            WHERE c.professor_id = ?
        """, (self.current_user.professor_id,))
        students = cursor.fetchall()
        
        # Insert data
        for student in students:
            self.professor_students_tree.insert("", tk.END, values=student)
            
        conn.close()