import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import *

#app is available from settings
db = SQLAlchemy(app)

class Guest(db.Model):
    __tablename__ = 'guests'
    barcode_id = db.Column(db.String(100),primary_key=True)
    user_id = db.Column(db.String(100),nullable=False) 
    name = db.Column(db.String(100),nullable=False)
    last_chg_time = db.Column(db.DateTime,default=datetime.datetime.utcnow)
    
    def json(self):
        return {'name':self.name,'barcode_id': self.barcode_id,'user_id':self.user_id}

    def add_guest(_name,_barcode_id,_userid):
        newGuest = Guest(name=_name,barcode_id=_barcode_id,user_id=_userid)
        print (newGuest)
        db.session.add(newGuest)
        db.session.commit()

    def get_guests():
        return [ Guest.json(guest) for guest in Guest.query.all()]

    def get_guest(_barcode_id):
        guest = Guest.query.filter_by(barcode_id=_barcode_id).first() 
        print (guest)
        return Guest.json(guest)
    
    def check_guest(_barcode_id):
        guest = Guest.query.filter_by(barcode_id=_barcode_id).first() 
        print (guest)
        if guest:
            return "valid"
        else:
            return "not_valid"
    
    def delete_guest(_barcode_id):
        try:
            Guest.query.filter_by(barcode_id=_barcode_id).delete()
            db.session.commit()
            return "done"
        except:
            return "error"

    def update_guest_info(_barcode_id,_name,_userid):
        guest_to_update = Guest.query.filter_by(barcode_id=_barcode_id).first()
        guest_to_update.user_id = _userid
        guest_to_update.name = _name
        db.session.commit()
    
    def __repr__(self):
        guest_obj = {
            'name':self.name,
            'barcode_id':self.barcode_id,
            'user_id':self.user_id
        }
        return json.dumps(guest_obj)