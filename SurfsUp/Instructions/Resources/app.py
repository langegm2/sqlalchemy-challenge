import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine)

measurement = Base.classes.measurement
Station = Base.classes.Station
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
        return (
            f"Welcome to the Hawaii climate analysis API <br/>",
            f"available routes: <br/>",
            f"/api/v1.0/precipitation<br/>",
            f"/api/v1.0/tobs<br/>",
            f"/api/v1.0/temp/start<br/>",
            f"/api/v1.0/temp/start/end<br/>",
            f"<p>'start' and 'end' date should be in the format MMDDYYYY.</p>"
        )
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= prev_year).all()
    session.close()

    precip = {date: prcp for date, prcp in precipitation}

    return jsonsify(precip)

@app.route("/api/v1.0/stations")
def stations():
        results = session.query(Station.station).all()
        session.close()

        stations = list(np.ravel(results))
        return jsonify(stations = stations)
        
 @app.route("/api/v1.0/tobs")
def temp_monthly():
        prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)      

    results = session.query(measurement.tobs).\
        filter(measurement.station == 'usc00519281').\
        filter(measurement.date >= prev_year).all()
    session.close() 

    temps = list(np.ravel(results))
    return jsonify (temps=temps)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def  stats(start=None, end=None):

    sel = [func.min(measurement.tobs, func.avg(measurement.tobs), func.measurement.tobs)] 

        if not end:
                start = dt.datetime.strptime(start, "%m%d%Y") 
                results = session.query(*sel).\
                    filter(measurement.date>= start).all()

                    session.close()

        temps = list(np.ravel(results))
        return jsonify(temps= temps) 

        start = dt.datetime.strptime(start, "%m%d%Y")  
        end = dt.datetime.strptime(end, "%m%d%Y")
        
        results = session.query(*sel).\
            filter(measurement.date >= start)
            filter(measurement.date <= end).all()

        session.close()

        temps = list(np.ravel(results))

        return jsonify(temps = temps)



if __name__ == "__main__":
        app.run(debug = true)

