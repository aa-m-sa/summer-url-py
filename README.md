# summer-url-py

A small URL shortening service with Python + Flask (+ Gunicorn). Also, my first web-thing.

## what it does?

It's a web app. It shortens URLs. (Assuming a short domain name, unlike https://surlpy.herokuapp.com/ )

The shortening API can be accessed at [/api/](https://surlpy.herokuapp.com/api/). It conforms to the following:

    POST /shorten
    Parameters: Parameter 'link' should contain the link to shorten.
    Returns: Id for the shortened link in text/plain format.

    GET /{id}
    Returns: 301 redirects the user agent to a previously stored URL. 404 error if no link stored with given id.

## how to use it?

The repo (python modules + etc) can be pushed to Heroku as-it-is.
Set environment variable `SUMMER_APP_CONFIG` to point to a Python object that Flask load as its configuration. Your best bet is `appconfig.ProductionConfig`.
You need also to specify the database URL as another environment variable. See `appconfig.py` for details.
Initialize (Postgres) database with `python initdb.py`.

## tests?

run `nosetests`

## requirements?

* Python 2.x
* Flask
* gunicorn
* psycopg2 and Postgres
* nose (for tests)

## license?

[MIT](./LICENSE).
