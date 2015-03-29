#all the imports
import sqlite3
from flask import Flask, request, session,g, flash, render_template, redirect, url_for
from contextlib import closing

#configurations
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

#Start a Flask web app & load configurations
app = Flask(__name__)
app.config.from_object(__name__)



#Database!
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
'''
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables"""
    init_db()
    print('Initialized the database.')
'''

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/view')
def show_entries():
    cur = g.db.execute('select username, password from entries order by id desc') 
    entries = [dict(username=row[0],password=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            flash(error)
            return "You are not in"
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            flash(error)
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return "You are in!"
    return render_template('sign_in.html', error=error)


@app.route('/signup',methods=['GET','POST'])
def signup():
    error = None
    print "Long Live China"
    if request.method == 'POST':
        print "Long Live Changchun!"
        print request.form['First name']
        print request.form['Last name']
        print request.form['Email']
        print request.form['password']
        print request.form['confirm password']
        return "You are in"
    return render_template('sign_up.html',error=error)



@app.route('/logout')
def logout():
    print "In layout function"
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run()



