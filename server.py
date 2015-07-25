from flask import Flask, session, render_template
## you did not import "request"
from flask import request, jsonify
import requests
import json
import os
import urllib2

app = Flask(__name__)

app.secret_key = os.urandom(24)

@app.route('/api', methods=['GET','POST'])
def api():
    img_url = request.args.get('img',0)
    url = 'http://apius.faceplusplus.com/v2/detection/detect?api_key=e2707513a30c55f950583457e8845ec1&api_secret=9cWd6oDOtFMmqhGT7mwPKphefakx52tI&url='+str(img_url)
    page = urllib2.urlopen(url)
    data = json.load(page)
    gender= data['face'][0]['attribute']['gender']['value']
    smiling = data['face'][0]['attribute']['smiling']['value']
    return jsonify(gender=gender, smile=smiling)

if __name__ == '__main__':
    port = int(os.environ.get('PORT',5000))
    ## keep the debug mode on in flask - it helps
    app.run(host='0.0.0.0', port= port, debug=True)
