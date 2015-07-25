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
        rate1 = rating()
        ageCategory = getAgeCategory()
        r = json.loads(json.dumps({'gender':gender, 'rating':rate1, 'ageCategory': ageCategory}, sort_keys = True,indent=4, separators=(',', ': ')))
        js.append(r)
        c=c+1
    return jsonify(results=js)

@app.route('/travelRecommender', methods=['GET','POST'])
def city():
    location = request.args.get('location',0)
    location = location.lower()
    if(location=='bangalore'):
        url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+location+'&destination='+location+'&waypoints=optimize:true|CubbonPark|LalBagh|ISCKONTemple|BangalorePalace|Wonderla|OrionMall&key=AIzaSyDVYEzlC_MuzKNDIwWzipvny3dkf4nSBVo'
        page = urllib2.urlopen(url)
        data = json.load(page)
        return jsonify(data=data)

@app.route('/travelApi', methods=['GET','POST'])
def travel():
    location = request.args.get('location',0)
    location = location.title()
    recommend = g.db.execute('select * from location where city = ?',[location])
    locals = []
    for row in recommend.fetchall():
        locals.append(row[2].replace(' ',''))

    ways = '|'.join(locals)
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin='+location+'&destination='+location+'&waypoints=optimize:true|'+ways+'&key=AIzaSyDVYEzlC_MuzKNDIwWzipvny3dkf4nSBVo'
    page = urllib2.urlopen(url)
    data = json.load(page)
    return url


if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    ## keep the debug mode on in flask - it helps
    app.run(host='0.0.0.0', port= port, debug=True)
