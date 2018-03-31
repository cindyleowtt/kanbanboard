from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)

app.config.from_object(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////kanban/kanban/kanban.db'
app.config['SECRET_KEY'] = 'this is real, this is me'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'pass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
	'''SQLAlchemy class for users.'''
	__tablename__ = 'users'
	id = db.Column('id', db.Integer, primary_key = True)
	username = db.Column('username', db.String(15))
	password = db.Column('password', db.String(15))
	# tasks = db.relationship('Tasks', backref='users', lazy=True)

	def ___init__(self, username, password):
		self.username = username
		self.password = password

	def __repr__(self):
		return '<User {}>'.format(self.username)

class Tasks(db.Model):
	'''SQLAlchemy class for each task. Normalised.'''
	__tablename__ = 'tasks'
	id = db.Column('id', db.Integer, primary_key = True)
	task = db.Column('task', db.String(200))
	state = db.Column('state', db.String(10))
	# user_id = db.Column('user_id', db.String(15), db.ForeignKey('users.user_id'), nullable=False)

	def ___init__(self, task, state, username):
		self.task = task
		self.state = state
		# self.user_id = user_id

	def json(self):
		return {
			'id': self.id,
			'task': self.task,
			'state': self.state,
			#'user_id': self.user_id
		}


def create_task(task, state): 
	db.session.add(Tasks(task=task, state=state))
	db.session.commit()

def delete_task(task_id):
	db.session.delete(Tasks.query.get(task_id))
	db.session.commit()

def move_state(task, newstate):
	task = Tasks.query.get(task_id)
	modified = False
	db.session.update()