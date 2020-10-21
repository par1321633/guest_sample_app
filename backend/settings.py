from flask import Flask
from flask_cors import CORS, cross_origin

DB_USERNAME='root'
DB_PASSWORD='Par123'
DB_NAME='prezotech'

app  = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{0}:{1}@localhost:3306/{2}'.format(DB_USERNAME,DB_PASSWORD,DB_NAME)
app.config['SQLALCHEMY_ECHO'] = True


cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})
