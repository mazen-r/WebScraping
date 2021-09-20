import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import csv
import json

filecsv = open('PremierLeagueBot.csv', 'w', encoding='utf8')
csv_columns = ['Rank', 'Club', 'Played', 'Won', 'Drawn', 'Lost', 'GF', 'GA', 'GD', 'Points', 'Next', 'Day', 'Time']
writer = csv.DictWriter(filecsv, fieldnames = csv_columns)
writer.writeheader()


url = 'https://www.premierleague.com/tables'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
ancher = soup.find_all('tr', {'data-compseason':'418'})
for pt in ancher:
	rank = pt.find('td', {'class':'pos button-tooltip'}).find('span', {'class':'value'}).text

	name = pt.find('span', {'class':'long'}).text

	td_tags = pt.find_all('td')

	played = td_tags[3].text
	won = td_tags[4].text
	drawn = td_tags[5].text
	lost = td_tags[6].text
	GF = td_tags[7].text
	GA = td_tags[8].text
	GD = td_tags[9].text.strip()
	points = td_tags[10].text

	next_match = pt.find_all('span', {'class':'teamName'})[1].find('abbr').get('title')

	day = td_tags[12].find('span', {'class':'matchInfo'}).text

	time = pt.find('time').text

	writer.writerow({'Rank':rank, 'Club':name, 'Played':played, 'Won':won, 'Drawn':drawn, 'Lost':lost, 'GF':GF, 'GA':GA, 'GD':GD,
	 'Points':points, 'Next':next_match, 'Day':day, 'Time':time})
filecsv.close()
# This script is Automated to Run every premierleague Night for someone who needs this data to displayed in his cafe