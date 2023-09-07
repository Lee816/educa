import requests
from pathlib import Path
import os, json

BASE_DIR = Path(__file__).resolve().parent.parent

with open(os.path.join(BASE_DIR, "secret.json")) as f:
    secret = json.loads(f.read())

username = secret['USERNAME']
password = secret['PASSWORD']

base_url = 'http://127.0.0.1:8000/api/'

# retrieve all courese
r = requests.get(f'{base_url}courses/')
courses = r.json()

available_courses = ', '.join([course['title'] for course in courses])
print(f'Available courses : {available_courses}')

for course in courses:
    course_id = course['id']
    course_title = course['title']

    r = requests.post(f'{base_url}courses/{course_id}/enroll/',auth=(username,password))

    if r.status_code == 200:
        print(f'Successfully enrolled in {course_title}')