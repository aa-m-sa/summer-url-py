# a small URL shortening service

import psycopg2 # if we want to persistent strorage on heroku
from flask import Flask, request,  g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import os

import appconfig

APPSETTINGS_ENVVAR = 'SUMMER_APP_CONFIG'

app = Flask(__name__)
app.config.from_object(appconfig.DevelopmentConfig)
# override with env var (if it's been set)
app.config.from_object(os.environ[APPSETTINGS_ENVVAR])

def connect_db():
    """Connect to the database.

    :returns: db connection obj

    """
    return psycopg2.connect(database = app.config['DATABASE'])

def init_db():
    """Utility function to initialize the database with schema.sql.
    """
    with connect_db() as conn:
        with conn.cursor() as curs:
            with open("schema.sql", "r") as sch_file:
                curs.execute(sch_file.read())
        conn.commit()


@app.before_request
def before_request():
    # later on we will be using a Heroku postgres db to store urls
    #g.db = connect_db()
    # actually in-memory thingy is a very bad idea;
    # mainly because it doesn't work (concurrency problems)
    pass


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# routes:

# web views

@app.route('/')
def show_index():
    """Show the webapp main page"""
    return render_template('mainpage.html')

@app.route('/addlink', methods=['POST'])
def add_link():
    """Web entry point for api/shorten"""
    shortened = shorten()
    return render_template('shortened.html', shortened = shortened)

# the underlying (public) api

@app.route('/api/shorten', methods=['POST'])
def shorten():
    """Shorten the URL contained in the parameters"""
    if request.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        raise Exception("received POST request Content-Type doesn't conform to API.")
    return create_shortened(request.form['link'])


@app.route('/api/<textid>', methods=['GET'])
def get_link(textid):
    """Redirect to the previously stored url, indentified by id"""
    return redirect(url_shortened(textid), code=301)

def create_shortened(link):
    """Assign an unique id to link and store both in the db.

    :link: url string
    :returns: id as text/plain

    """
    # how this will work internally:
    # db rows: id (integer), text (url)
    # new link -> id++, add to db
    # this ensures that two different links will not get the same id
    # each integer id is mapped into an ASCII string (which is returned)
    return url_for('static', filename='notfound.html')

def url_shortened(textid):
    """Return a valid url assigned to this textid

    :textid: text/plain id
    :returns: url string

    """

    # parse text id to integer
    # fetch the url for that key from db

    # TODO
    return url_for('static', filename='notfound.html')

if __name__ == '__main__':
    app.run()
