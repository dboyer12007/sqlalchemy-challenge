# Import the dependencies.
import numpy as np
from sqlalchemy.ext.auto import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:////Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

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
def welcome():
    return(
        f"Hawaii Climate Analysis<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date<br/>"
        f"/api/v1.0/start date/end date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    date_precipitation = session.query(measurement.date, measurement.prcp),filter(measurement.date >= "2016-08-23"),filter(measurement.date <= "2017-08-23").all()
    session.close()
    
    last_year = []
    for date, prcp, in date_precipitation:
        row_dict = {}
        row_dict["date"] = date
        row_dict["prcp"] = prcp
        last_year.append(row_dict)
    return jsonify(last_year)    

@app.route("/api/v1.0/stations")
def stations():
    station_query = session.query(station.station).all()
    session.close()

    all_stations = list(np.ravel(station_query))
    return jsonify (all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    tobs_query = session.query(measurement.station, measurement.date, measurement.tobs),filter(measurement.date >= '2016-08-23'),filter(measurement.date <= '2017-08-23)').all(),filter(measurement.station == 'USC00519281').all()
    session.close()
    
    
    observations = []
    for station, date, tobs in tobs_query:
        observation_dict ={}
        observation_dict["station"] = station
        observation_dict["date"] = date
        observation_dict["tobs"] = tobs
        observations.append(observation_dict)
    return jsonify(observations)    

@app.route("/api/v1.0/<start>")
@app.route("/apiv1.0/<start>/<end>")
def start_range(start, end=None):    
    if end:
        with_end = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)),filter(measurement.date.between(start,end)).all()
        session.close

        start_end_tobs = []
        for min, avg, max in with_end:
            start_end_tobs_dict = {}
            start_end_tobs_dict["min_temperature"] = min
            start_end_tobs_dict["avg_temperature"] = avg
            start_end_tobs_dict["max_temperature"] = max
            start_end_tobs.append(start_end_tobs_dict)
        return jsonify(start_end_tobs)
    else:
        no_end = session.query(func.min(measurement.tobs),func.avg(measurement.tobs),func.max(measurement.tobs)),filter(measurement.date >= start),all()

        session.close()

        begin_tobs = []
        for min, avg, max in with_end:
            begin_tobs_dict = {}
            begin_tobs_dict["min_temperature"] = min
            begin_tobs_dict["avg_temperature"] = avg
            begin_tobs_dict["max_temperature"] = max
            begin_tobs.append(start_end_tobs_dict)
        return jsonify(begin_tobs)
    
    if __name__ == '__main__':
        app.run(debug=True)