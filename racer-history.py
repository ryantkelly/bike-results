import requests, sys, csv, json, argparse
from bs4 import BeautifulSoup
from pprint import pprint


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

parser = argparse.ArgumentParser('Compile racer history for announcing')
parser.add_argument('--years', help="Comma-separated list of years to include", required=True)
parser.add_argument('--type', help="Event type", choices=['road','cross'], required=True)
parser.add_argument('--predictor_depth', help="Depth of predicted finish", default=9)
parser.add_argument('--results_depth', help="Depth of results", default=4)
parser.add_argument('--event_id', help="BikeReg Event ID", required=True)

args = parser.parse_args()

payload = {'url': 'https://www.bikereg.com/Confirmed/'+args.event_id}
valid_years = [y.strip(' ') for y in args.years.split(',')] # Define the years of results you want to get - here, 2015 and 2016
predictor_depth = args.predictor_depth
max_placing = args.results_depth
results_type = args.type

if results_type == "road":
	predictor = 'https://www.road-results.com/predictor.aspx'
	historyUrl = 'https://www.road-results.com/racer/'
elif results_type == "cross":
	predictor = 'https://www.crossresults.com/predictor.aspx'
	historyUrl = 'https://www.crossresults.com/racer/'

ignore = ['WAITLIST', 'Tent', 'tent', 'Wait', 'Club', 'Expo', 'Credit', 'Parking', 'Preview', 'Pre-ride', 'Intro'] #words in categories you want to ignore

r = requests.get(predictor, params=payload)
if r.status_code != 200:
	print ('whoops' + r.status_code)
	sys.exit()

soup = BeautifulSoup(r.text, 'html.parser')
for category in soup.find_all('span', class_='categoryname'):
	if any(x in category.text for x in ignore):
		continue
	print(category.text)
	writer = csv.writer(open('output/'+category.text.replace('/', '-').replace(':', '-')+'.csv', 'w'))
	payload['cat'] = category['raceid']
	r = requests.get(predictor, params=payload)
	sort = {}
	
	if results_type == "cross":
		j = r.json()
		for racer in j:
			sort[racer['points']] = [racer['firstname']+' '+racer['lastname'], racer['id']]
	elif results_type == "road":
		p_soup = BeautifulSoup(r.text,'html.parser')
		for row in p_soup.find_all('tr', class_=['datarow1','datarow2','datarow3']):
			cell = row.find_all('td')
			l = []
			try:
				_id = cell[0].find('a')['href'].split('rID=')[1]
			except TypeError:
				_id = ""
			sort[cell[2].text.strip()] = [cell[0].text.split('. ')[1], _id]
	c = 0
	for key in sorted(sort):
		history_request = requests.get(historyUrl+str(sort[key][1]))
		
		if history_request.status_code != 200:
			print('whoops' + str(r.status_code))
			break
		history_soup = BeautifulSoup(history_request.text, 'html.parser')
		
		if results_type == "cross":
			yc = 0
			for year in history_soup.find_all('div', class_='headerrow1'):
				shortyear = year.text[:5].strip()
				if shortyear in valid_years:
					table = history_soup.find_all('table', class_='datatable1')[yc]
					for tr in table.find_all('tr', class_=['datarow3', 'datarow2', 'datarow1']):
						td = tr.find_all('td')
						place = td[4].text.strip()
						if is_number(place) and int(place) <= max_placing:
							# category.text
							arr = [sort[key][0], shortyear, td[1].text.strip(), td[2].text.strip(), place]
							try:
								writer.writerow(arr)
							except UnicodeEncodeError:
								print("Unicode error on page "+historyUrl+str(sort[key][1]))
				yc = yc + 1	
		elif results_type == "road":
			yc = 0
			years = history_soup.find_all('div', class_='monthContent')
			for header in history_soup.find_all('a', class_='expandMonth'):
				shortyear = header.text.split(' - ')[0].strip()
				if shortyear in valid_years:
					table = years[yc]
					for tr in table.find_all('tr', class_=['datarow3', 'datarow2', 'datarow1']):
						td = tr.find_all('td')
						try:
							place = td[4].text.strip()
						except IndexError:
							pprint(tr)
						if is_number(place) and int(place) <= max_placing:
							# category.text
							arr = [sort[key][0], shortyear, td[1].text.strip(), td[2].text.strip(), place]
							try:
								writer.writerow(arr)
							except UnicodeEncodeError:
								print("Unicode error on page "+historyUrl+str(sort[key][1]))
				yc+=1

		c = c + 1
		if c > predictor_depth:
			break
