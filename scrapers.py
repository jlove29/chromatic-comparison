import requests
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import csv

class FreeArtScraper:
    def __init__(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
    # Can only read directly from webpage for artists with <= 20 works
    def _readWeb(self, artist):
        url = 'https://www.freeart.com/gallery/d/' + artist + '/' + artist + '.html'
        page = requests.get(url).content
        return page
    # Must download full html and parse for artists with > 20 works
    def _readFile(self, artist):
        page = open('./pages/' + artist + '.txt', 'r').read()
        return page
    # Pull image and metadata for single work by artist
    def _scrapeentry(self, work):
        caption = work.find('p').text.split('.')
        year = caption[0]
        if year == 'c': year = caption[1]
        try: year = int(year)
        except: year = -1
        link = work.find('img')['src']
        imageid = link.split('/')[-1].split('.')[0]
        link = 'https://www.freeart.com' + link
        fname = './images/' + imageid + '.jpg'
        # Save image locally
        image = urllib.request.urlretrieve(link, fname)
        row = [imageid, movement, artist, year]
        return row
    # Run scraper for artist [artist]
    def scrape(self, artist):
        try: page = self._readWeb(artist)
        except: page = self._readFile(artist)
        content = BeautifulSoup(page, 'html.parser')
        # Get artist information
        born = int(content.find('dd', {'data-name': 'birth_year'}).text)
        died = int(content.find('dd', {'data-name': 'death_year'}).text)
        country = content.find('dd', {'data-name': 'country'}).text
        movement = content.find('dd', {'data-name': 'movement'}).text
        # Save data about each work
        data = []
        works = content.find('ul', {'class': 'works'}).findAll('li')
        for work in works: data.append(self._scrapeentry(work))
        # Write data about works to file
        with open('data.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            for row in data:
                writer.writerow(row)
        # Write data about artists to file
        with open('meta.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow([artist, born, died, country, movement])

class WGAScraper:
    def __init__(self):
        data = pd.read_csv('./catalog.csv', engine='python')
        self.data = self._parsecatalogue(data)
        self.id0 = 0
    # Parse information from database catalogue
    def _parsecatalogue(self, data):
        data = data.dropna(subset=['DATE'])
        data = data[data['TECHNIQUE'].apply(lambda x: 'Oil' in x)]
        data['YEAR'] = data.apply(lambda x: guessyear(x), axis=1)
        data = data[['AUTHOR', 'YEAR', 'URL', 'TYPE', 'SCHOOL']]
        data = data[data['YEAR'].apply(lambda x: x >= 1700 and x <= 1820)]
        return data
    # Parse year, or use time range if year unavailable
    def _guessyear(self, row):
        year = row['DATE']
        try: return int(year)
        except:
            if 'c.' in year or 'c,' in year or 'C.' in year or 'c-' in year:
                try: return int(year.split(' ')[-1])
                except: pass
            if len(year) == 7:
                if '-' in year and '/' in year: pass
                elif '-' in year: return int(year.split('-')[0])
                elif '/' in year: return int(year.split('/')[0])
                else: return int(year[:4])
            return int(row['TIMEFRAME'].split('-')[0])
    # Pull image from individual entry in catalogue
    def _scrapeentry(entry):
        print(self.id0)
        url = entry['URL']
        country = entry['SCHOOL']
        genre = entry['TYPE']
        year = entry['YEAR']
        page = requests.get(url)
        content = BeautifulSoup(page.content, 'html.parser')
        links = content.findAll('a')
        for link in links:
            ref = link['href']
            if 'jpg' in ref:
                image = 'https://www.wga.hu' + ref
                fname = './images/' + country + '/' + str(year) + '-' + \
                        genre + '-' + str(id0) + '.jpg'
                urllib.request.urlretrieve(image, fname)
        self.id0 += 1
    # Run the scraper
    def scrape(self):
        self.data.apply(lambda x: self._scrapeentry(x), axis=1)
