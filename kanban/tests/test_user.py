# testing_users.py

# Unit testing 

import os 
import unittest 
from database import app, db, Users, Flasks
import app 

test_db = 'test.db'

class BasicTests(unittest.TestCase):

	# Set up is called prior to each unit test executing. 

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(app.config['BASEDIR'], test_db)
		self.app = app.test_client()
		db.drop_all()
		db.create_all()

	# Tear down is called after each unit test finishes executing. 

	def tearDown(self):
		pass

	# Test the main page to check for 200 response code 

	def test_main(self):
		response = self.app.get('/', follow_redirects = True)
		return self.assertEqual(response.status_code, 200)

	# Test register, log in and log out 
	
	def register(self, username, password): 
		return self.app.post('/register', data = dict(username=username, password=password))

	def login(self, username, password):
		return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	# Test cases for registering 

	def test_register(self):
		response = self.register('cindyleow', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)
		# Check if registered 
		self.assertTrue(Users.query.filter_by(task=data['task'],state=data['state']).first())
		self.assertIn(b'Thanks for registering!', response.data)

	def test_login_logout(self):
		register('admin','password')
		r = self.login('admin', 'password')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(session['username'], 'admin')

	def posttask(self, task, state):
		return self.app.post('/add', data = dict(task=task, state=state))

	def test_post(self): 
	# Checks if the task has been added to the database. 
		data = {'task': 'this is my unique task', 
				'state': 'doing'}
		# Sends a HTTP post request to the routed address for the add function. 
		r = posttask(data['task'], data['state'])
		# Query the database for the particular task. 
		self.assertEqual(r.status_code, 200)
		self.assertTrue(Flasks.query.filter_by(task=data['task'],state=data['state']).first())
		# Ensures that the task has been added to the database. and is unique

if __name__ == "__main__":
	unittest.main()


