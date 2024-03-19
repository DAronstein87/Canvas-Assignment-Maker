import requests

# Your Canvas LMS API base URL
BASE_URL = "https://fusion.instructure.com/api/v1"

# Your Canvas API token
API_TOKEN = open("myAPIkey.txt", "r").read()


def get_courses():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/courses"
    params = {
        "enrollment_type": "teacher",
        "per_page": 100  # Adjust as necessary
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        courses = response.json()
        return courses
    else:
        print(f"Failed to retrieve courses: {response.status_code}")
        return None

def print_courses(courses):
    if courses:
        print("Courses you teach:")
        for course in courses:
            print(f"- {course['name']} (ID: {course['id']})")
    else:
        print("No courses found.")


def create_assignment(course_id, assignment_name, assignment_description, due_at, group_id, published, module_id=None, position = 0, submission_type = "online_text_entry", points_possible=10):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/courses/{course_id}/assignments"
    payload = {
        "assignment": {
            "name": assignment_name,
            "description": assignment_description,
            "due_at": due_at,
            "assignment_group_id": group_id,
            "published": published,
            "points_possible": points_possible,
            "submission_types": [submission_type],
            # You can add more parameters as necessary, such as grading_type, etc.
        }
    }

    # If submission type is 'online_text_entry', add 'submission_type' and 'online_text_entry_submissions' keys to payload
    if submission_type == 'online_text_entry':
        payload['assignment']['submission_type'] = submission_type
        payload['assignment']['online_text_entry_submissions'] = True

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 201:
        assignment_id = response.json()["id"]
        print("Assignment created successfully.")
        if module_id:
            add_assignment_to_module(course_id, assignment_id, module_id, position)
        return assignment_id
    else:
        print(f"Failed to create assignment: {response.status_code}")
        print(response.text)
        return None

def add_assignment_to_module(course_id, assignment_id, module_id, position = 1):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/courses/{course_id}/modules/{module_id}/items"
    payload = {
        "module_item": {
            "title": "Assignment",
            "type": "Assignment",
            "content_id": assignment_id,
            "position": position
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Assignment added to module successfully.")
    else:
        print(f"Failed to add assignment to module: {response.status_code}")
        print(response.text)

    
def get_user_id():
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/users/self"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_id = response.json()["id"]
        print(f"Your user ID is: {user_id}")
        return user_id
    else:
        print(f"Failed to get user ID: {response.status_code}")
        print(response.text)
        return None


def get_assignment_groups(course_id):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/courses/{course_id}/assignment_groups"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        assignment_groups = response.json()
        return assignment_groups
    else:
        print(f"Failed to get assignment groups: {response.status_code}")
        return None
def get_assignment_group_dict(course_id):
    #Function to return a dict of the names of assignment groups with values of their IDs
    groups = get_assignment_groups(course_id)
    return {group['name']: group['id'] for group in groups}

##if __name__ == "__main__":
##    # Example usage
##    course_id = "205127"  # Replace with the ID of the course
##
##    assignment_groups = get_assignment_groups(course_id)
##    if assignment_groups:
##        print("Assignment Groups:")
##        for group in assignment_groups:
##            print(f"- {group['name']} (ID: {group['id']})")
##    else:
##        print("No assignment groups found.")

##if __name__ == "__main__":
##    # Example usage
##    course_id = "205127"  # Replace with the ID of the course you want to add the assignment to
##    assignment_name = "Test Assignment"
##    assignment_description = "This is a test assignment created via the Canvas API."
##    due_at = "2024-03-15T23:59:59Z"  # Due date in ISO 8601 format
##    group_id = "924973"  # Replace with the ID of the assignment group
##    published = True  # Whether the assignment is published or not
##
##    create_assignment(course_id, assignment_name, assignment_description, due_at, group_id, published)
def get_modules(course_id):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    url = f"{BASE_URL}/courses/{course_id}/modules?include[]=items"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        modules = response.json()
        return modules
    else:
        print(f"Failed to get modules: {response.status_code}")
        print(response.text)
        return None

def print_modules(course_id):
    modules = get_modules(course_id)
    if modules:
        print("Modules in the course:")
        for module in modules:
            print(f"- {module['name']} (ID: {module['id']})")
    else:
        print("No modules found.")

#Functions to get/print the "student digital binder" modules
def get_student_modules(course_id):
    modules = get_modules(course_id)
    student_modules = []
    if modules:
        
        for module in modules:
            if 'student digital' in module['name'].lower():
                student_modules.append(module)

    return student_modules    

def print_student_modules(course_id):
    modules = get_modules(course_id)
    if modules:
        print("Modules containing 'student' in their name:")
        for module in modules:
            if 'student digital' in module['name'].lower():
                print(module['name'])
    else:
        print("No modules found for the course.")

if __name__ == "__main__":
    # Example usage
    course_id = "207098"  # Replace with the ID of the course
    print_student_modules(course_id)
    print(get_assignment_group_dict(course_id))
    assignment_name = "Classwork"
    assignment_description = "This is a classwork assignment created via the Canvas API."
    due_at = None  # Due date in ISO 8601 format
    group_id = "932110"  # Replace with the ID of the assignment group
    published = True  # Whether the assignment is published or not
    module_id = "2618931"  # Replace with the ID of the module to which the assignment should be moved
    # for i in range(4):
    #     create_assignment(course_id, assignment_name, assignment_description, due_at, group_id, published, points_possible=10, submission_type = "online_text_entry", module_id="2618931")
    
    
   


    

