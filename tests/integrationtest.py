# integrationtest.py

import app
import pytest 
from database import app, db, Users, Flasks
import requests 
from flask_sqlalchemy import SQLAlchemy

# Post a HTTP request with a valid expression and confirm that the correct answer is returned.

def setUp(self):
        # creates a test client
    self.app = app.test_client()
        # propagate the exceptions to the test client
    self.app.testing = True 

def posttest(self): 
	# Checks if the task has been added to the database. 
	data = {'task': 'this is my unique task', 
			'state': 'doing'}
	# Sends a HTTP post request to the routed address for the add function. 
	r = requests.post(url = 'http://localhost:5000/add', data = data)
	# Query the database for the particular task. 
	assert (Flasks.query.filter_by(task=data['task'],state=data['state']).first()) == True
		# Ensures that the task has been added to the database. is unique.

def postfalsetest(self): 
	data = {'task': 'INSERT INTO USERS values(1,2,3)',
				'state': 123}
	r = requests.post(url = 'http://localhost:5000/add', data = data)
	assert (Flasks.query.filter_by(task=data['task'],state=data['state']).first()) == False