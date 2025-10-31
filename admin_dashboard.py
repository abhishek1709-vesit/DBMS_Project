"""Admin dashboard module for the University Management System"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from config import DATABASE_NAME
from ui_components import create_label, create_entry, create_combobox, create_button
from ui_components import create_treeview, create_form_frame, create_tree_frame

class AdminDashboard:
    def __init__(self, root, user):
        self.root = root
        self.current_user = user
        self.logout_callback = None
        self.create_dashboard()
        
    def set_logout_callback(self, callback):
        """Set the callback function for logout"""
        self.logout_callback = callback
        
    def create_dashboard(self):
        """Create admin dashboard"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        welcome_label = tk.Label(header_frame, text="Welcome, Admin", 
                                font=("Arial", 16, "bold"))
        welcome_label.pack(side=tk.LEFT)
        
        logout_button = ttk.Button(header_frame, text="Logout", command=self.logout)
        logout_button.pack(side=tk.RIGHT)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create tabs
        self.student_tab = ttk.Frame(self.notebook)
        self.professor_tab = ttk.Frame(self.notebook)
        self.course_tab = ttk.Frame(self.notebook)
        self.department_tab = ttk.Frame(self.notebook)
        self.section_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.student_tab, text="Students")
        self.notebook.add(self.professor_tab, text="Professors")
        self.notebook.add(self.course_tab, text="Courses")
        self.notebook.add(self.department_tab, text="Departments")
        self.notebook.add(self.section_tab, text="Sections")
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Create content for each tab
        self.create_student_tab()
        self.create_professor_tab()
        self.create_course_tab()
        self.create_department_tab()
        self.create_section_tab()
        
    def logout(self):
        """Logout and return to login screen"""
        if self.logout_callback:
            self.logout_callback()
            
    def on_tab_changed(self, event):
        """Handle tab change events to refresh data when needed"""
        # Get the currently selected tab
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        
        # Refresh professor dropdown in course tab when course tab is selected
        if tab_text == "Courses":
            self.load_professors_to_course_combobox()
            self.load_departments_to_course_combobox()
        # Refresh course dropdown in section tab when section tab is selected
        elif tab_text == "Sections":
            self.load_courses_to_section_combobox()
            
    def create_student_tab(self):
        """Create the student management tab"""
        # Left frame for form
        form_frame = create_form_frame(self.student_tab, "Student Information")
        
        # Form fields
        create_label(form_frame, "Name:", 0, 0)
        self.student_name_entry = create_entry(form_frame, 30, 0, 1)
        
        create_label(form_frame, "Email:", 1, 0)
        self.student_email_entry = create_entry(form_frame, 30, 1, 1, pady=5)
        
        create_label(form_frame, "Date of Birth (YYYY-MM-DD):", 2, 0)
        self.student_dob_entry = create_entry(form_frame, 30, 2, 1, pady=5)
        
        create_label(form_frame, "Username:", 3, 0)
        self.student_username_entry = create_entry(form_frame, 30, 3, 1, pady=5)
        
        create_label(form_frame, "Password:", 4, 0)
        self.student_password_entry = create_entry(form_frame, 30, 4, 1, pady=5)
        self.student_password_entry.config(show="*")
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        create_button(button_frame, "Add Student", self.add_student, "left")
        create_button(button_frame, "Update Student", self.update_student, "left")
        create_button(button_frame, "Delete Student", self.delete_student, "left")
        
        # Search
        search_frame = ttk.Frame(form_frame)
        search_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.student_search_entry = ttk.Entry(search_frame, width=20)
        self.student_search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_students)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.student_tab, "Student Records")
        
        # Create treeview
        columns = ("ID", "Name", "Email", "DOB", "Username")
        headings = ("ID", "Name", "Email", "Date of Birth", "Username")
        widths = (50, 150, 200, 100, 100)
        self.student_tree = create_treeview(tree_frame, columns, headings, widths)
        self.student_tree.bind("<ButtonRelease-1>", self.select_student)
        self.load_students()
        
    def load_students(self):
        """Load students from database to treeview"""
        # Clear existing data
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT student_id, name, email, dob, username FROM Student")
        students = cursor.fetchall()
        
        # Insert data
        for student in students:
            self.student_tree.insert("", tk.END, values=student)
            
        conn.close()
            
    def add_student(self):
        """Add a new student to database"""
        name = self.student_name_entry.get()
        email = self.student_email_entry.get()
        dob = self.student_dob_entry.get()
        username = self.student_username_entry.get()
        password = self.student_password_entry.get()
        
        if not name or not username or not password:
            messagebox.showerror("Error", "Name, username, and password are required")
            return
            
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Student (name, email, dob, username, password) VALUES (?, ?, ?, ?, ?)", 
                          (name, email, dob, username, password))
            conn.commit()
            conn.close()
            
            self.load_students()
            
            # Clear form
            self.student_name_entry.delete(0, tk.END)
            self.student_email_entry.delete(0, tk.END)
            self.student_dob_entry.delete(0, tk.END)
            self.student_username_entry.delete(0, tk.END)
            self.student_password_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Student added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")
            
    def select_student(self, event):
        """Select a student from treeview to populate form"""
        try:
            selected_item = self.student_tree.selection()[0]
            values = self.student_tree.item(selected_item, "values")
            
            # Populate form
            self.student_name_entry.delete(0, tk.END)
            self.student_name_entry.insert(0, values[1])
            
            self.student_email_entry.delete(0, tk.END)
            self.student_email_entry.insert(0, values[2])
            
            self.student_dob_entry.delete(0, tk.END)
            self.student_dob_entry.insert(0, values[3])
            
            self.student_username_entry.delete(0, tk.END)
            self.student_username_entry.insert(0, values[4])
        except IndexError:
            pass  # No item selected
            
    def update_student(self):
        """Update selected student"""
        try:
            selected_item = self.student_tree.selection()[0]
            student_id = self.student_tree.item(selected_item, "values")[0]
            
            name = self.student_name_entry.get()
            email = self.student_email_entry.get()
            dob = self.student_dob_entry.get()
            username = self.student_username_entry.get()
            
            if not name or not username:
                messagebox.showerror("Error", "Name and username are required")
                return
                
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # If password field is empty, don't update password
            if self.student_password_entry.get():
                cursor.execute("UPDATE Student SET name=?, email=?, dob=?, username=?, password=? WHERE student_id=?", 
                              (name, email, dob, username, self.student_password_entry.get(), student_id))
            else:
                cursor.execute("UPDATE Student SET name=?, email=?, dob=?, username=? WHERE student_id=?", 
                              (name, email, dob, username, student_id))
            conn.commit()
            conn.close()
            
            self.load_students()
            
            messagebox.showinfo("Success", "Student updated successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a student to update")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")
            
    def delete_student(self):
        """Delete selected student"""
        try:
            selected_item = self.student_tree.selection()[0]
            student_id = self.student_tree.item(selected_item, "values")[0]
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete this student?")
            if result:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Student WHERE student_id=?", (student_id,))
                conn.commit()
                conn.close()
                
                self.load_students()
                
                # Clear form
                self.student_name_entry.delete(0, tk.END)
                self.student_email_entry.delete(0, tk.END)
                self.student_dob_entry.delete(0, tk.END)
                self.student_username_entry.delete(0, tk.END)
                self.student_password_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Student deleted successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a student to delete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")
            
    def search_students(self):
        """Search students by name or ID"""
        search_term = self.student_search_entry.get()
        
        # Clear existing data
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
            
        # Search by name or ID
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        if search_term.isdigit():
            cursor.execute("SELECT student_id, name, email, dob, username FROM Student WHERE student_id=? OR name LIKE ?", 
                          (search_term, f"%{search_term}%"))
        else:
            cursor.execute("SELECT student_id, name, email, dob, username FROM Student WHERE name LIKE ?", (f"%{search_term}%",))
            
        students = cursor.fetchall()
        conn.close()
        
        # Insert data
        for student in students:
            self.student_tree.insert("", tk.END, values=student)
            
    def create_professor_tab(self):
        """Create the professor management tab"""
        # Left frame for form
        form_frame = create_form_frame(self.professor_tab, "Professor Information")
        
        # Form fields
        create_label(form_frame, "Name:", 0, 0)
        self.professor_name_entry = create_entry(form_frame, 30, 0, 1)
        
        create_label(form_frame, "Email:", 1, 0)
        self.professor_email_entry = create_entry(form_frame, 30, 1, 1, pady=5)
        
        create_label(form_frame, "Department:", 2, 0)
        self.professor_dept_combobox = create_combobox(form_frame, 27, 2, 1, pady=5)
        self.load_departments_to_combobox()
        
        create_label(form_frame, "Username:", 3, 0)
        self.professor_username_entry = create_entry(form_frame, 30, 3, 1, pady=5)
        
        create_label(form_frame, "Password:", 4, 0)
        self.professor_password_entry = create_entry(form_frame, 30, 4, 1, pady=5)
        self.professor_password_entry.config(show="*")
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        create_button(button_frame, "Add Professor", self.add_professor, "left")
        create_button(button_frame, "Update Professor", self.update_professor, "left")
        create_button(button_frame, "Delete Professor", self.delete_professor, "left")
        
        # Search
        search_frame = ttk.Frame(form_frame)
        search_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.professor_search_entry = ttk.Entry(search_frame, width=20)
        self.professor_search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_professors)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.professor_tab, "Professor Records")
        
        # Create treeview
        columns = ("ID", "Name", "Email", "Department", "Username")
        headings = ("ID", "Name", "Email", "Department", "Username")
        widths = (50, 150, 200, 150, 100)
        self.professor_tree = create_treeview(tree_frame, columns, headings, widths)
        self.professor_tree.bind("<ButtonRelease-1>", self.select_professor)
        self.load_professors()
        
    def load_departments_to_combobox(self):
        """Load departments to combobox"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT dept_id, dept_name FROM Department")
        departments = cursor.fetchall()
        conn.close()
        
        # Create a list of department names for the combobox
        dept_names = [dept[1] for dept in departments]
        self.professor_dept_combobox['values'] = dept_names
        
        # Create a mapping for dept_id lookup
        self.dept_id_map = {dept[1]: dept[0] for dept in departments}
        
    def load_professors(self):
        """Load professors from database to treeview"""
        # Clear existing data
        for item in self.professor_tree.get_children():
            self.professor_tree.delete(item)
            
        # Fetch data with department names
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT p.professor_id, p.name, p.email, d.dept_name, p.username
            FROM Professor p 
            LEFT JOIN Department d ON p.dept_id = d.dept_id
        """)
        professors = cursor.fetchall()
        conn.close()
        
        # Insert data
        for professor in professors:
            self.professor_tree.insert("", tk.END, values=professor)
            
    def select_professor(self, event):
        """Select a professor from treeview to populate form"""
        try:
            selected_item = self.professor_tree.selection()[0]
            values = self.professor_tree.item(selected_item, "values")
            
            # Populate form
            self.professor_name_entry.delete(0, tk.END)
            self.professor_name_entry.insert(0, values[1])
            
            self.professor_email_entry.delete(0, tk.END)
            self.professor_email_entry.insert(0, values[2])
            
            self.professor_dept_combobox.set(values[3] if values[3] else "")
            self.professor_username_entry.delete(0, tk.END)
            self.professor_username_entry.insert(0, values[4])
        except IndexError:
            pass  # No item selected
            
    def add_professor(self):
        """Add a new professor to database"""
        name = self.professor_name_entry.get()
        email = self.professor_email_entry.get()
        dept_name = self.professor_dept_combobox.get()
        username = self.professor_username_entry.get()
        password = self.professor_password_entry.get()
        
        if not name or not username or not password:
            messagebox.showerror("Error", "Name, username, and password are required")
            return
            
        try:
            # Get department ID
            dept_id = self.dept_id_map.get(dept_name) if dept_name else None
            
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Professor (name, email, dept_id, username, password) VALUES (?, ?, ?, ?, ?)", 
                          (name, email, dept_id, username, password))
            conn.commit()
            conn.close()
            
            self.load_professors()
            
            # Refresh professor dropdown in course tab
            self.load_professors_to_course_combobox()
            # Refresh course dropdown in section tab (as course information may have changed)
            self.load_courses_to_section_combobox()
            
            # Clear form
            self.professor_name_entry.delete(0, tk.END)
            self.professor_email_entry.delete(0, tk.END)
            self.professor_dept_combobox.set("")
            self.professor_username_entry.delete(0, tk.END)
            self.professor_password_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Professor added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add professor: {str(e)}")
            
    def update_professor(self):
        """Update selected professor"""
        try:
            selected_item = self.professor_tree.selection()[0]
            professor_id = self.professor_tree.item(selected_item, "values")[0]
            
            name = self.professor_name_entry.get()
            email = self.professor_email_entry.get()
            dept_name = self.professor_dept_combobox.get()
            username = self.professor_username_entry.get()
            
            if not name or not username:
                messagebox.showerror("Error", "Name and username are required")
                return
                
            # Get department ID
            dept_id = self.dept_id_map.get(dept_name) if dept_name else None
            
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            # If password field is empty, don't update password
            if self.professor_password_entry.get():
                cursor.execute("UPDATE Professor SET name=?, email=?, dept_id=?, username=?, password=? WHERE professor_id=?", 
                              (name, email, dept_id, username, self.professor_password_entry.get(), professor_id))
            else:
                cursor.execute("UPDATE Professor SET name=?, email=?, dept_id=?, username=? WHERE professor_id=?", 
                              (name, email, dept_id, username, professor_id))
            conn.commit()
            conn.close()
            
            self.load_professors()
            
            # Refresh professor dropdown in course tab
            self.load_professors_to_course_combobox()
            # Refresh course dropdown in section tab (as course information may have changed)
            self.load_courses_to_section_combobox()
            
            messagebox.showinfo("Success", "Professor updated successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a professor to update")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update professor: {str(e)}")
            
    def delete_professor(self):
        """Delete selected professor"""
        try:
            selected_item = self.professor_tree.selection()[0]
            professor_id = self.professor_tree.item(selected_item, "values")[0]
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete this professor?")
            if result:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Professor WHERE professor_id=?", (professor_id,))
                conn.commit()
                conn.close()
                
                self.load_professors()
                
                # Refresh professor dropdown in course tab
                self.load_professors_to_course_combobox()
                # Refresh course dropdown in section tab (as course information may have changed)
                self.load_courses_to_section_combobox()
                
                # Clear form
                self.professor_name_entry.delete(0, tk.END)
                self.professor_email_entry.delete(0, tk.END)
                self.professor_dept_combobox.set("")
                self.professor_username_entry.delete(0, tk.END)
                self.professor_password_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Professor deleted successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a professor to delete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete professor: {str(e)}")
            
    def search_professors(self):
        """Search professors by name or ID"""
        search_term = self.professor_search_entry.get()
        
        # Clear existing data
        for item in self.professor_tree.get_children():
            self.professor_tree.delete(item)
            
        # Search by name or ID
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        if search_term.isdigit():
            cursor.execute("""
                SELECT p.professor_id, p.name, p.email, d.dept_name, p.username
                FROM Professor p 
                LEFT JOIN Department d ON p.dept_id = d.dept_id 
                WHERE p.professor_id=? OR p.name LIKE ?
            """, (search_term, f"%{search_term}%"))
        else:
            cursor.execute("""
                SELECT p.professor_id, p.name, p.email, d.dept_name, p.username
                FROM Professor p 
                LEFT JOIN Department d ON p.dept_id = d.dept_id 
                WHERE p.name LIKE ?
            """, (f"%{search_term}%",))
            
        professors = cursor.fetchall()
        conn.close()
        
        # Insert data
        for professor in professors:
            self.professor_tree.insert("", tk.END, values=professor)
            
    def create_course_tab(self):
        """Create the course management tab"""
        # Left frame for form
        form_frame = create_form_frame(self.course_tab, "Course Information")
        
        # Form fields
        create_label(form_frame, "Course Name:", 0, 0)
        self.course_name_entry = create_entry(form_frame, 30, 0, 1)
        
        create_label(form_frame, "Credits:", 1, 0)
        self.course_credits_entry = create_entry(form_frame, 30, 1, 1, pady=5)
        
        create_label(form_frame, "Semester:", 2, 0)
        self.course_semester_entry = create_entry(form_frame, 30, 2, 1, pady=5)
        
        create_label(form_frame, "Department:", 3, 0)
        self.course_dept_combobox = create_combobox(form_frame, 27, 3, 1, pady=5)
        self.load_departments_to_course_combobox()
        
        create_label(form_frame, "Professor:", 4, 0)
        self.course_professor_combobox = create_combobox(form_frame, 27, 4, 1, pady=5)
        self.load_professors_to_course_combobox()
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        create_button(button_frame, "Add Course", self.add_course, "left")
        create_button(button_frame, "Update Course", self.update_course, "left")
        create_button(button_frame, "Delete Course", self.delete_course, "left")
        
        # Search
        search_frame = ttk.Frame(form_frame)
        search_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.course_search_entry = ttk.Entry(search_frame, width=20)
        self.course_search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_courses)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.course_tab, "Course Records")
        
        # Create treeview
        columns = ("ID", "Name", "Credits", "Semester", "Department", "Professor")
        headings = ("ID", "Course Name", "Credits", "Semester", "Department", "Professor")
        widths = (50, 150, 70, 100, 120, 150)
        self.course_tree = create_treeview(tree_frame, columns, headings, widths)
        self.course_tree.bind("<ButtonRelease-1>", self.select_course)
        self.load_courses()
        
    def load_departments_to_course_combobox(self):
        """Load departments to course combobox"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT dept_id, dept_name FROM Department")
        departments = cursor.fetchall()
        conn.close()
        
        # Create a list of department names for the combobox
        dept_names = [dept[1] for dept in departments]
        self.course_dept_combobox['values'] = dept_names
        
        # Create a mapping for dept_id lookup
        self.course_dept_id_map = {dept[1]: dept[0] for dept in departments}
        
    def load_professors_to_course_combobox(self):
        """Load professors to course combobox"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT professor_id, name FROM Professor")
        professors = cursor.fetchall()
        conn.close()
        
        # Create a list of professor names for the combobox
        prof_names = [prof[1] for prof in professors]
        self.course_professor_combobox['values'] = prof_names
        
        # Create a mapping for professor_id lookup
        self.course_prof_id_map = {prof[1]: prof[0] for prof in professors}
        
    def load_courses(self):
        """Load courses from database to treeview"""
        # Clear existing data
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
            
        # Fetch data with department and professor names
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT c.course_id, c.course_name, c.credits, c.semester, d.dept_name, p.name 
            FROM Course c 
            LEFT JOIN Department d ON c.dept_id = d.dept_id
            LEFT JOIN Professor p ON c.professor_id = p.professor_id
        """)
        courses = cursor.fetchall()
        conn.close()
        
        # Insert data
        for course in courses:
            self.course_tree.insert("", tk.END, values=course)
            
    def select_course(self, event):
        """Select a course from treeview to populate form"""
        try:
            selected_item = self.course_tree.selection()[0]
            values = self.course_tree.item(selected_item, "values")
            
            # Populate form
            self.course_name_entry.delete(0, tk.END)
            self.course_name_entry.insert(0, values[1])
            
            self.course_credits_entry.delete(0, tk.END)
            self.course_credits_entry.insert(0, values[2])
            
            self.course_semester_entry.delete(0, tk.END)
            self.course_semester_entry.insert(0, values[3])
            
            self.course_dept_combobox.set(values[4] if values[4] else "")
            self.course_professor_combobox.set(values[5] if values[5] else "")
        except IndexError:
            pass  # No item selected
            
    def add_course(self):
        """Add a new course to database"""
        course_name = self.course_name_entry.get()
        credits = self.course_credits_entry.get()
        semester = self.course_semester_entry.get()
        dept_name = self.course_dept_combobox.get()
        prof_name = self.course_professor_combobox.get()
        
        if not course_name:
            messagebox.showerror("Error", "Course name is required")
            return
            
        try:
            # Get department ID
            dept_id = self.course_dept_id_map.get(dept_name) if dept_name else None
            
            # Get professor ID
            prof_id = self.course_prof_id_map.get(prof_name) if prof_name else None
            
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Course (course_name, credits, semester, dept_id, professor_id) VALUES (?, ?, ?, ?, ?)", 
                          (course_name, credits, semester, dept_id, prof_id))
            conn.commit()
            conn.close()
            
            self.load_courses()
            
            # Refresh course dropdown in section tab
            self.load_courses_to_section_combobox()
            
            # Clear form
            self.course_name_entry.delete(0, tk.END)
            self.course_credits_entry.delete(0, tk.END)
            self.course_semester_entry.delete(0, tk.END)
            self.course_dept_combobox.set("")
            self.course_professor_combobox.set("")
            
            messagebox.showinfo("Success", "Course added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add course: {str(e)}")
            
    def update_course(self):
        """Update selected course"""
        try:
            selected_item = self.course_tree.selection()[0]
            course_id = self.course_tree.item(selected_item, "values")[0]
            
            course_name = self.course_name_entry.get()
            credits = self.course_credits_entry.get()
            semester = self.course_semester_entry.get()
            dept_name = self.course_dept_combobox.get()
            prof_name = self.course_professor_combobox.get()
            
            if not course_name:
                messagebox.showerror("Error", "Course name is required")
                return
                
            # Get department ID
            dept_id = self.course_dept_id_map.get(dept_name) if dept_name else None
            
            # Get professor ID
            prof_id = self.course_prof_id_map.get(prof_name) if prof_name else None
                
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE Course SET course_name=?, credits=?, semester=?, dept_id=?, professor_id=? WHERE course_id=?", 
                          (course_name, credits, semester, dept_id, prof_id, course_id))
            conn.commit()
            conn.close()
            
            self.load_courses()
            
            # Refresh course dropdown in section tab
            self.load_courses_to_section_combobox()
            
            messagebox.showinfo("Success", "Course updated successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a course to update")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update course: {str(e)}")
            
    def delete_course(self):
        """Delete selected course"""
        try:
            selected_item = self.course_tree.selection()[0]
            course_id = self.course_tree.item(selected_item, "values")[0]
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete this course?")
            if result:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Course WHERE course_id=?", (course_id,))
                conn.commit()
                conn.close()
                
                self.load_courses()
                
                # Refresh course dropdown in section tab
                self.load_courses_to_section_combobox()
                
                # Clear form
                self.course_name_entry.delete(0, tk.END)
                self.course_credits_entry.delete(0, tk.END)
                self.course_semester_entry.delete(0, tk.END)
                self.course_dept_combobox.set("")
                self.course_professor_combobox.set("")
                
                messagebox.showinfo("Success", "Course deleted successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a course to delete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete course: {str(e)}")
            
    def search_courses(self):
        """Search courses by name or ID"""
        search_term = self.course_search_entry.get()
        
        # Clear existing data
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
            
        # Search by name or ID
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        if search_term.isdigit():
            cursor.execute("""
                SELECT c.course_id, c.course_name, c.credits, c.semester, d.dept_name, p.name 
                FROM Course c 
                LEFT JOIN Department d ON c.dept_id = d.dept_id
                LEFT JOIN Professor p ON c.professor_id = p.professor_id
                WHERE c.course_id=? OR c.course_name LIKE ?
            """, (search_term, f"%{search_term}%"))
        else:
            cursor.execute("""
                SELECT c.course_id, c.course_name, c.credits, c.semester, d.dept_name, p.name 
                FROM Course c 
                LEFT JOIN Department d ON c.dept_id = d.dept_id
                LEFT JOIN Professor p ON c.professor_id = p.professor_id
                WHERE c.course_name LIKE ?
            """, (f"%{search_term}%",))
            
        courses = cursor.fetchall()
        conn.close()
        
        # Insert data
        for course in courses:
            self.course_tree.insert("", tk.END, values=course)
            
    def create_department_tab(self):
        """Create the department management tab"""
        # Left frame for form
        form_frame = create_form_frame(self.department_tab, "Department Information")
        
        # Form fields
        create_label(form_frame, "Department Name:", 0, 0)
        self.dept_name_entry = create_entry(form_frame, 30, 0, 1)
        
        create_label(form_frame, "Location:", 1, 0)
        self.dept_location_entry = create_entry(form_frame, 30, 1, 1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        create_button(button_frame, "Add Department", self.add_department, "left")
        create_button(button_frame, "Update Department", self.update_department, "left")
        create_button(button_frame, "Delete Department", self.delete_department, "left")
        
        # Search
        search_frame = ttk.Frame(form_frame)
        search_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.dept_search_entry = ttk.Entry(search_frame, width=20)
        self.dept_search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_departments)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.department_tab, "Department Records")
        
        # Create treeview
        columns = ("ID", "Name", "Location")
        headings = ("ID", "Department Name", "Location")
        widths = (50, 200, 200)
        self.dept_tree = create_treeview(tree_frame, columns, headings, widths)
        self.dept_tree.bind("<ButtonRelease-1>", self.select_department)
        self.load_departments()
        
    def load_departments(self):
        """Load departments from database to treeview"""
        # Clear existing data
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)
            
        # Fetch data
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Department")
        departments = cursor.fetchall()
        conn.close()
        
        # Insert data
        for dept in departments:
            self.dept_tree.insert("", tk.END, values=dept)
            
    def select_department(self, event):
        """Select a department from treeview to populate form"""
        try:
            selected_item = self.dept_tree.selection()[0]
            values = self.dept_tree.item(selected_item, "values")
            
            # Populate form
            self.dept_name_entry.delete(0, tk.END)
            self.dept_name_entry.insert(0, values[1])
            
            self.dept_location_entry.delete(0, tk.END)
            self.dept_location_entry.insert(0, values[2])
        except IndexError:
            pass  # No item selected
            
    def add_department(self):
        """Add a new department to database"""
        dept_name = self.dept_name_entry.get()
        location = self.dept_location_entry.get()
        
        if not dept_name:
            messagebox.showerror("Error", "Department name is required")
            return
            
        try:
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Department (dept_name, location) VALUES (?, ?)", 
                          (dept_name, location))
            conn.commit()
            conn.close()
            
            self.load_departments()
            self.load_departments_to_combobox()  # Refresh comboboxes
            self.load_departments_to_course_combobox()
            # Refresh course dropdown in section tab (as course information may have changed)
            self.load_courses_to_section_combobox()
            
            # Clear form
            self.dept_name_entry.delete(0, tk.END)
            self.dept_location_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Department added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add department: {str(e)}")
            
    def update_department(self):
        """Update selected department"""
        try:
            selected_item = self.dept_tree.selection()[0]
            dept_id = self.dept_tree.item(selected_item, "values")[0]
            
            dept_name = self.dept_name_entry.get()
            location = self.dept_location_entry.get()
            
            if not dept_name:
                messagebox.showerror("Error", "Department name is required")
                return
                
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE Department SET dept_name=?, location=? WHERE dept_id=?", 
                          (dept_name, location, dept_id))
            conn.commit()
            conn.close()
            
            self.load_departments()
            self.load_departments_to_combobox()  # Refresh comboboxes
            self.load_departments_to_course_combobox()
            # Refresh course dropdown in section tab (as course information may have changed)
            self.load_courses_to_section_combobox()
            
            messagebox.showinfo("Success", "Department updated successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a department to update")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update department: {str(e)}")
            
    def delete_department(self):
        """Delete selected department"""
        try:
            selected_item = self.dept_tree.selection()[0]
            dept_id = self.dept_tree.item(selected_item, "values")[0]
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete this department?")
            if result:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Department WHERE dept_id=?", (dept_id,))
                conn.commit()
                conn.close()
                
                self.load_departments()
                self.load_departments_to_combobox()  # Refresh comboboxes
                self.load_departments_to_course_combobox()
                # Refresh course dropdown in section tab (as course information may have changed)
                self.load_courses_to_section_combobox()
                
                # Clear form
                self.dept_name_entry.delete(0, tk.END)
                self.dept_location_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Department deleted successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a department to delete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete department: {str(e)}")
            
    def search_departments(self):
        """Search departments by name or ID"""
        search_term = self.dept_search_entry.get()
        
        # Clear existing data
        for item in self.dept_tree.get_children():
            self.dept_tree.delete(item)
            
        # Search by name or ID
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        if search_term.isdigit():
            cursor.execute("SELECT * FROM Department WHERE dept_id=? OR dept_name LIKE ?", 
                          (search_term, f"%{search_term}%"))
        else:
            cursor.execute("SELECT * FROM Department WHERE dept_name LIKE ?", (f"%{search_term}%",))
            
        departments = cursor.fetchall()
        conn.close()
        
        # Insert data
        for dept in departments:
            self.dept_tree.insert("", tk.END, values=dept)
            
    def create_section_tab(self):
        """Create the section management tab"""
        # Left frame for form
        form_frame = create_form_frame(self.section_tab, "Section Information")
        
        # Form fields
        create_label(form_frame, "Course:", 0, 0)
        self.section_course_combobox = create_combobox(form_frame, 27, 0, 1)
        self.load_courses_to_section_combobox()
        
        create_label(form_frame, "Room Number:", 1, 0)
        self.section_room_entry = create_entry(form_frame, 30, 1, 1, pady=5)
        
        create_label(form_frame, "Time Slot:", 2, 0)
        self.section_time_entry = create_entry(form_frame, 30, 2, 1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        create_button(button_frame, "Add Section", self.add_section, "left")
        create_button(button_frame, "Update Section", self.update_section, "left")
        create_button(button_frame, "Delete Section", self.delete_section, "left")
        
        # Search
        search_frame = ttk.Frame(form_frame)
        search_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.section_search_entry = ttk.Entry(search_frame, width=20)
        self.section_search_entry.pack(side=tk.LEFT, padx=5)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_sections)
        search_button.pack(side=tk.LEFT, padx=5)
        
        # Right frame for treeview
        tree_frame = create_tree_frame(self.section_tab, "Section Records")
        
        # Create treeview
        columns = ("ID", "Course", "Room", "Time Slot")
        headings = ("ID", "Course", "Room Number", "Time Slot")
        widths = (50, 200, 120, 120)
        self.section_tree = create_treeview(tree_frame, columns, headings, widths)
        self.section_tree.bind("<ButtonRelease-1>", self.select_section)
        self.load_sections()
        
    def load_courses_to_section_combobox(self):
        """Load courses to section combobox"""
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT course_id, course_name FROM Course")
        courses = cursor.fetchall()
        conn.close()
        
        # Create a list of course names for the combobox
        course_names = [course[1] for course in courses]
        self.section_course_combobox['values'] = course_names
        
        # Create a mapping for course_id lookup
        self.section_course_id_map = {course[1]: course[0] for course in courses}
        
    def load_sections(self):
        """Load sections from database to treeview"""
        # Clear existing data
        for item in self.section_tree.get_children():
            self.section_tree.delete(item)
            
        # Fetch data with course names
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.section_id, c.course_name, s.room_no, s.time_slot 
            FROM Section s 
            LEFT JOIN Course c ON s.course_id = c.course_id
        """)
        sections = cursor.fetchall()
        conn.close()
        
        # Insert data
        for section in sections:
            self.section_tree.insert("", tk.END, values=section)
            
    def add_section(self):
        """Add a new section to database"""
        course_name = self.section_course_combobox.get()
        room_no = self.section_room_entry.get()
        time_slot = self.section_time_entry.get()
        
        if not course_name:
            messagebox.showerror("Error", "Course is required")
            return
            
        try:
            # Get course ID
            course_id = self.section_course_id_map.get(course_name)
            
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Section (course_id, room_no, time_slot) VALUES (?, ?, ?)", 
                          (course_id, room_no, time_slot))
            conn.commit()
            conn.close()
            
            self.load_sections()
            
            # Clear form
            self.section_course_combobox.set("")
            self.section_room_entry.delete(0, tk.END)
            self.section_time_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Section added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add section: {str(e)}")
            
    def select_section(self, event):
        """Select a section from treeview to populate form"""
        try:
            selected_item = self.section_tree.selection()[0]
            values = self.section_tree.item(selected_item, "values")
            
            # Populate form
            self.section_course_combobox.set(values[1])
            
            self.section_room_entry.delete(0, tk.END)
            self.section_room_entry.insert(0, values[2])
            
            self.section_time_entry.delete(0, tk.END)
            self.section_time_entry.insert(0, values[3])
        except IndexError:
            pass  # No item selected
            
    def update_section(self):
        """Update selected section"""
        try:
            selected_item = self.section_tree.selection()[0]
            section_id = self.section_tree.item(selected_item, "values")[0]
            
            course_name = self.section_course_combobox.get()
            room_no = self.section_room_entry.get()
            time_slot = self.section_time_entry.get()
            
            if not course_name:
                messagebox.showerror("Error", "Course is required")
                return
                
            # Get course ID
            course_id = self.section_course_id_map.get(course_name)
                
            conn = sqlite3.connect(DATABASE_NAME)
            cursor = conn.cursor()
            
            cursor.execute("UPDATE Section SET course_id=?, room_no=?, time_slot=? WHERE section_id=?", 
                          (course_id, room_no, time_slot, section_id))
            conn.commit()
            conn.close()
            
            self.load_sections()
            
            messagebox.showinfo("Success", "Section updated successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a section to update")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update section: {str(e)}")
            
    def delete_section(self):
        """Delete selected section"""
        try:
            selected_item = self.section_tree.selection()[0]
            section_id = self.section_tree.item(selected_item, "values")[0]
            
            # Confirm deletion
            result = messagebox.askyesno("Confirm", "Are you sure you want to delete this section?")
            if result:
                conn = sqlite3.connect(DATABASE_NAME)
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM Section WHERE section_id=?", (section_id,))
                conn.commit()
                conn.close()
                
                self.load_sections()
                
                # Clear form
                self.section_course_combobox.set("")
                self.section_room_entry.delete(0, tk.END)
                self.section_time_entry.delete(0, tk.END)
                
                messagebox.showinfo("Success", "Section deleted successfully")
        except IndexError:
            messagebox.showerror("Error", "Please select a section to delete")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete section: {str(e)}")
            
    def search_sections(self):
        """Search sections by course name or ID"""
        search_term = self.section_search_entry.get()
        
        # Clear existing data
        for item in self.section_tree.get_children():
            self.section_tree.delete(item)
            
        # Search by course name or ID
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        if search_term.isdigit():
            cursor.execute("""
                SELECT s.section_id, c.course_name, s.room_no, s.time_slot 
                FROM Section s 
                LEFT JOIN Course c ON s.course_id = c.course_id
                WHERE s.section_id=? OR c.course_name LIKE ?
            """, (search_term, f"%{search_term}%"))
        else:
            cursor.execute("""
                SELECT s.section_id, c.course_name, s.room_no, s.time_slot 
                FROM Section s 
                LEFT JOIN Course c ON s.course_id = c.course_id
                WHERE c.course_name LIKE ?
            """, (f"%{search_term}%",))
            
        sections = cursor.fetchall()
        conn.close()
        
        # Insert data
        for section in sections:
            self.section_tree.insert("", tk.END, values=section)