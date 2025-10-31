"""Main application file for the University Management System"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

from config import WINDOW_TITLE, WINDOW_SIZE, BACKGROUND_COLOR
from database import create_database
from auth import authenticate_user
from ui_components import create_label, create_entry, create_combobox, create_button
from ui_components import create_treeview, create_form_frame, create_tree_frame

# Import dashboard modules
from student_dashboard import StudentDashboard
from professor_dashboard import ProfessorDashboard
from admin_dashboard import AdminDashboard

class UniversityManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=BACKGROUND_COLOR)
        
        # Initialize current user
        self.current_user = None
        self.current_user_role = None
        
        # Create database and tables
        create_database()
        
        # Create login UI
        self.create_login_ui()
        
    def create_login_ui(self):
        """Create the login user interface"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Title
        title_label = tk.Label(self.root, text=WINDOW_TITLE, 
                              font=("Arial", 24, "bold"), bg=BACKGROUND_COLOR, fg="#333333")
        title_label.pack(pady=30)
        
        # Login frame
        login_frame = ttk.LabelFrame(self.root, text="Login", padding=20)
        login_frame.pack(pady=20)
        
        # Username
        create_label(login_frame, "Username:", 0, 0)
        self.username_entry = create_entry(login_frame, 30, 0, 1)
        
        # Password
        create_label(login_frame, "Password:", 1, 0)
        self.password_entry = create_entry(login_frame, 30, 1, 1, pady=5)
        self.password_entry.config(show="*")
        
        # Role selection
        create_label(login_frame, "Role:", 2, 0)
        self.role_var = tk.StringVar()
        role_combobox = create_combobox(login_frame, 27, 2, 1, pady=5)
        role_combobox['values'] = ["Student", "Professor", "Admin"]
        role_combobox.set("Student")
        self.role_var = role_combobox
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Info label
        info_label = tk.Label(login_frame, text="Default Admin: admin / admin123", 
                             font=("Arial", 10), fg="gray")
        info_label.grid(row=4, column=0, columnspan=2)
        
    def login(self):
        """Handle user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_var.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
            
        user = authenticate_user(username, password, role)
        if user:
            self.current_user = user
            self.current_user_role = role
            if role == "Student":
                dashboard = StudentDashboard(self.root, user)
                dashboard.set_logout_callback(self.create_login_ui)
            elif role == "Professor":
                dashboard = ProfessorDashboard(self.root, user)
                dashboard.set_logout_callback(self.create_login_ui)
            elif role == "Admin":
                dashboard = AdminDashboard(self.root, user)
                dashboard.set_logout_callback(self.create_login_ui)
        else:
            messagebox.showerror("Error", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversityManagementSystem(root)
    root.mainloop()