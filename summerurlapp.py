# a small URL shortening service

import psycopg2 # if we want to persistent strorage on heroku
from flask import Flask, request,  g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import os
import urlparse

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
    if not app.config['DATABASE_URL']:
        raise Exception('Database URL not set!')

    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(app.config['DATABASE_URL'])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return conn

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
    g.db = connect_db()


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
    """Shorten the URL contained in the parameter link, by
    assigning an unique id to link and store both in the db.

    :returns: id as text/plain

    """
    if request.headers.get('Content-Type') != 'application/x-www-form-urlencoded':
        raise Exception("received POST request Content-Type doesn't conform to API.")

    # how this will work internally:
    # db rows: id (integer), text (url)
    # new link -> id++, add to db
    # this ensures that two different links will not get the same id
    # each integer id is mapped into an ASCII string (which is returned)

    cur = g.db.cursor()
    cur.execute('insert into urls (url) values (%s) returning id', [request.form['link']])
    idinteger = cur.fetchone()
    if not idinteger:
        raise Exception('insertin url into db failed')
    g.db.commit()
    return url_for('get_link', textid = str(idinteger[0]), _external=True)


@app.route('/api/<textid>', methods=['GET'])
def get_link(textid):
    """Redirect to the previously stored url, indentified by id.
    Return a valid url assigned to this textid

    :textid: text/plain id
    :returns: url string

    """

    # parse text id to integer
    # fetch the url for that key from db

    # TODO

    cur = g.db.cursor()
    cur.execute('select url from urls where id = %s', [int(textid)])
    orig_url = cur.fetchone()
    return redirect(orig_url[0], code=301)

if __name__ == '__main__':
    app.run()
