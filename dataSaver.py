import json

# Importing functions from your provided code
from canvasAPIFunctions import *

# Function to call provided functions and save their outputs to text files
def save_data_to_files():
    # Call functions to get data
    courses = get_courses()
    all_course_modules = {}
    all_course_assignment_groups = {}

    # Assuming you have course IDs in a list called course_ids
    for course in courses:
        all_course_modules[course] = get_student_modules(courses[course])
        all_course_assignment_groups[course] = get_assignment_groups(courses[course])

    # Save data to text files
    with open('courses.txt', 'w') as courses_file:
        json.dump(courses, courses_file)

    with open('all_course_modules.txt', 'w') as modules_file:
        json.dump(all_course_modules, modules_file)

    with open('all_course_assignment_groups.txt', 'w') as groups_file:
        json.dump(all_course_assignment_groups, groups_file)

save_data_to_files()


