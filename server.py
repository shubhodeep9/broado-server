from flask import Flask, session, render_template, g
## you did not import "request"
from flask import request, jsonify
import requests
import json
import os
import urllib2
import simplejson as jsons
from flask import Response
import sqlite3

app = Flask(__name__)

DATABASE = 'DB/broado.db'
DEBUG = True

app.secret_key = os.urandom(24)
app.config.from_object(__name__)
app.config.from_envvar('TRAVELSAFE_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/api', methods=['GET','POST'])
def api():
    js = []
    c=0
    img_url = request.args.get('img',0)
    url = 'http://apius.faceplusplus.com/v2/detection/detect?api_key=e2707513a30c55f950583457e8845ec1&api_secret=9cWd6oDOtFMmqhGT7mwPKphefakx52tI&url='+str(img_url)
    page = urllib2.urlopen(url)
    data = json.load(page)
    for i in range(len(data['face'])):
        latitude = request.args.get('latitude', 0, type = float)
        longitude = request.args.get('longitude', 0 , type = float)
        gender= data['face'][i]['attribute']['gender']['value']
        age = data['face'][i]['attribute']['age']['value']
        def getAgeCategory():
        	age = data['face'][i]['attribute']['age']['value']
        	if(age>55):
        		ageCategory = "Old Age"
        	if(age>20 and age<56):
        		ageCategory = "Youth"
    		if(age>12 and age<21):
    			ageCategory = "Teenager"
    		if(age<12):
    		    ageCategory = "Kids"

    		return ageCategory
        def rating():
        	smiling = data['face'][i]['attribute']['smiling']['value']
        	if(smiling>75):
        		rate=5
        	if(smiling>61 and smiling<76):
        		rate=4
        	if(smiling>50 and smiling<62):
        		rate=3
        	if(smiling>35 and smiling<15):
        		rate=2
        	elif(smiling<15):
        		rate=1
        	return rate

        def givePlaceName():
            url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&sensor=true'
            page = urllib2.urlopen(url)
            data = json.load(page)
            address = data['results'][0]['formatted_address']
            return address
        rate1 = rating()
        ageCategory = getAgeCategory()
        address = givePlaceName()
        g.db.execute('insert into upload (img_url,ageCategory,latitude,longitude,rating,gender,location) values (?,?,?,?,?,?,?)',[img_url,ageCategory,latitude,longitude,rate1,gender,address])
        g.db.commit()

    return 'yo'

@app.route('/travelApi', methods=['GET','POST'])
def travel():
    location = request.args.get('location',0)
    location = location.title()
    recommend = g.db.execute('select * from location where city = ?',[location])
    js = []
    locals = []
    for row in recommend.fetchall():
        locals.append(row[2].replace(' ',''))

    ways = '|'.join(locals)
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+location+'&destination='+location+'&waypoints=optimize:true|'+ways+'&key=AIzaSyDVYEzlC_MuzKNDIwWzipvny3dkf4nSBVo'
    page = urllib2.urlopen(url)
    data = json.load(page)
    for i in range(len(data['routes'][0]['legs'])):
        start = data['routes'][0]['legs'][i]['start_address']
        duration = data['routes'][0]['legs'][i]['duration']['text']
        distance = data['routes'][0]['legs'][i]['distance']['text']
        end = data['routes'][0]['legs'][i]['end_address']
        r = json.loads(json.dumps({'start':start, 'duration':duration, 'distance':distance, 'end':end}, sort_keys = False,indent=4, separators=(',', ': ')))
        js.append(r)
    return jsonify(nearby=js)

@app.route('/eudgetApi', methods =['GET','POST'])
def getbudget():
    budget = requests.args.get('budget', 5000, type = int)
    living = requests.args.get('living', type = str)
    if(living=='royale'):
        hotels = g.db.execute('select * from hotels where living=royale')
        #Display data
    elif(living=='normal'):
        hotels = g.db.execute('select * from hotels where living=normal')
        #display data
    elif (living=='low'):
        hotels = g.db.execute('select * from hotels where living=low')

        #Display data

    #finally, send all the data in json...(Hotel selected based upon the rating..)
if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    ## keep the debug mode on in flask - it helps
    app.run(host='0.0.0.0', port= port, debug=True)
