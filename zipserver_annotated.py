'''
We built this webapp in under an hour as part of a demo for
the meetup event "[Bottle: When Small is Good](http://www.meetup.com/pug-ip/events/124708312/)."

The webapp is meant to expose a simple API over a corpus of zip codes and
their associated data.

**This file represents the [annotated] final version, so it doesn't include
several of the intermediate teaching points I included during its construction.**

It was created quickly, without any deep regard for extensibility.
It's meant to be instructive, not realistic.  For example, there
is no error checking, only minimal data validation, and the Bottle
variables are fully qualified (e.g., "bottle.HTTPError" instead of
"HTTPError") to help make explicit where Bottle is involved.

Some usage:

    python ./zipserver.py

    http://127.0.0.1:8888/

    http://127.0.0.1:8888/population/08540
    http://127.0.0.1:8888/population/08540?all=1
    http://127.0.0.1:8888/population/08540?all=0

    http://127.0.0.1:8888/population/notazip
    http://127.0.0.1:8888/population/999

    http://127.0.0.1:8888/update-population/08540/100
    http://127.0.0.1:8888/update-population/08540/-100
    http://127.0.0.1:8888/update-population/08540/-100
    curl --data 'zip_code=08540&delta=100' 'http://127.0.0.1:8888/update-population'
    curl --data '{"zip_code": "08540", "delta": 100}' 'http://127.0.0.1:8888/update-population'
    curl -H 'Content-type: application/json' --data '{"zip_code": "08540", "delta": 100}' 'http://127.0.0.1:8888/update-population'

    http://127.0.0.1:8888/browse
'''

import bottle
import sqlite3
import logging

# create our Bottle application.
app = bottle.Bottle()

conn = sqlite3.connect('njny_zip_codes.db')
conn.row_factory = sqlite3.Row

logging.basicConfig()
logger = logging.getLogger('zipserver')
logger.setLevel(logging.INFO)


def valid_zip(zip_code):
    '''If the incoming zip code string is valid, return it.
    Otherwise, raise an exception.'''

    try:
        # for our demo, just an approximate validation suffices
        zc = int(zip_code)
        assert zc > 0
    except:
        raise bottle.HTTPError(400, 'bad zip: {}'.format(zip_code))

    return zip_code


def validate(name, validator):
    '''
    Returns a decorator that validates the incoming HTTP params by
    calling function 'validator' on the param named 'name'.

    We'll raise a 400 if validator() fails, otherwise we just
    return our wrapped function's retval so that HTTP processing
    may continue.
    '''

    def _validate_decorator(fn):

        def _validate_wrapper(*args, **kwargs):
            try:
                logger.info('kwargs: {}'.format(kwargs))

                # do the validation
                kwargs[name] = validator(kwargs[name])

            except Exception as exx:
                raise bottle.HTTPError(400, 'invalid param: {}={}'.format(name, kwargs[name]))

            # if we get here, then the validator succeeded
            return fn(*args, **kwargs)

        return _validate_wrapper
    return _validate_decorator


@app.route('/browse')
def browse_home():
    '''The root of a RESTful interface to browse zip codes.'''

    c = conn.cursor()
    c.execute('select * from zip_codes limit 30')
    all_rows = c.fetchall()

    return bottle.jinja2_template('browse_home.tpl', all_zips = all_rows)


@app.route('/update-population', method='POST')
def update_population():
    '''Add 'delta' to the estimated_population of zip code 'zip_code'.'''

    req = bottle.request
    args = req.json
    zip_code = args['zip_code']
    delta = args['delta']

    c = conn.cursor()
    c.execute('update zip_codes set estimated_population = estimated_population + ? where zip = ?',
        (delta, zip_code))
    conn.commit()
    return 'ok\n'


@app.route('/population/<zip_code>')
@validate('zip_code', valid_zip)
def get_population(zip_code):
    '''Return some of the data associated with zip code 'zip_code'.
    If param 'all' is '1', return all fields.'''

    c = conn.cursor()
    c.execute('select * from zip_codes where zip = ?', (zip_code,))
    row = c.fetchone()

    if not row:
        return 'could not find zip code {}'.format(zip_code)

    is_all = bottle.request.params.get('all')
    if is_all == '1':
        return dict(zip(row.keys(), row))
    else:
        return {'zip': zip_code, 'pop': row['estimated_population'], 'name': row['primary_city']}


@app.route('/')
def home():
    return 'hello, world!\n'


# start the webserver
app.run(port=8888, reloader=True)

