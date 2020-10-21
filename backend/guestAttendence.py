import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import *

#app is available from settings
db = SQLAlchemy(app)

class Guest_Attendence(db.Model):
    __tablename__ = 'guests_attendence'
    barcode_id = db.Column(db.String(100),primary_key=True)
    user_id = db.Column(db.String(100),nullable=False) 
    entry_point = db.Column(db.String(100),nullable=False,primary_key=True)
    entry_time = db.Column(db.DateTime,primary_key=True,default=datetime.datetime.utcnow)
    
    def json(self):
        return {'entry_point':self.entry_point,'entry_time':self.entry_time.strftime('%d-%m-%Y %H:%M:%S'),'barcode_id': self.barcode_id,'user_id':self.user_id}
        

    def myconverter(self,o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


    def add_attendence(_barcode_id,_userid,_entry_point):
        newGuestAttendence = Guest_Attendence(barcode_id=_barcode_id,user_id=_userid,entry_point=_entry_point)
        db.session.add(newGuestAttendence)
        db.session.commit()

    def get_guests_attendence_info():
        return [ Guest_Attendence.json(Guest) for guest in Guest_Attendence.query.all()]

    def get_guest_attendence(barcode_id):
        print (barcode_id)
        guest_info = Guest_Attendence.query.filter_by(barcode_id=barcode_id).all()
        print (guest_info)
        return [ Guest_Attendence.json(guest_info) for guest_info in guest_info]
        
    def delete_guest_attendence(_barcode_id,_entry_point,_entry_time):
        try:
            Guest_Attendence.query.filter_by(barcode_id=_barcode_id,entry_point=_entry_point,entry_time=_entry_time).delete()
            db.session.commit()
            return "done"
        except:
            return "error"

 
    def __repr__(self):
        guest_obj = {
            'barcode_id':self.barcode_id,
            'user_id':self.user_id,
            'entry_point':self.entry_point,
            'entry_time':self.entry_time.strftime('%d-%m-%Y %H:%M:%S')
        }
        return json.dumps(guest_obj)