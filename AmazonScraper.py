import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv

filecsv = open('AmazonScraper.csv', 'w', encoding='utf8')
csv_columns = ['Name', 'Price' ,'Rating', 'Img']
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()

for page in range (5):

	r = requests.get(f'https://www.amazon.eg/-/en/s?k=laptop&i=electronics&rh=n%3A21832907031&page={page}')
	soup = BeautifulSoup(r.content, 'html.parser')

	ancher = soup.find_all('div', {'class':'sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20'})
	for pt in ancher:

		name = pt.find('span', {'class':'a-size-base-plus a-color-base a-text-normal'}).text

		element = pt.find('a', {'class':'a-popover-trigger a-declarative'})
		if element:
			rate = element.find_all("i")[0].text[0:3]
		else:
			rate = 'No Rate'

		price_element = pt.find('span', {'class':'a-price-whole'})
		if price_element:
			price = price_element.text[:-1]+str(' EGP')
		else:
			price = ('No Price')

		img = pt.find('img', {'class':'s-image'}).get('src')

		writer.writerow({'Name':name, 'Price':price, 'Rating':rate, 'Img':img})
	