import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, send_file
from io import StringIO
from plotFromDb import plotFromDb as pdb

app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(

    DATABASE = os.path.join(app.root_path, 'brilCast.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
   
   ))
    
app.config.from_envvar('BRILCAST_SETTINGS', silent=True)

def connect_db():
    """Connect to the specific database"""
    
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
    
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print("Initialized the database.")
    
    
def get_db():
    """Opens a new database connection if there is none yet for the 
    current application context. 
        """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select temp, inTemp, inHum, time from entries order by id desc')
    entries = cur.fetchall()
    return render_template('temp.html', entries=entries)
        
@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries (temp, inTemp, inHum, time) values (?,?,?, ?)', [request.form['temp'],request.form['inTemp'], request.form['inHum'], request.form['time']])
    db.commit()
    flash('New entry successfully posted')
    return redirect(url_for('show_entries'))

 
@app.route('/images')
def images():
    return render_template("images.html")

@app.route('/fig')
def fig():
    fig =pdb()
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    
    app.run(host = '0.0.0.0')
        