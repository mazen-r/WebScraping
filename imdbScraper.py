from bs4 import BeautifulSoup
import requests
import csv
import time


filecsv = open('k700.csv', 'w', encoding='utf8')
csv_columns = ['Name', 'Date' ,'Rate', 'Votes', 'Genre', 'Duration','Type', 'Certificate', 'Episodes', 'Nudity', 'Violence', 'Profanity', 'Alcohol', 'Frightening']
writer = csv.DictWriter(filecsv, fieldnames=csv_columns)
writer.writeheader()

x = 1
s = requests.Session()


for page in range(5755,7000, 50):
    print ('--- page Number', round(page / 50 + 1 - .02), '---')

    try:
        r = requests.get(f'https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_special,short&start={page}&ref_=adv_nxt')
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
    # r = requests.get('https://www.imdb.com/search/title/?title_type=feature,tv_movie,tv_series,tv_episode,tv_special,tv_miniseries,short&adult=include&start={i}&ref_=adv_nxt',
    #     headers=headers)
    

    soup = BeautifulSoup(r.content, 'html.parser')

    
    ancher = soup.find_all('div', {'class':'lister-item mode-advanced'})
    for pt in ancher:

        name = pt.find('h3', {'class':'lister-item-header'}).find('a').text
        print (name)
        dates = pt.find('span', {'class':'lister-item-year text-muted unbold'}).text.replace('(', '').replace(')', '').strip()
        for i in dates.split():
            if i.isdigit():
                date = i

        rates = pt.find('strong')
        if rates:
            rate = rates.text
        else:
            rate = 'No Rate'

        vote = pt.find('span', {'name':'nv'})
        if vote:
            votes = vote.text
        else:
            votes = 'No Votes'

        genre = pt.find('span', {'class':'genre'}).text.strip()
        
        first_link = pt.find('h3', {'class':'lister-item-header'}).find('a').attrs['href']

        try:
            r2 = requests.get('http://imdb.com'+first_link)
        except requests.exceptions.ConnectionError:
            r2.status_code = "Connection refused"

        
        soup2 = BeautifulSoup(r2.content, 'html.parser')

        typeee = soup2.find('span', {'class':'EpisodeNavigationForSeries__EpisodeCountSpan-sc-1aswzzz-3 jbsbnI'})
        if typeee:
            typee = 'Series'

        else:
            typee = 'Film'

        if typee == 'Film':
            episdoes = '-'
        else:
            episdoes = soup2.find('span', {'class':'ipc-title__subtext'}).text
        


        duuration = pt.find('span', {'class':'runtime'})

        if duuration:
            duration = duuration.text[:-3]
        else:
            duration = 'None'


        certificates = soup2.find_all('a', {'class':'ipc-link ipc-link--baseAlt ipc-link--inherit-color TitleBlockMetaData__StyledTextLink-sc-12ein40-1 rgaOW'})
        if len(certificates) == 2:
            certificate = certificates[1].text
            

        else:
            certificate = 'None'
            
        if certificate == 'None':
            second_link = 'None'
        else:

            second_link = certificates[1].attrs['href']

        

        try:
            r3 = requests.get('http://imdb.com'+second_link)
        except requests.exceptions.ConnectionError:
            r3.status_code = "Connection refused"

        # r3 = requests.get('http://imdb.com'+second_link,headers=headers)
        soup3 = BeautifulSoup(r3.content, 'html.parser')

        if certificate == 'None':

            nudity = 'No Rate'
            violence = 'No Rate'
            profanity = 'No Rate'
            alcohol = 'No Rate'
            frightening = 'No Rate'

        else:

            element = soup3.find_all('div', {'class':'advisory-severity-vote__container ipl-zebra-list__item'})
            if element:

                nudity = element[0].find('span')
                if nudity:    
                    nudity = nudity.text
                else:
                    nudity = 'No Rate'

                violence = element[2].find('span')
                if violence:    
                    violence = violence.text
                else:
                    violence = 'No Rate'

                profanity = element[4].find('span')
                if profanity:    
                    profanity = profanity.text
                else:
                    profanity = 'No Rate'

                alcohol = element[6].find('span')
                if alcohol:    
                    alcohol = alcohol.text
                else:
                    alcohol = 'No Rate'

                frightening = element[8].find('span')
                if frightening:    
                    frightening = frightening.text
                else:
                    frightening = 'No Rate'

            else:
                nudity = 'No Rate'
                violence = 'No Rate'
                profanity = 'No Rate'
                alcohol = 'No Rate'
                frightening = 'No Rate'

        print ('Got', x)
        x = x+1

        writer.writerow({'Name':name, 'Date':date ,'Rate':rate, 'Votes':votes, 'Genre':genre, 'Duration':duration, 'Type':typee, 'Certificate':certificate, 'Episodes':episdoes,
         'Nudity':nudity, 'Violence':violence, 'Profanity':profanity, 'Alcohol':alcohol, 'Frightening':frightening})
