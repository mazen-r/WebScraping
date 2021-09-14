import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv

filecsv = open('BooksScraper.csv', 'w', encoding='utf8')
csv_columns = ['Name', 'Price' ,'Rating', 'Kind', 'Availbity', 'Img']
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()


for page in range(5):
	print ('----',page,'----')


	url = 'https://books.toscrape.com/catalogue/page-'

	r = requests.get(f'https://books.toscrape.com/catalogue/page-{page}.html')
	soup = BeautifulSoup(r.content, 'html.parser')

	ancher = soup.find_all('li', {'class':'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
	for pt in ancher:

		link = pt.find('a').attrs['href']		
		r2 = requests.get('https://books.toscrape.com/catalogue/'+link)
		soup2 = BeautifulSoup(r2.content, 'html.parser')

		name = soup2.find('div', {'class':'col-sm-6 product_main'}).find('h1').text

		availbity = soup2.find('p', {'class':'instock availability'}).text
		availbity = availbity.strip()[10:-1]

		stars = soup2.find('div', {'class':'col-sm-6 product_main'}).find('p', {'class':'star-rating'}).get('class')
		rating = stars[1]

		cost = soup2.find('p', {'class':'price_color'}).text
		price = float(cost.replace('£', '')) * 1.18
		price = ('$')+str(round(price, 2))

		kind = soup2.find('ul', "breadcrumb").find_all('a')[2].text

		img = soup2.find('div', {'class':'item active'}).img.get('src')
		img = 'https://books.toscrape.com'+img[5:]

		writer.writerow({'Name':name, 'Price':price, 'Rating':rating, 'Kind':kind, 'Availbity':availbity, 'Img':img})


filecsv.close()