#all the imports
import sqlite3
from flask import Flask, request, session, flash, render_template, redirect, url_for

#configurations
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#Start a Flask web app & load configurations
app = Flask(__name__)
app.config.from_object(__name__)

"""
Note: Temporarity dropping DB for experiment purpose
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
"""

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return "You are in!"
    return render_template('sign_in.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()



