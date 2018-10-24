from . import app_models as db
import os, hashlib


dbname = os.getenv("INFLUXDB_DATABASE")
measure_name = "record_name"
tag_key = hashlib.md5(str(db.timeset()).encode('utf-8')).hexdigest()


def insert(data=None): 
    data_prepare = [{
        "measurement": measure_name,
        "tags": {
            "record_id": measure_name+"_"+tag_key
        },
        "time": db.timeset(),
        "fields": data
    }]
    try:
        status = db.insert(dbname, data_prepare)
    except Exception as e:
        respon = {
            "status": False,
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "status": status,
            "measurement": measure_name,
            "data": data
        }
        return respon

def delete(tag_id):
    data_prepare={
        "record_id": tag_id
    }
    try:
        status = db.delete(dbname=dbname,
            measurement=measure_name,
            tags=data_prepare)
    except Exception as e:
        respon = {
            "status": False,
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "status": status,
            "measurement": measure_name,
            "data": data_prepare
        }
        return respon

def result():
    try:
        dm = db.query(dbname,"SELECT * FROM "+measure_name)
        data_points = list(dm.get_points(measurement=measure_name))
    except Exception as e:
        respon = {
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "measurement": measure_name,
            "data": data_points
        }
        return respon

def row(tags):
    try:
        dm = db.query(dbname,"SELECT * FROM "+measure_name)
        data_points = list(dm.get_points(measurement=measure_name, tags=tags))
    except Exception as e:
        respon = {
            "messages": str(e)
        }
        return respon
    else:
        respon = {
            "measurement": measure_name,
            "data": data_points
        }
        return respon

