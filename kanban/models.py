import sqlite3 as sql
import hashlib

def register(username,password):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?,?)", (username,hash(password)))
    con.commit()
    con.close()

def validate(username, password):
    con = sqlite3.connect('static/user.db')
    completion = False
    with con:
		cur = con.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
	    for row in rows:
	    	dbUser = row[0]
	        dbPass = row[1]
	        if dbUser==username:
	        	completion = check_password(dbPass, password)
    return completion

def checkpassword(hashed_password, userpassword): 
	return hashed_password == hashlib.md5(userpassword.encode()).hexdigest()