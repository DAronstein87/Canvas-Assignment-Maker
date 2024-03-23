import json
import threading
import tkinter as tk
import time
import itertools
from canvasAPIFunctions import *  # Import your custom functions

# Function to call provided functions and save their outputs to text files
def save_data_to_files(finish_callback):
    # Simulate long-running task
    courses = get_courses()
    all_course_modules = {}
    all_course_assignment_groups = {}

    # Assuming you have course IDs
    for course in courses:
        all_course_modules[course] = get_student_modules(courses[course])
        all_course_assignment_groups[course] = get_assignment_groups(courses[course])

    # Save data to files
    with open('courses.txt', 'w') as courses_file:
        json.dump(courses, courses_file)

    with open('all_course_modules.txt', 'w') as modules_file:
        json.dump(all_course_modules, modules_file)

    with open('all_course_assignment_groups.txt', 'w') as groups_file:
        json.dump(all_course_assignment_groups, groups_file)

    finish_callback()  # Notify the spinner to stop and close

class SpinnerWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Status")
        # Set window size
        window_width = 400  # Increase the width
        window_height = 200  # Increase the height
        
        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate x and y coordinates for the Tk root window
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        
        # Set the dimensions of the screen and where it is placed
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        
        self.label = tk.Label(root, text="Working...", font=("Arial", 14))
        self.label.pack(expand=True)  # Make the label expand to fill the space
        self.spinner = itertools.cycle(['-', '\\', '|', '/'])
        self.running = False

    def update_spinner(self):
        while self.running:
            next_spinner = next(self.spinner)
            self.label.config(text=f"Working... {next_spinner}")
            time.sleep(0.1)
            self.root.update_idletasks()

    def start(self):
        self.running = True
        threading.Thread(target=self.update_spinner, daemon=True).start()

    def stop(self):
        self.running = False
        self.label.config(text="Done!")
        self.root.update_idletasks()
        time.sleep(1)  # Display "Done!" for 1 second
        self.root.destroy()

def main():
    root = tk.Tk()
    spinner_window = SpinnerWindow(root)
    
    # Start the spinner
    spinner_window.start()
    
    # Start save_data_to_files in its thread and pass spinner_window.stop as the callback to be called when save_data_to_files is done
    data_thread = threading.Thread(target=lambda: save_data_to_files(spinner_window.stop), daemon=True)
    data_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()



