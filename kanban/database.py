from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban/kanban/schema.sql'
app.config['SECRET_KEY'] = 'this is real, this is me'
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'pass'

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.Text)
    password = db.Column('password', db.Text)

    def ___init__(self, username, password):
    	self.username = username
    	self.password = password

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column('id', db.Integer, primary_key = True)
    task = db.Column('task', db.Text)
    state = db.Column('state', db.Text)
    username = db.Column('username', db.Text)

    def ___init__(self, task, state, username):
    	self.task = task
    	self.state = state
    	self.username = username
