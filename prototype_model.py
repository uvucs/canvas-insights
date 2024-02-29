import pandas as pd
from canvasapi import Canvas
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import random

class PrototypeModel:
    def get_data(self, api_key:str):
        """Summary:
            This method extracts all the users assignment submission data for the current semester. It outputs the data as a Pandas DataFrame.

        Args:
            api_key (str): API Key created by the User.

        Returns:
            _type_: DataFrame
        """
        self.api_key = api_key
        url = 'https://uvu.instructure.com'
        cursor = Canvas(url, api_key)
        if cursor == None:
            return print('Error creating cursor object. Check your API Key.')
        courses = []
        course_objects = []
        course_assignments = []
        course_assignment_objects = []
        course_assignment_submissions = []
        
        for course in cursor.get_courses():
            name = course.name
            if '2024 Spring' in name:
                courses.append({'course_id':course.id, 'course_name':course.name})
                course_objects.append(course)
                
        for course in course_objects:
            for assignment in course.get_assignments():
                course_assignment_objects.append(assignment)
                course_assignments.append({'course_id':course.id, 'assignment_id':assignment.id, 'assignment_name':assignment.name, 'description':assignment.description, 'submitted':assignment.has_submitted_submissions, 'points_possible':assignment.points_possible, 'submission_types':assignment.submission_types})
        
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
        
        courses = pd.DataFrame(courses)
        assignments = pd.DataFrame(course_assignments)
        submissions = pd.DataFrame(submission_info)
        submissions = submissions.merge(assignments, on='assignment_id')
        submissions = submissions.merge(courses, on='course_id')
        
        
        return submissions
    
    def clean_data(self, training_data:pd.DataFrame):
        """
        Summary:
        This method is used to clean the raw data collected from the "get_data" method. This removes unnecessary columns, changes datatypes, and creates a label for the model.

        Args:
            training_data (pd.DataFrame): The raw data collected from the "get_data" method.

        Returns:
            _type_: DataFrame
        """
        self.training_data = training_data
        try:
            training_data = training_data[['course_name', 'assignment_name', 'attempt', 'submission_type', 'points_possible', 'grade', 'submitted_at', 'due_date']]
            training_data['course_name'] = training_data['course_name'].str.replace(' | 2024 Spring - Full Term', '')
            training_data.dropna(subset=['grade'], inplace=True)
            training_data['hours_elapsed'] = round(abs((pd.to_datetime(training_data['due_date']) - pd.to_datetime(training_data['submitted_at']))).dt.total_seconds() / 3600, 3)
            training_data = training_data[['course_name', 'attempt', 'submission_type', 'points_possible',  'hours_elapsed']]
        except:
            print(Exception)
        return training_data
    
    def preprocess_data(self, training_data:pd.DataFrame):
        self.training_data = training_data
        encoder = LabelEncoder()
        try:
            training_data['course_name'] = encoder.fit_transform(training_data['course_name'])
            training_data['submission_type'] = encoder.fit_transform(training_data['submission_type'])
        except:
            print(Exception)
        
        return training_data
    
    def run(self, data:pd.DataFrame):
        """Summary:
        This method is used to preprocess the training data by encoding categorical columns and removing unnecessary features.

        Args:
            data (pd.DataFrame): The preprocessed data transformed by the "preprocess_data" method.
        """
        
        self.data = data
        
        X = data.drop(columns=['hours_elapsed'])
        y = data['hours_elapsed']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor()
        
        model.fit(X_train, y_train)
        
        return print(f"We predict it will take you {model.predict([[random.randint(1,3),random.randint(1,4),random.randint(1,3),random.randrange(10,100,5)]])} hours to complete this assignment.")