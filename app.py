import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>/api/v1.0/< start ></a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>/api/v1.0/< start >/< end ></a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitations():
    print("Inside Precipitation endpoint")

    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    """Return a list of all dates and precipitation measurements"""
    # Query all precipitation measurements
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a Dictionary to show the data
    all_precipitations = []
    for date, prcp in results:
        precipitations_dict = {}
        precipitations_dict["date"] = date
        precipitations_dict["prcp"] = prcp
        all_precipitations.append(precipitations_dict)

    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    
    print("Inside stations endpoint")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Create a list of stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    
    print("Inside TOBS endpoint")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = dt.date(2017, 8, 18)
    twelve_months = relativedelta(months=12)
    one_year_ago_date = last_date - twelve_months
    one_year_ago_date

    """Return a list of TOBS"""
    # Query all stations
    tobs_result = session.query(Measurement.tobs).\
                    filter(Measurement.station == "USC00519281").\
                    filter(Measurement.date >= one_year_ago_date).\
                    all()

    session.close()

    # Create a list of stations
    all_tobs = list(np.ravel(tobs_result))

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def tobs_with_start_date(start):
    print("Inside TOBS endpoint with start date")

    # Create our session (link) from Python to the DB
    session = Session(engine)

    sel = [ Measurement.date, 
            func.min(Measurement.tobs),
            func.avg(Measurement.tobs), 
            func.max(Measurement.tobs)
           ]
    
    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            all()
        
    session.close()

    #all_info = [{"date":result[0], "min":result[1], "avg":result[2], "max":result[3]} for result in results]
    all_data = []
    for x in results:
        all_data.append({'date': x[0],'avg tobs': x[1],'max tobs': x[2],'min tobs': x[3]})

    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)
