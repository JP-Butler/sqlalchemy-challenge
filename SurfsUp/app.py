# Import the dependencies.
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import timedelta


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
# reference variable for measurement table
measurement_table = Base.classes.measurement
# reference variable for station table
station_table = Base.classes.station




#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
 
@app.route('/')
def welcome():
    #list availible apis
    return(
        f"Welcome to the Climate App!<br>"
        f"Available Routes below:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt;<br>"
    )

# define precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    year_prior_dt = dt.date(2017,8,23) - dt.timedelta(days=365)
    data_results = session.query(measurement_table.date, measurement_table.prcp).filter\
    (measurement_table.date >= year_prior_dt).all()

    precip_data = {}
    for date, prcp in data_results:
        precip_data[date] = prcp
    
    session.close()
    return jsonify(precip_data)


# define stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    station_list = session.query(station_table.station, station_table.name, \
                                 station_table.latitude, station_table.longitude, \
                                 station_table.elevation).all()

    all_stations = list(np.ravel(station_list))
    
    session.close()
    return jsonify({"list of available stations" : all_stations})
    #return jsonify(list_of_available_stations = all_stations)
# Create our session (link) from Python to the DB



if __name__ == '__main__':
    app.run(debug=True)