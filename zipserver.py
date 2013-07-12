import bottle
import sqlite3
import logging

app = bottle.Bottle()

conn = sqlite3.connect('njny_zip_codes.db')
conn.row_factory = sqlite3.Row

logging.basicConfig()
logger = logging.getLogger('zipserver')
logger.setLevel(logging.INFO)


def valid_zip(zip_code):
    try:
        zc = int(zip_code)
        assert zc > 0
    except:
        raise bottle.HTTPError(400, 'bad zip: {}'.format(zip_code))

    return zip_code


def validate(name, validator):
    def _validate_decorator(fn):

        def _validate_wrapper(*args, **kwargs):
            try:
                logger.info('kwargs: {}'.format(kwargs))
                kwargs[name] = validator(kwargs[name])

            except Exception as exx:
                raise bottle.HTTPError(400, 'invalid param: {}={}'.format(name, kwargs[name]))

            return fn(*args, **kwargs)

        return _validate_wrapper
    return _validate_decorator


@app.route('/browse')
def browse_home():
    c = conn.cursor()
    c.execute('select * from zip_codes limit 30')
    all_rows = c.fetchall()

    return bottle.jinja2_template('browse_home.tpl', all_zips = all_rows)


@app.route('/update-population', method='POST')
def update_population():
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


app.run(port=8888, reloader=True)

