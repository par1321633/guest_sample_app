
from flask import Flask,jsonify,request,Response,make_response
import json

from settings import *

from guestModel import *
from guestAttendence import *

import pyexcel as pe
import pandas as pd 
import mysql.connector
import numpy as np

print(__name__) # print __main__

#decorator bind a function 
@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/guests')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def fetch_guests():
    #return jsonify({'Guests' : guests})
    return jsonify({'Guests' : Guest.get_guests()})

@app.route('/guest/<_barcode>') #type cast isbn passed to int
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_guest_by_barcode(_barcode):
    print (_barcode)
    if Guest.get_guest(_barcode):
        return jsonify(Guest.get_guest(_barcode))
    else:
        return "Not a Valid a Barcode Id....!!"


@app.route('/add_guest',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def add_guest():
    request_data = request.get_json()
    print (request_data['name'],request_data['barcode_id'],request_data['user_id'])
    Guest.add_guest(request_data['name'],request_data['barcode_id'],request_data['user_id'])
    response =  Response("",201,mimetype='application/json')
    response.headers['Location'] = "/guest/" + str(request_data['barcode_id'])
    return response

@app.route('/guest/<barcode>',methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def update_guest(barcode):
    new_data =  (request.get_json())
    print (new_data)
    Guest.update_guest_info(barcode,new_data['name'],new_data['user_id'])
    response = Response("",status=204)
    return "Done"


@app.route('/guest/<barcode>',methods=['DELETE'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def delete_barcode(barcode):
    print (barcode)
    try:
        Guest.delete_guest(barcode)
        return Response("",status=204)
    except:
        invalidBookObjectMsg= {
            "error":"No book find for provided ISBN"
        }
        return Response(json.dumps(invalidBookObjectMsg),status=400,mimetype='application/json')

@app.route('/add_guest_attendence',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def add_guest_attendence():
    request_data = request.get_json()
    print (request_data['entry_point'],request_data['barcode_id'],request_data['user_id'])
    Guest_Attendence.add_attendence(request_data['barcode_id'],request_data['user_id'],request_data['entry_point'])
    response =  Response("",201,mimetype='application/json')
    response.headers['Location'] = "/guest/" + str(request_data['barcode_id'])
    return response

@app.route('/guest_attendence/<barcode>',methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def get_guest_info(barcode):
    print (barcode)
    if Guest.check_guest(barcode) == "valid":
        return jsonify(Guest_Attendence.get_guest_attendence(barcode))
    else:
        return "Not a Valid a Barcode Id....!!"


@app.route('/download')
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def download():
    mydb = mysql.connector.connect(host="localhost",user="root",
        passwd="Par123", database="prezotech") 
    sql_select="""
    select b.*,a.name from
    guests a join guests_attendence b 
    on a.barcode_id=b.barcode_id 
    where date(b.entry_time)=curdate()
    """
    mycursor = mydb.cursor()
    mycursor.execute(sql_select)
    col=['barcode_id','user_id','entry_point','attendance','name']
    df = pd.DataFrame(mycursor.fetchall())
    df.columns=col
    df = df.pivot_table(index=['barcode_id','user_id','name'],columns='entry_point',values='attendance',aggfunc='first')
    df.replace(np.NaN,'-',inplace=True)
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

app.run(port=5000)
