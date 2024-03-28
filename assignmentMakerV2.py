#Run dataSaver.py before running this script. It will pull all of your course data from canvas and save in text files. 
#You only need to run the dataSaver file once. Re-run when you have a new course.

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from canvasAPIFunctions import *
import json
import threading

# Function to recreate dictionaries from text files. Assumes these files exist. Create them by first running dataSaver.py
def load_data_from_files():
    courses = {}
    all_course_modules = {}
    all_course_assignment_groups = {}

    # Load data from text files
    with open('courses.txt', 'r') as courses_file:
        courses = json.load(courses_file)

    with open('all_course_modules.txt', 'r') as modules_file:
        all_course_modules = json.load(modules_file)

    with open('all_course_assignment_groups.txt', 'r') as groups_file:
        all_course_assignment_groups = json.load(groups_file)

    return courses, all_course_modules, all_course_assignment_groups

# Fetch courses using the Canvas API
courses, all_course_modules, all_course_assignment_groups = load_data_from_files()

recently_created_assignments = []
class CanvasAssignmentCreator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Canvas Assignment Creator")

        # Course
        self.course_label = ttk.Label(self, text="Course:")
        self.course_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.course_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.course_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.course_combobox.bind("<<ComboboxSelected>>", lambda event: (self.load_modules(), self.load_groups()))

        # Module
        self.module_label = ttk.Label(self, text="Module:")
        self.module_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.module_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.module_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Assignment Group
        self.group_label = ttk.Label(self, text="Assignment Group:")
        self.group_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.group_combobox = ttk.Combobox(self, state="readonly", width=40)
        self.group_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Assignment Name
        self.assignment_name_label = ttk.Label(self, text="Name:")
        self.assignment_name_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.assignment_name_entry = ttk.Entry(self, width=40)
        self.assignment_name_entry.insert(0, 'Homework ' + datetime.now().strftime('%Y-%m-%d'))
        self.assignment_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Assignment Description
        self.assignment_description_label = ttk.Label(self, text="Description:")
        self.assignment_description_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.assignment_description_entry = ttk.Entry(self, width=40)
        self.assignment_description_entry.insert(0, 'Submit your work here')
        self.assignment_description_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Due Date
        self.due_label = ttk.Label(self, text="Due Date:")
        self.due_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.due_entry = ttk.Entry(self, width=40)
        # Calculate the date two days from today
        two_days_from_today = datetime.now() + timedelta(days=2)
        # Format the date as a string
        formatted_date = two_days_from_today.strftime('%Y-%m-%dT%H:%M:%S')
        self.due_entry.insert(0, formatted_date)
        self.due_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Points Possible
        self.points_label = ttk.Label(self, text="Points Possible:")
        self.points_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.points_entry = ttk.Entry(self, width=40)
        self.points_entry.insert(0, '10')
        self.points_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        # Position in Module
        self.position_label = ttk.Label(self, text="Position in Module:")
        self.position_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.position_entry = ttk.Entry(self, width=40)
        self.position_entry.insert(0, '0')
        self.position_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # Published
        self.course_assessment = tk.BooleanVar()
        self.course_assessment.set(False)
        self.course_assessment_checkboxbox = ttk.Checkbutton(self, text="Final Assessment Emoji", variable=self.course_assessment)
        self.course_assessment_checkboxbox.grid(row=8, column=1, padx=5, pady=5, sticky="w")
        
        # Published
        self.published_var = tk.BooleanVar()
        self.published_var.set(True)
        self.published_checkbox = ttk.Checkbutton(self, text="Published", variable=self.published_var)
        self.published_checkbox.grid(row=9, column=1, padx=5, pady=5, sticky="w")

        # Create Assignment Button
        self.create_button = ttk.Button(self, text="Create Assignment", command=self.make_assignment_thread)
        self.create_button.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=11, column=0, columnspan=2, pady=10, sticky='ew')

        # Delete Assignments Button
        self.delete_button = ttk.Button(self, text="Delete Previous Assignment", command=self.delete_assignments_thread)
        self.delete_button.grid(row=12, column=1, padx=5, pady=5, sticky="w")

        self.load_courses()

    def load_courses(self):
        
        # Extract the names of the courses
        course_names = list(courses.keys())

        # Populate the course combobox with the course names
        self.course_combobox['values'] = course_names

        # Select the first course by default if there are courses available
        if course_names:
            self.course_combobox.current(0)

        # Load modules for the first course
        self.load_modules()
        self.load_groups()


    def load_modules(self, event=None):
        # Fetch modules using the Canvas API based on the selected course
        selected_course = self.course_combobox.get()

        if selected_course:
            
            # Extract module names from the fetched data
            module_names = list(all_course_modules[selected_course])
        
            # Populate the module combobox with the module names
            self.module_combobox['values'] = module_names

            # Select the first module by default if there are modules available
            if module_names:
                self.module_combobox.current(0)
        else:
            # If course ID is not found, clear the module combobox
            self.module_combobox['values'] = []
    
    def load_groups(self, event=None):
        # Fetch assignment groups using the Canvas API based on the selected course
        selected_course = self.course_combobox.get()

        if selected_course:
        
            # Extract module names from the fetched data
            group_names = list(all_course_assignment_groups[selected_course])

            # Populate the module combobox with the module names
            self.group_combobox['values'] = group_names

            # Select the first module by default if there are modules available
            if group_names:
                self.group_combobox.current(0)
        else:
            # If course ID is not found, clear the module combobox
            self.group_combobox['values'] = []
    
    def make_assignment_thread(self):
        """
        This function is a wrapper to run the assignment creation in a thread.
        It starts a new thread to create an assignment using the provided parameters.
        """
        # Create and start a new thread for the assignment creation process
        threading.Thread(target=self.make_assignment, daemon=True).start()
    
    def make_assignment(self):
        # This method takes the input values and make API call to create assignment
        course = self.course_combobox.get()
        module = self.module_combobox.get()
        group = self.group_combobox.get()
        due_date = self.due_entry.get()
        points_possible = self.points_entry.get()
        position = self.position_entry.get()
        assignment_name = self.assignment_name_entry.get()
        assignment_description = self.assignment_description_entry.get()
        published = self.published_var.get()
        
        # Define a dictionary to map groups to emojis
        group_emojis = {
            "Independent Practice": "✏️",
            "Classwork": "✏️",
            "Assessments": "📕 ",
            "Unit Assessments": "📕 ",
            "Course Assessment": "📝"
            # Add more groups and corresponding emojis as needed
        }
        
        # Get the emoji corresponding to the selected group
        if self.course_assessment.get():
            emoji = group_emojis["Course Assessment"]
        elif "independent" in group.lower():
            emoji = group_emojis["Independent Practice"]
        elif "classwork" in group.lower():
            emoji = group_emojis["Classwork"]
        elif "assessment" in group.lower():
            emoji = group_emojis["Assessments"]
        elif "evidence of" in group.lower():
            emoji = group_emojis["Independent Practice"]

        # Add the emoji to the beginning of the assignment name
        assignment_name = f"{emoji} {assignment_name}"
        # Create the assignment on canvas
        assignment_id = create_assignment(courses[course], assignment_name, assignment_description, due_date, all_course_assignment_groups[course][group], published, all_course_modules[course][module], position, "online_text_entry", points_possible)
        # Workaround to display the right name. We have to change the name after creating the assignment,
        # and then it displays properly in student module. Otherwise, just shows 'assignment.'
        update_assignment_name(courses[course], assignment_id, assignment_name + " ")
        global recently_created_assignments
        recently_created_assignments.insert(0, (courses[course], assignment_id))
        print(recently_created_assignments)
    
    def delete_assignments_thread(self):
        """
        This function is a wrapper to run the assignment deletion in a thread.
        It starts a new thread to delete one or more assignments
        """
        # Create and start a new thread for the assignment deletion process
        threading.Thread(target=self.delete_assignments, daemon=True).start()
    
    def delete_assignments(self):
        """
        Delete assignments based on the specified number of assignments to delete and the recently_created_assignments list.
        """
        global recently_created_assignments
        try:
            course_id, assignment_id = recently_created_assignments[0]
            delete_assignment(course_id, assignment_id) 
            recently_created_assignments = recently_created_assignments[1:]
            print(recently_created_assignments)
        except:
            print("No more assignments to delete.")
       
if __name__ == "__main__":
    app = CanvasAssignmentCreator()
    app.mainloop()
