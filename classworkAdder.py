from canvastest import *
courses = get_courses()

for course in courses:
    if '' in course['name']:
        groups = get_assignment_groups(course['id'])
        print(groups)
        for group in groups:
            if 'classwork' in group['name'].lower():
                classwork = group['id']
        for module in get_student_modules(course['id']):
            for item in module['items']:
                if 'session' in item['title'].lower():
                    position = item['position']+1
                    create_assignment(course['id'], "Classwork", "What did you learn today?", None, classwork, False, module['id'], position)


