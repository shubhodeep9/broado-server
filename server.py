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

    return jsonify(entries=[2,3])

places_img = {'Chennai': 'https://upload.wikimedia.org/wikipedia/commons/7/73/Chennai_Kathipara_bridge.jpg', 'Mumbai': 'https://upload.wikimedia.org/wikipedia/commons/6/66/Mumbai_skyline88907.jpg','Bangalore':'http://www.discoverbangalore.com/images/Slide1.jpg'}

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
    loc = g.db.execute('select * from location where city = ?',[location])
    bla = []
    des = []
    for row in loc.fetchall():
        bla.append(row[4])
        des.append(row[3])
    bla.append(places_img[location])
    des.append('Hometown')
    for i in range(len(data['routes'][0]['legs'])):
        start = data['routes'][0]['legs'][i]['start_address']
        duration = data['routes'][0]['legs'][i]['duration']['text']
        distance = data['routes'][0]['legs'][i]['distance']['text']
        end = data['routes'][0]['legs'][i]['end_address']
        r = json.loads(json.dumps({'start':start, 'duration':duration, 'distance':distance, 'end':end, 'img': bla[i],'description': des[i]}, sort_keys = False,indent=4, separators=(',', ': ')))
        js.append(r)
    return jsonify(nearby=js)

@app.route('/db')
def db_See():
    sel = g.db.execute('select * from upload')
    see = []
    for i in sel.fetchall():
        see.append(dict(location=i[0],url=i[2]),rating=i[5],gender=i[6],ageCategory=i[7]))
    return jsonify(see=see)

@app.route('/budgetApi', methods =['GET','POST'])
def getbudget():
    city = request.args.get('city',0)
    living = request.args.get('living', 0)
    hot = g.db.execute('select * from hotels where hotel_type=? and hotel_city=?',[living,city.title()])
    hotel = []
    for i in hot.fetchall():
        hotel.append(dict(name=i[1],rating=i[2],facilities=i[3],review=i[4]))

    return jsonify(see=hotel)


@app.route('/ratingApi', methods =["GET","POST"])
def getRating():
    sum=0
    counter = 0
    latitude = request.args.get('latitude', 0, type = float)
    longitude = request.args.get('longitude', 0 , type = float)
    url = 'http://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&sensor=true'
    page = urllib2.urlopen(url)
    data = json.load(page)
    age = {'old_age':0,'youth':0,'teen':0,'kids':0}
    address = data['results'][0]['formatted_address']
    query = g.db.execute('SELECT * from upload where location =?',[address])
    for i in query.fetchall():
        sum=sum+int(i[5])
        if(str(i[7])=='Old Age'):
            age['old_age']=age['old_age']+1
        elif(str(i[7])=='Youth'):
            age['youth']=age['youth']+1
        elif(str(i[7])=='Teenager'):
            age['teen']=age['teen']+1
        elif(str(i[7])=='Kids'):
            age['kids']=age['kids']+1

        counter=counter+1
    age_group = ''
    if (age['old_age']>age['youth'] and age['old_age']>age['teen'] and age['old_age']>age['kids']):
        age_group = "Old Age"
    elif(age['youth']>age['old_age'] and age['youth']>age['teen'] and age['youth']>age['kids']):
        age_group = "Kids"
    elif(age['teen']>age['youth'] and age['teen'] > age['kids'] and age['teen'] > age['old_age']):
        age_group = "Teenager"
    elif(age['kids']>age['youth'] and age['kids']>age['teen'] and age['kids']>age['old_age']):
        age_group = "Kids"
    averageRating= float(sum)/float(counter)
    return jsonify(age_group=age_group,rating=averageRating)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    ## keep the debug mode on in flask - it helps
    app.run(host='0.0.0.0', port= port, debug=True)
