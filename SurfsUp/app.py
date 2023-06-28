# Import the dependencies
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import timedelta, datetime


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
    #list availible api - routes
    return(
        f"<h1>Welcome to the Climate App!<h1/>"
        f"<h2>Available Routes below:<h2/>"
        f"1)&nbsp&nbspPrecipitation data for last 12 months<br>"
        f"/api/v1.0/precipitation<br>"
        f"2)&nbsp&nbspStation list of Hawaii Database<br>"
        f"/api/v1.0/stations<br>"
        f"3)&nbsp&nbspTemperature Observations (tobs) of the most-active station for the previous year of data<br>"
        f"/api/v1.0/tobs<br>"
        f"4)&nbsp&nbspReturn the min, max and average temperature for all dates >= a specific start date<br>"
        f"/api/v1.0/&lt;start&gt;<br>"
        f"5)&nbsp&nbspReturn the min, max and average temperature for all dates between a specific start and end date, inclusive<br>"
        f"/api/v1.0/&lt;start&gt/&lt;end&gt;<br>"
    )

# define precipitation route for precipiation analysis of last 12 months of data
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query DB for precipitation data 
    year_prior_dt = dt.date(2017,8,23) - dt.timedelta(days=365)
    data_results = session.query(measurement_table.date, measurement_table.prcp).filter\
    (measurement_table.date >= year_prior_dt).all()

    precip_data = {}
    for date, prcp in data_results:
        precip_data[date] = prcp
    
    session.close()
    return jsonify(precip_data)


# Define stations route for stations in the DB
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #query DB for station data
    station_list = session.query(station_table.station, station_table.name, \
                                 station_table.latitude, station_table.longitude, \
                                 station_table.elevation).all()

    all_stations = list(np.ravel(station_list))
    
    session.close()
    return jsonify({"list of available stations" : all_stations})
    

# Define Temperature Observations (tobs) route of most active station for previous year
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query lines for tobs of most active station
    active_station_list = session.query(measurement_table.station, 
                          func.count(measurement_table.station))\
                          .group_by(measurement_table.station)\
                          .order_by(func.count(measurement_table.station).desc()).all()
    year_prior_date = dt.date(2017,8,18) - dt.timedelta(days=365)
    tobs_data_results = session.query(measurement_table.date, measurement_table.tobs).filter\
                                 (measurement_table.station == 'USC00519281')\
                                 .filter(measurement_table.date >= year_prior_date).all()

    # Iterate over rows to create list of dictionaries, organized by date
    tobs_list = [{'date': row.date, 'tobs': row.tobs} for row in tobs_data_results]

    #close session & return a JSONified list
    session.close()
    return jsonify(tobs_list)



# Dynamic routes for start date & start/end date parameters
@app.route('/api/v1.0/<start>')
@app.route("/api/v1.0/<start>/<end>")
def tobs_by_date_range(start= None, end= None):

# Create our session (link) from Python to the DB
    session = Session(engine)
    

    # values returned if only start date given
    if end == None:
        #format start_date from string to date type
        start_date = dt.datetime.strptime(start, "%m%d%Y").date()
        #query for temp data(min,max & avg) after and including start_date
        tobs_data = session.query(func.min(measurement_table.tobs), \
                                func.max(measurement_table.tobs), \
                                func.avg(measurement_table.tobs))\
                                .filter(measurement_table.date >= start_date).all()
            
        
        # format data ouput into a list, close session then return a json list
        list_tobs= list(np.ravel(tobs_data))
        session.close()
        return jsonify(list_tobs)
        # Values returned when start & end date provided
    else: 
        #format start & end_date from string to date type
        start_date = dt.datetime.strptime(start, "%m%d%Y").date()
        #query for temp data (min,max & avg) in between and including exact date range
        end_date = dt.datetime.strptime(end, "%m%d%Y").date()
        tobs_data = session.query(func.min(measurement_table.tobs), \
                                func.max(measurement_table.tobs), \
                                func.avg(measurement_table.tobs))\
                                .filter(measurement_table.date >= start_date)\
                                .filter(measurement_table.date <= end_date).all()
            
        # format data ouput into a list, close session then return a json list  
        list_tobs= list(np.ravel(tobs_data))
        session.close()
        return jsonify(list_tobs)



# Run the Flask app in debug mode when script is executed as the main module
if __name__ == '__main__':
    app.run(debug=True)