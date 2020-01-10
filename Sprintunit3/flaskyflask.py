from flask import Flask
import openaq

APP = Flask(__name__)

#Part 1:

@APP.route('/')
def root():
    """Base view."""
    api = openaq.OpenAQ()
    status, body = api.measurements(city='Los Angeles', parameter='pm25')#This is the request we want. 
    mytupl=[]
    for body_data in body['results']:
        datedata=body_data['date']
        val=body_data['value']
        utc_datetime=datedata['utc']
        mytupl.append((utc_datetime,val)) 
    return str(mytupl)

# #Part 2: work
# api = openaq.OpenAQ()
# # status, body = api.cities()
# #Did the thing locally!
# status, body = api.measurements(city='Los Angeles', parameter='pm25')#This is the request we want. 

# mytupl=[]

# for body_data in body['results']:
#     datedata=body_data['date']
#     val=body_data['value']
#     utc_datetime=datedata['utc']
#     mytupl.append((utc_datetime,val))
# print(mytupl)       

# # firstlist=body['results']
# # print(firstlist)

from flask_sqlalchemy import SQLAlchemy

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Time {}>'.format(self.datetime)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    DB.session.commit()
    return 'Data refreshed!'