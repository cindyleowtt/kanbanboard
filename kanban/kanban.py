import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import hashlib

app = Flask(__name__)
app.config.from_object(__name__) 

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'database.db'),
    SECRET_KEY='developmentkey',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

database = '/Users/cindyleow/kanban/kanban/static/database.db'

@app.route('/')
def index(): 
    if not session.get('logged_in'): 
        return redirect(url_for('login')) 
    else:
        username = session['username']
        return render_template('home.html', username = username)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        con = sqlite3.connect(database)
        cur = con.cursor()
        task = request.form['task']
        username = session['username']
        state = request.form['state']
        cur.execute('insert into tasks (task, username, state) values (?, ?, ?)', (task,  username, state))
        con.commit()
        cur.close()
        con.close()
        flash('New todo list successfully posted')
        return redirect(url_for(index))

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
    con = sqlite3.connect(database)
    completion = False
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0] # check if user exists
        dbPass = row[1]
        if dbUser==username:
            completion = check_password(dbPass, password)
    return completion

def check_password(hashed_password, userpassword): 
    return hashed_password == hashlib.md5(userpassword.encode()).hexdigest()

@app.route('/register', methods=['GET', 'POST'])
def register():
    session['logged_in'] = False
    if request.method == 'POST':            
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        con = sqlite3.connect(database)
        cur = con.cursor() 
        cur.execute('SELECT * from USERS WHERE username = ?', (username,))
        result = cur.fetchone()
        if result: 
            flash('The username is already taken. Please choose another one.')
            return render_template('register.html', form = request.form)
        else: 
            cur.execute('INSERT INTO USERS values(?,?)',(username, password))
            con.commit()
            flash('You are registered.')
            cur.close()
            con.close()
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
        return redirect(url_for('index'))

if __name__ == '__main__': 
    app.run(debug=True) 
