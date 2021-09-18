import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import csv
tags = []

for page in range (150): #There is 150 chapters

	r = requests.get(f'https://gatemanga.com/ar/solo-leveling/%d8%a7%d9%84%d9%81%d8%b5%d9%84-{page}/?style=list%27')

	soup = BeautifulSoup(r.content, 'html.parser')

	ancher = soup.find_all('div', {'class':'page-break'})
	for pt in ancher:
		img_tag = pt.find('img')
		link = img_tag.get('data-src').strip()
		name = img_tag.get('id')

		with open (name +'.jpg', 'wb') as f:
			im = requests.get(link)
			f.write(im.content)

#This Script can run on most of manga websites you just need to change the url