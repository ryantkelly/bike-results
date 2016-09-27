import requests, sys, csv, json
from bs4 import BeautifulSoup

# todo:
# 	This will not work well for events with multiple days, like KMC, as each field/day is considered it's own field on crossresults. So...fix that?

# Here is the stuff for you to define!
writer = csv.writer(open('output.csv', 'w')) # Change the name of the output file if you want
payload = {'url': 'http://www.bikereg.com/Confirmed/32269'} # Enter the confirmed riders URL from BikeReg to send to Cross Results

predictor = 'https://www.crossresults.com/predictor.aspx'
ignore = ['WAITLIST', 'Tent', 'Wait'] #words in categories you want to ignore

r = requests.get(predictor, params=payload)
if r.status_code != 200:
	print 'whoops' + r.status_code
	sys.exit()

soup = BeautifulSoup(r.text, 'html.parser')
registered = {}
for category in soup.find_all('span', class_='categoryname'):
	if any(x in category.text for x in ignore):
		continue
	ctext = category.text.encode('ascii', 'ignore')
	print ctext
	payload['cat'] = ctext
	r = requests.get(predictor, params=payload)
	j = json.loads(r.text)
	for racer in j:
		registered.setdefault((racer['firstname']+' '+racer['lastname']).encode('ascii', 'ignore'), []).append(ctext)
	
for r in (sorted(registered, key=lambda r: len(registered[r]), reverse=True)):
	if len(registered[r])>1:
		l = registered[r]
		l.insert(0, r)
		writer.writerow(l)
