import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

from flask import Flask, jsonify

from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f'Here are the following routes:</br>'
        '<a href=http://127.0.0.1:5000/api/v1.0/precipitation>/api/v1.0/precipitation</a></br>'
        '<a href=http://127.0.0.1:5000/api/v1.0/stations>api/v1.0/stations</api/v1.0/stations</a></br>'
        '<a href=http://127.0.0.1:5000/api/v1.0/tobs>/api/v1.0/tobs</a></br>'
        '/api/v1.0/start</br>'
        '/api/v1.0/start/end')

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    year_prcp = session.query(Measurement.prcp, Measurement.date).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    session.close()

    all_prcp = []
    for prcp, date in year_prcp:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    query = sqlalchemy.select(Station)

    result = engine.execute(query).fetchall()

    session.close()

    all_stations = []
    for latitude, id, elevation, station, name, longitude in result:
        station_dict = {}
        station_dict["latitude"] = latitude
        station_dict["id"] = id
        station_dict["elevation"] = elevation
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["longtitude"] = longitude
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    query = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()

    session.close()

    all_prcp = []
    for prcp, date in query:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    avg_tobs = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    max_tobs = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    min_tobs = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).all()


    session.close()

    avg_temp = list(np.ravel(avg_tobs))
    max_temp = list(np.ravel(max_tobs))
    min_temp = list(np.ravel(min_tobs))


    return f"Average Temperature: {avg_temp} Maximum Temperature: {max_temp} Minimum Temperature: {min_temp}" 

@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    session = Session(engine)
    avg_tobs = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    max_tobs = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    min_tobs = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()


    session.close()

    avg_temp = list(np.ravel(avg_tobs))
    max_temp = list(np.ravel(max_tobs))
    min_temp = list(np.ravel(min_tobs))

    return f"Average Temperature: {avg_temp} Maximum Temperature: {max_temp} Minimum Temperature: {min_temp}" 


if __name__ == "__main__":

    app.run(debug=True)