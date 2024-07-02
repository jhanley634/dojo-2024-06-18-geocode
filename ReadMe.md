
This repo supports a pair of [talks](https://www.meetup.com/hackerdojo/events)
given Tuesday June 18th and July 2nd at the [Hacker Dojo](https://www.hackerdojo.com).
Start out by following these setup instructions.

# setup

Either tell your IDE to clone the repo to a convenient local folder,
or follow these instructions at a bash prompt.

1. `cd` somewhere suitable and then clone in the usual way: `$ git clone https://github.com/jhanley634/dojo-2024-06-18-geocode.git`
2. `cd` into the repo: `$ cd dojo-2024-06-18-geocode`
3. Create a new virtual environment: `$ make venv` (actually just `make` suffices)
4. Activate the venv: `$ source ~/.venv/dojo-geocode/bin/activate`

# web_bench

This fills in timing numbers for some performance concerns
that cropped up in a recent evening's discussions.

`server.py` is a simple bjoern webserver, an anvil to pound on.

The `client_speed_compare.py` client demos several async and
synchronous ways of making http requests.
It reports timing figures to stdout.
You will find measurements from one run in data/timing.txt.

`client_speed_chart.py` parses such a log,
and uses seaborn to depict same data in several ways:
- boxplot
- catplot
- violinplot
- kdeplot (kernel density estimate)

Run it with `$ make web_bench/data/timing.csv`

# geocoding

We find (lat, long) pairs for the several thousand residential addresses
in data/resident_addr.csv, storing API results to data/geocoded.csv.
You can run `geocode.py` with `$ make geocoding/data/geocoded.csv`.

With (lat, long) values in hand, we can display them in several ways.
1. simple -- a streamlit app, which supports Open Street Map drill downs
2. bay_area -- a matplotlib overview that shows coastlines
3. san_mateo -- zoomed in on San Mateo county, showing its southern border
4. filter -- a Flask server that lets us focus on the houses of a given street
