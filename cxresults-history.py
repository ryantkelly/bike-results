import requests, sys, csv, json
from bs4 import BeautifulSoup

# todo: 
#	write actual error handling I guess
#	option to output to different files by category
#	option to define what results of top riders you want
#	also yes my code is crap, why don't you go munch my butt


# Here is the stuff for you to define!
writer = csv.writer(open('output.csv', 'w')) # Change the name of the output file if you want
payload = {'url': 'https://www.bikereg.com/Confirmed/31266'} # Enter the confirmed riders URL from BikeReg to send to Cross Results
validYears = [str(2015), str(2016)] # Define the years of results you want to get - here, 2015 and 2016
maxplacing = 4 # 0-indexed of the max placing you care about - default is 4, therefore the top 5 predicted's riders results will be returned

predictor = 'https://www.crossresults.com/predictor.aspx'
historyUrl = 'https://www.crossresults.com/racer/'

r = requests.get(predictor, params=payload)
if r.status_code != 200:
	print 'whoops' + r.status_code
	sys.exit()

soup = BeautifulSoup(r.text, 'html.parser')
for category in soup.find_all('span', class_='categoryname'):
	print category.text
	payload['cat'] = category.text
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
				for tr in table.find_all('tr', class_='datarow1'):
					td = tr.find_all('td')
					arr = [category.text, sort[key][0], shortyear, td[1].text.strip(), td[2].text.strip(), td[4].text.strip()]
					try:
						writer.writerow(arr)
					except UnicodeEncodeError:
						print "Unicode error on page "+historyUrl+str(sort[key][1])
			yc = yc + 1		
		
		c = c + 1
		if c > maxplacing:
			break
