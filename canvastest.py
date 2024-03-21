import requests

# Your Canvas LMS API base URL
BASE_URL = "https://fusion.instructure.com/api/v1"

# Your Canvas API token
API_TOKEN = open("myAPIkey.txt", "r").read()

headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
#returns a dictionary of course names: course IDs. All get functions return similar dictionaries.
def get_courses():
    
    url = f"{BASE_URL}/courses"
    params = {
        "enrollment_type": "teacher",
        "per_page": 100  # Adjust as necessary
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        courses = response.json()
        return {course['name']: course['id'] for course in courses}
    else:
        print(f"Failed to retrieve courses: {response.status_code}")
        return None

def create_assignment(course_id, assignment_name, assignment_description, due_at, group_id, published, module_id=None, position = 0, submission_type = "online_text_entry", points_possible=10):
    
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
        payload['assignment']['submission_types'] = ["online_text_entry", "online_upload"]

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

def get_assignment_groups(course_id):
    
    url = f"{BASE_URL}/courses/{course_id}/assignment_groups"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        groups = response.json()
        return {group['name']: group['id'] for group in groups}
    else:
        print(f"Failed to get assignment groups: {response.status_code}")
        return None
    

def get_modules(course_id):
    
    url = f"{BASE_URL}/courses/{course_id}/modules?include[]=items"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        modules = response.json()
        return {module['name']: module['id'] for module in modules}
    else:
        print(f"Failed to get modules: {response.status_code}")
        print(response.text)
        return None


#Functions to get/print the "student digital binder" modules
def get_student_modules(course_id):
    
    modules = get_modules(course_id)
    student_modules = {}
    if modules:
        for key in modules.keys():
            if 'student digital' in key.lower():
                student_modules[key] = modules[key]

    return student_modules    

if __name__ == "__main__":
    # Example usage
    course_id = "207098"  # Replace with the ID of the course
    print(get_assignment_groups(course_id))
    print(list(get_student_modules(course_id).keys()))
    assignment_name = "Classwork"
    assignment_description = "This is a classwork assignment created via the Canvas API."
    due_at = None  # Due date in ISO 8601 format
    group_id = "932110"  # Replace with the ID of the assignment group
    published = True  # Whether the assignment is published or not
    module_id = "2618931"  # Replace with the ID of the module to which the assignment should be moved
    
    
    
   


    

