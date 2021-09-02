import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
location_name = []
skills = []
Links = []
Salary = []
requirements = []
date = []
page_num = 0

url = f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start=0{page_num}'

r = requests.get(url)
src = r.content
soup = BeautifulSoup(src, 'lxml')



job_titles = soup.find_all('h2', {'class':'css-m604qf'})
company_names = soup.find_all('a', {'class':'css-17s97q8'})
location_names = soup.find_all('span', {'class':'css-5wys0k'})
job_skills = soup.find_all('div', {'class':'css-y4udm8'})
posted_new = soup.find_all('div', {'class':'css-4c4ojb'})
posted_old = soup.find_all('div', {'class':'css-do6t5g'})
posted = [*posted_new, *posted_old]


for i in range(len(job_titles)):
	job_title.append(job_titles[i].text)
	Links.append(job_titles[i].find('a').attrs['href'])
	company_name.append(company_names[i].text)
	location_name.append(location_names[i].text)
	skills.append(job_skills[i].text)
	date_text = posted[i].text.replace('-', '').strip()
	date.append(date_text)


			

for Link in Links:
	url = requests.get(Link)
	src = url.content
	soup = BeautifulSoup(src, 'lxml')
	requirement = soup.find('div', {'class':'css-1t5f0fr'}).ul
	req_text = ''
	for li in requirement.find_all('li'):
		req_text += li.text+'| '
	req_text = req_text[0:-2]
	requirements.append(req_text)


file_list = [job_title, company_name, date, location_name, requirements, Links, requirements]
exported = zip_longest(*file_list)

with open ('D:\Code/Wuzzuf.csv', 'w', encoding='utf8') as myfile:
	wr = csv.writer(myfile)
	wr.writerow(['Job Title', 'Company Name', 'Date','Location Name', 'skills', 'Links', 'Requirements'])
	wr.writerows(exported)
