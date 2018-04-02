import flask 
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib

@app.route('/home')
@app.route('/')
def index(): 
	if not session.get('logged_in'): 
		return redirect(url_for('login')) 
	else:
		username = session['username']
		todos = Flasks.query.filter_by(state='todo',task_user=username).all()
		doing = Flasks.query.filter_by(state='doing', task_user=username).all()
		done = Flasks.query.filter_by(state='done', task_user=username).all()
		return render_template('home.html', username=username, todo = todos, doing = doing, done = done) # tasks = tasks)

@app.route('/add', methods=['POST'])
def add():
	if request.method == 'POST':
		username = session["username"]
		task = request.form.get("task", None)
		state = request.form.get("state", None)
		create_task(task, state, username)
		flash('New task successfully posted')
		return redirect(url_for('index'))
	return redirect(url_for('index'))

def create_task(task, state, username): 
	db.session.add(Flasks(task=task, state=state, task_user=username))
	db.session.commit()

@app.route('/edit/<id>', methods=['POST'])
def edit(id):
	task = Flasks.query.filter_by(id = id).first()
	state = request.form.get("newstate", None)
	if state == 'delete': 
		delete_task(id) 
	else:
		task.state = state 
	db.session.commit()
	return redirect(url_for('index'))

def delete_task(task_id):
	db.session.delete(Flasks.query.get(task_id))
	db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if validate(request.form['username'], request.form['password']): 
			session['logged_in'] = True
			flash('You are logged in')
			session['username'] = request.form['username']
			return redirect(url_for('index'))
		else:
			flash('Error')
			return redirect(url_for('login'))
	else:
		return render_template('login.html', error=error)

def validate(username, password):
	completion = False
	all_users = Users.query.all()
	hashed_pw = hashlib.md5(request.form['password'].encode()).hexdigest()
	auth = Users.query.filter_by(username=username,password=hashed_pw).first()
	if auth is None: 
		flash ('Username and/or Password is invalid.')
		return redirect(url_for('login'))
	else:
		completion = True
		return completion

def check_password(hashed_password, userpassword): 
	return hashed_password == hashlib.md5(userpassword.encode()).hexdigest()

@app.route('/register', methods=['GET', 'POST'])
def register():
	session['logged_in'] = False
	if request.method == 'POST':            
		username = request.form['username']
		password = hashlib.md5(request.form['password'].encode()).hexdigest()
		if Users.query.filter_by(username=username).first():
			flash('The username is already taken. Please choose another one.')
			return render_template('register.html', form = request.form)
		else: 
			new = Users(username='{}'.format(username), password='{}'.format(password))
			db.session.add(new) 
			db.session.commit()
			flash('You are registered.')
			session['logged_in'] = True
			session['username'] = username
			return redirect(url_for('index'))
	return render_template('register.html', form = request.form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	session.pop('logged_in', None)
	flash('You are logged out.')
	return redirect(url_for('index'))
	if session['logged_in'] == False:
		flash('You are not even logged in yet!')
		return redirect(url_for('index'))

if __name__ == '__main__': 
	db.create_all()
	app.run(debug=True) 
