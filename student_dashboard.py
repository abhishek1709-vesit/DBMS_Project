"""Student dashboard module for the University Management System"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from config import DATABASE_NAME
from ui_components import create_label, create_entry, create_combobox, create_button
from ui_components import create_treeview, create_form_frame, create_tree_frame

class StudentDashboard:
    def __init__(self, root, user):
        self.root = root
        self.current_user = user
        self.create_dashboard()
        
    def create_dashboard(self):
        """Create student dashboard"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        welcome_label = tk.Label(header_frame, text=f"Welcome, {self.current_user.name} (Student)", 
                                font=("Arial", 16, "bold"))
        welcome_label.pack(side=tk.LEFT)
        
        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        self.available_courses_tab = ttk.Frame(self.notebook)
        self.my_courses_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.available_courses_tab, text="Available Courses")
        self.notebook.add(self.my_courses_tab, text="My Courses")
        
        # Create content for each tab
        self.create_available_courses_tab()
        self.create_my_courses_tab()
        
    def logout(self):
        """Logout and return to login screen"""
        # This will be implemented in the main application
        pass
        
    def create_available_courses_tab(self):
        """Create the available courses tab for students"""
        # Left frame for enrollment
        form_frame = create_form_frame(self.available_courses_tab, "Enroll in Course")
        
        # Course selection
        create_label(form_frame, "Select Course:", 0, 0)
        self.available_course_combobox = create_combobox(form_frame, 27, 0, 1)
        self.load_available_courses()
        
        # Enroll button
        enroll_button = ttk.Button(form_frame, text="Enroll", command=self.enroll_in_course)
        enroll_button.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.available_courses_tab, "Available Courses")
        
        # Create treeview
        columns = ("ID", "Name", "Credits", "Professor", "Department")
        headings = ("ID", "Course Name", "Credits", "Professor", "Department")
        widths = (50, 200, 70, 150, 150)
        self.available_courses_tree = create_treeview(tree_frame, columns, headings, widths)
        self.load_available_courses_list()
        
    def load_available_courses(self):
        """Load available courses to combobox"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.course_id, c.course_name 
            FROM Course c
            LEFT JOIN Enrollment e ON c.course_id = e.section_id 
            WHERE e.student_id IS NULL OR e.student_id != ?
        """, (self.current_user.student_id,))
        courses = cursor.fetchall()
        
        # Create a list of course names for the combobox
        course_names = [course[1] for course in courses]
        self.available_course_combobox['values'] = course_names
        
        # Create a mapping for course_id lookup
        self.available_course_id_map = {course[1]: course[0] for course in courses}
        
        conn.close()
        
    def load_available_courses_list(self):
        """Load available courses to treeview"""
        # Clear existing data
        for item in self.available_courses_tree.get_children():
            self.available_courses_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.credits, p.name, d.dept_name
            FROM Course c
            LEFT JOIN Professor p ON c.professor_id = p.professor_id
            LEFT JOIN Department d ON c.dept_id = d.dept_id
        """)
        courses = cursor.fetchall()
        
        # Insert data
        for course in courses:
            self.available_courses_tree.insert("", tk.END, values=course)
            
        conn.close()
            
    def enroll_in_course(self):
        """Enroll student in selected course"""
        course_name = self.available_course_combobox.get()
        
        if not course_name:
            messagebox.showerror("Error", "Please select a course")
            return
            
        try:
            # Get course ID
            course_id = self.available_course_id_map.get(course_name)
            
            # Check if already enrolled
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM Enrollment WHERE student_id=? AND section_id=?", 
                          (self.current_user.student_id, course_id))
            if cursor.fetchone():
                messagebox.showerror("Error", "You are already enrolled in this course")
                conn.close()
                return
                
            # Create a section for this course if it doesn't exist
            cursor.execute("SELECT * FROM Section WHERE course_id=?", (course_id,))
            section = cursor.fetchone()
            if not section:
                # Create a new section
                cursor.execute("INSERT INTO Section (course_id, room_no, time_slot) VALUES (?, ?, ?)", 
                              (course_id, "TBD", "TBD"))
                conn.commit()
                cursor.execute("SELECT * FROM Section WHERE course_id=?", (course_id,))
                section = cursor.fetchone()
                
            # Enroll student
            cursor.execute("INSERT INTO Enrollment (student_id, section_id, grade) VALUES (?, ?, ?)", 
                          (self.current_user.student_id, section[0], "N/A"))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Enrolled in course successfully")
            self.load_available_courses()  # Refresh available courses
            self.load_my_courses()  # Refresh my courses
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll: {str(e)}")
            
    def create_my_courses_tab(self):
        """Create the my courses tab for students"""
        # Create tree frame
        tree_frame = create_tree_frame(self.my_courses_tab, "My Courses")
        
        # Create treeview
        columns = ("ID", "Name", "Credits", "Professor", "Department", "Grade")
        headings = ("ID", "Course Name", "Credits", "Professor", "Department", "Grade")
        widths = (50, 200, 70, 150, 150, 70)
        self.my_courses_tree = create_treeview(tree_frame, columns, headings, widths)
        self.load_my_courses()
        
    def load_my_courses(self):
        """Load student's enrolled courses"""
        # Clear existing data
        for item in self.my_courses_tree.get_children():
            self.my_courses_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.credits, p.name, d.dept_name, e.grade
            FROM Enrollment e
            JOIN Section s ON e.section_id = s.section_id
            JOIN Course c ON s.course_id = c.course_id
            LEFT JOIN Professor p ON c.professor_id = p.professor_id
            LEFT JOIN Department d ON c.dept_id = d.dept_id
            WHERE e.student_id = ?
        """, (self.current_user.student_id,))
        courses = cursor.fetchall()
        
        # Insert data
        for course in courses:
            self.my_courses_tree.insert("", tk.END, values=course)
            
        conn.close()