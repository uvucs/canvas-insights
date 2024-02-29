import os
import sys
import pandas as pd

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.assignment import Assignment

from concurrent.futures import ThreadPoolExecutor

# Canvas API URL
API_URL = "https://uvu.instructure.com"

# Canvas API key (follow instructions on README file)
#API_KEY = open("API_KEY.txt", "r").read().strip()

# Initialize a new Canvas object
canvas = Canvas(API_URL, sys.argv[1])

# Canvas User ID
USER_ID = canvas.get_user('self').id

courses = []
course_objects: list[Course] = []
course_assignments = []
course_assignment_objects: list[Assignment] = []
course_assignment_submissions = []

print('Fetching Courses')
# iterate through all available courses, append the raw strings to a list of dictionaries, append the Course objects to a separate list
for course in canvas.get_courses():
    courses.append({'course_id':course.id, 'course_name':course.name})
    course_objects.append(course)

# output list of dictionaries as Pandas DataFrame
courses = pd.DataFrame(courses)

print("threshing data, this may take a while")
# OUTER FOR LOOP: iterate through all available courses
# INNER FOR LOOP: for each course, iterate over all available assignments, append full Assignment Objects to list, append the raw strings to a list of dictionaries
for course in course_objects:
    for assignment in course.get_assignments(): # Uses a linked list of GET requests. Can't be parallelized.
        course_assignment_objects.append(assignment)
        course_assignments.append({'course_id':course.id, 'assignment_id':assignment.id, 'assignment_name':assignment.name, 'description':assignment.description, 'submitted':assignment.has_submitted_submissions, 'points_possible':assignment.points_possible, 'submission_types':assignment.submission_types})

# output list of dictionaries as Pandas DataFrame
course_assignments = pd.DataFrame(course_assignments)

print("more threshing, this may take longer")
# for each Assignment Object in the "course_assignment_objects" list, iterate over each available submission made by the user (you)
with ThreadPoolExecutor(max_workers=32) as ex:
    submissions = ex.map(lambda assignment: assignment.get_submission('self'), course_assignment_objects)
    for submission in submissions:
        course_assignment_submissions.append(submission)

submission_info = []
for submission in course_assignment_submissions:
    # only include assignments that have been completed
    try:
        if submission.attempt != None:
            submission_info.append({'assignment_id':submission.assignment_id, 'attachments':submission.attachments, 'attempt':submission.attempt, 'body':submission.body, 'due_date':submission.cached_due_date, 'grade':submission.entered_grade, 'score':submission.entered_score, 'extra_attempts':submission.extra_attempts, 'submission_id':submission.id, 'late':submission.late, 'submission_type':submission.submission_type, 'submitted_at':submission.submitted_at})
    except:
        pass
# output list of dictionaries as Pandas DataFrame
submissions = pd.DataFrame(submission_info)

# reorder columns in DataFrame
submissions = submissions[['assignment_id', 'submission_id', 'submission_type', 'body', 'attachments', 'attempt', 'extra_attempts', 'due_date', 'grade', 'score', 'late', 'submitted_at']]


print('Outputting to files')
courses_file = f'{USER_ID}_courses'
assignments_file = f'{USER_ID}_assignments'
submissions_file = f'{USER_ID}_submissions'

courses_file = os.path.join('test_files', courses_file)
assignments_file = os.path.join('test_files', assignments_file)
submissions_file = os.path.join('test_files', submissions_file)

courses.to_parquet(courses_file, index=False, compression='snappy')
course_assignments.to_parquet(assignments_file, index=False, compression='snappy')
submissions.drop(columns=['attachments'], inplace=True)
submissions.to_parquet(submissions_file, index=False, compression='snappy')
