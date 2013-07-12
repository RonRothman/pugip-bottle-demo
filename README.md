pugip-bottle-demo
=================
We built this webapp in under an hour as part of a demo for
the Meetup event "[Bottle: When Small is Good](http://www.meetup.com/pug-ip/events/124708312/)."

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

The code and data can be found [here](http://ronrothman.com/public/pugip-bottle-demo/) or [here](https://github.com/RonRothman/pugip-bottle-demo).
The original Python User Group event can be found [here](http://www.meetup.com/pug-ip/events/124708312/).

Ron Rothman

