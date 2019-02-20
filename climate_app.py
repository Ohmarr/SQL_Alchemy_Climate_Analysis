# ## Step 2 - Climate App
# Design a Flask API based on the queries that you have just developed.
# ### Routes
# * `/`
#   * Home page.
#   * List all routes that are available.
# * `/api/v1.0/precipitation`
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#   * Return the JSON representation of your dictionary.
# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset.
# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point.
#   * Return a JSON list of Temperature Observations (tobs) for the previous year.
# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# ## Hints
# * You will need to join the station and measurement tables for some of the analysis queries.
# * Use Flask `jsonify` to convert your API data into a valid JSON response object.


import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template, redirect #flask is a server
#################################################
# Database Setup - SESSION SETUP
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
        routes = ['http://127.0.0.1:5000/api/v1.0/precipitation',
                'http://127.0.0.1:5000/api/v1.0/stations',
                'http://127.0.0.1:5000/api/v1.0/tobs',
                'http://127.0.0.1:5000/api/v1.0/<start>',
                'http://127.0.0.1:5000/api/v1.0/<start>/<end>'
        ]
        return render_template('index.html', routes=routes)

@app.route('/api/v1.0/precipitation')
def precipitation():
#Starting from the last data point in the database. 
# Calculate the date one year from the last date in data set.
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
# Perform a query to retrieve the data and precipitation scores
        results = session.query(Measurement.date, Measurement.prcp).\
                  filter(Measurement.date >= prev_year).\
                  all()
        precipitation = list(np.ravel(results))
        return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations(): 
    """Return a JSON list of stations from the dataset"""
    all_stations = session.query(Station.station).all()
    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def total_observation():
    """Return a JSON list of stations from the dataset"""
    active_stations = session.query(Station.station, func.count(Measurement.station).label('actives')).\
                  filter(Station.station == Measurement.station).\
                  group_by(Station.station).\
                  order_by(func.count(Measurement.station).desc()).\
                  all()
    return jsonify(active_stations)
@app.route("/api/v1.0/<start>/")
def start():
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
       When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
       When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive."""
    return()
@app.route("/api/v1.0/<start>/<end>")
def startend():
    return()



if __name__ == '__main__':
    app.run(debug=True)
# /
#         Home page.
#         List all routes that are available.
# /api/v1.0/precipitation
#         Convert the query results to a Dictionary using date as the key and prcp as the value.
#         Return the JSON representation of your dictionary.
# /api/v1.0/stations
#         Return a JSON list of stations from the dataset.
# /api/v1.0/tobs
#         query for the dates and temperature observations from a year from the last data point.
#         Return a JSON list of Temperature Observations (tobs) for the previous year.
# /api/v1.0/<start> and /api/v1.0/<start>/<end>
#         Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#         When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#         When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.