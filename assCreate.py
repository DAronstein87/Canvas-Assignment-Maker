import tkinter as tk
from tkinter import ttk
from datetime import datetime
from canvastest import *
# Fetch courses using the Canvas API
courses = get_courses()
class CanvasAssignmentCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Canvas Assignment Creator")

        # Course
        self.course_label = ttk.Label(self, text="Course:")
        self.course_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.course_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.course_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.course_combobox.bind("<<ComboboxSelected>>", self.load_modules)

        # Module
        self.module_label = ttk.Label(self, text="Module:")
        self.module_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.module_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.module_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Assignment Group
        self.group_label = ttk.Label(self, text="Assignment Group:")
        self.group_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.group_entry = ttk.Entry(self, width=40)
        self.group_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Due Date
        self.due_label = ttk.Label(self, text="Due Date:")
        self.due_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.due_entry = ttk.Entry(self, width=40)
        self.due_entry.insert(0, datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
        self.due_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Points Possible
        self.points_label = ttk.Label(self, text="Points Possible:")
        self.points_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.points_entry = ttk.Entry(self, width=40)
        self.points_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Position
        self.position_label = ttk.Label(self, text="Position:")
        self.position_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.position_entry = ttk.Entry(self, width=40)
        self.position_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Published
        self.published_var = tk.BooleanVar()
        self.published_var.set(True)
        self.published_checkbox = ttk.Checkbutton(self, text="Published", variable=self.published_var)
        self.published_checkbox.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Create Assignment Button
        self.create_button = ttk.Button(self, text="Create Assignment", command=self.create_assignment)
        self.create_button.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # Placeholder for Canvas API integration
        self.load_courses()

    def load_courses(self):
        
        # Extract the names of the courses
        course_names = [course['name'] for course in courses]

        # Populate the course combobox with the course names
        self.course_combobox['values'] = course_names

        # Select the first course by default if there are courses available
        if course_names:
            self.course_combobox.current(0)

        # Load modules for the first course
        self.load_modules()


    def load_modules(self, event=None):
        # Fetch modules using the Canvas API based on the selected course
        selected_course = self.course_combobox.get()
        print(selected_course)
        
        for course in courses:
            if course['name'] == selected_course:
                course_id = course['id']
                
        if course_id:
            # Use the Canvas API to fetch the modules for the selected course. get_modules is imported from canvastest.py
            modules = get_modules(course_id)
            # Extract module names from the fetched data
            module_names = [module['name'] for module in modules]

            # Populate the module combobox with the module names
            self.module_combobox['values'] = module_names

            # Select the first module by default if there are modules available
            if module_names:
                self.module_combobox.current(0)
        else:
            # If course ID is not found, clear the module combobox
            self.module_combobox['values'] = []


    def create_assignment(self):
        # Placeholder method to create assignment using Canvas API
        # This method would take the input values and make API call to create assignment
        # Replace this with your actual Canvas API call to create assignment
        course = self.course_combobox.get()
        module = self.module_combobox.get()
        group = self.group_entry.get()
        due_date = self.due_entry.get()
        points_possible = self.points_entry.get()
        position = self.position_entry.get()
        published = self.published_var.get()

        # Print the values (replace with actual API call)
        print("Course:", course)
        print("Module:", module)
        print("Assignment Group:", group)
        print("Due Date:", due_date)
        print("Points Possible:", points_possible)
        print("Position:", position)
        print("Published:", published)

if __name__ == "__main__":
    app = CanvasAssignmentCreator()
    app.mainloop()
