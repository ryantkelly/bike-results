import requests, sys, csv, json
from bs4 import BeautifulSoup

# todo: 
#	write actual error handling I guess
#	option to output to different files by category
#	also yes my code is crap, why don't you go munch my butt

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


# Here is the stuff for you to define!
writer = csv.writer(open('output.csv', 'w')) # Change the name of the output file if you want
payload = {'url': 'https://www.bikereg.com/Confirmed/32407'} # Enter the confirmed riders URL from BikeReg to send to Cross Results
validYears = [str(2015), str(2016)] # Define the years of results you want to get - here, 2015 and 2016
predictorDepth = 4 # 0-indexed of the max predicting placing you care about - default is 4, therefore the top 5 predicted's riders results will be returned
maxPlacing = 10 # 0-indexed. Max placing for riders results you care about. So, rider's top five results returned.

predictor = 'https://www.crossresults.com/predictor.aspx'
historyUrl = 'https://www.crossresults.com/racer/'
ignore = ['WAITLIST', 'Tent', 'tent', 'Wait', 'Club', 'Expo', 'Credit', 'Parking', 'Preview', 'Pre-ride'] #words in categories you want to ignore

r = requests.get(predictor, params=payload)
if r.status_code != 200:
	print 'whoops' + r.status_code
	sys.exit()

soup = BeautifulSoup(r.text, 'html.parser')
for category in soup.find_all('span', class_='categoryname'):
	if any(x in category.text for x in ignore):
		continue
	print category.text
	payload['cat'] = category['raceid']
	r = requests.get(predictor, params=payload)
	j = json.loads(r.text)
	sort = {}
	for racer in j:
		sort[racer['points']] = [racer['firstname']+' '+racer['lastname'], racer['id']]
	c = 0
	for key in sorted(sort):
		history_request = requests.get(historyUrl+str(sort[key][1]))
		if history_request.status_code != 200:
			print 'whoops' + r.status_code
			break
		history_soup = BeautifulSoup(history_request.text, 'html.parser')
		yc = 0
		for year in history_soup.find_all('div', class_='headerrow1'):
			shortyear = year.text[:5].strip()
			if shortyear in validYears:
				table = history_soup.find_all('table', class_='datatable1')[yc]
				for tr in table.find_all('tr', class_=['datarow2', 'datarow1']):
					td = tr.find_all('td')
					place = td[4].text.strip()
					if is_number(place) and int(place) <= maxPlacing:
						arr = [category.text, sort[key][0], shortyear, td[1].text.strip(), td[2].text.strip(), place]
						try:
							writer.writerow(arr)
						except UnicodeEncodeError:
							print "Unicode error on page "+historyUrl+str(sort[key][1])
			yc = yc + 1		
		
		c = c + 1
		if c > predictorDepth:
			break
