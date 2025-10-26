"""UI components module for the University Management System"""

import tkinter as tk
from tkinter import ttk

def create_label(parent, text, row, column, sticky=tk.W, padx=5, pady=5):
    """Create a standardized label"""
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=column, sticky=sticky, padx=padx, pady=pady)
    return label

def create_entry(parent, width, row, column, padx=5, pady=5):
    """Create a standardized entry widget"""
    entry = ttk.Entry(parent, width=width)
    entry.grid(row=row, column=column, padx=padx, pady=pady)
    return entry

def create_combobox(parent, width, row, column, padx=5, pady=5, state="readonly"):
    """Create a standardized combobox"""
    combobox = ttk.Combobox(parent, width=width, state=state)
    combobox.grid(row=row, column=column, padx=padx, pady=pady)
    return combobox

def create_button(parent, text, command, side="left", padx=5):
    """Create a standardized button"""
    button = ttk.Button(parent, text=text, command=command)
    if side == "left":
        button.pack(side=tk.LEFT, padx=padx)
    elif side == "right":
        button.pack(side=tk.RIGHT, padx=padx)
    elif side == "top":
        button.pack(side=tk.TOP, padx=padx)
    elif side == "bottom":
        button.pack(side=tk.BOTTOM, padx=padx)
    else:
        button.pack(side=tk.LEFT, padx=padx)
    return button

def create_treeview(parent, columns, headings, widths):
    """Create a standardized treeview with scrollbars"""
    # Treeview with scrollbar
    tree_frame = ttk.Frame(parent)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
    tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
    tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                       yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
    tree_scroll_y.config(command=tree.yview)
    tree_scroll_x.config(command=tree.xview)
    
    # Set headings and column widths
    for i, (heading, width) in enumerate(zip(headings, widths)):
        tree.heading(columns[i], text=heading)
        tree.column(columns[i], width=width)
    
    tree.pack(fill=tk.BOTH, expand=True)
    return tree

def create_form_frame(parent, text):
    """Create a standardized form frame"""
    form_frame = ttk.LabelFrame(parent, text=text)
    form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    return form_frame

def create_tree_frame(parent, text):
    """Create a standardized tree frame"""
    tree_frame = ttk.LabelFrame(parent, text=text)
    tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    return tree_frame