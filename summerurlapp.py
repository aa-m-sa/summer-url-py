# a small URL shortening service

import psycopg2 # if we want to persistent strorage on heroku
from flask import Flask, request,  g, redirect, url_for, abort, render_template, flash
from contextlib import closing

CONFIGMODULE = 'appconfig'

app = Flask(__name__)
app.config.from_object(CONFIGMODULE)

def connect_db():
    """Connect to the database.

    :returns: db connection obj

    """
    return psycopg2.connect(database = app.config['DATABASE'])

def init_db():
    """Initializes the database
    """
    #TODO initialize the database with schema.sql
    # sqlalchemy etc seems overkill for an app this simple

    pass


@app.before_request
def before_request():
    # later on we will be using a db for this
    #g.db = connect_db()
    pass


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# view functions

@app.route('/')
def hello_world():
    """Hello World!"""
    return 'Hello World'

if __name__ == '__main__':
    app.run()
