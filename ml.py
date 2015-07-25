import urllib2
import io, json
from bs4 import BeautifulSoup
regno = raw_input('Enter Registration number whose gender you want to know :')
url = 'http://apius.faceplusplus.com/v2/detection/detect?api_key=e2707513a30c55f950583457e8845ec1&api_secret=9cWd6oDOtFMmqhGT7mwPKphefakx52tI&url=https%3A%2F%2Facademics.vit.ac.in%2Fstudent%2Fview_photo_2.asp%3Frgno%3D'+str(regno)+'&attribute=age%2Cgender%2Crace%2Csmiling%2Cpose%2Cglass'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read()).get_text()
#print soup
data = soup
with open('data.json', 'w') as outfile:
     json.dump(data, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
content = json.loads(soup)
with open('data.json') as da:
	data = json.loads(json.load(da))
gender= data['face'][0]['attribute']['gender']['value']
print 'Gender of '+ str(regno) + 'i s : ' +gender
smiling = data['face'][0]['attribute']['smiling']['value']
print smiling
if(smiling>65):
	print smiling
	print 'And this person has a smiling face on i-Card'