from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils
import json

def scrape(curr_url, hash, soup, results):
    print('Found la7.it...')

    for t in soup.find_all('body', class_='node-type-la7-video'):
        print('Getting drupal article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''
        for c in t.find_all('div', class_='infoVideoRow'):
            for d in c.find_all('div', class_='dateVideo'):
                dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
        dm["title"] = ''
        for c in t.find_all('div', class_='infoVideoRow'):
            for d in c.find_all('h1'):
                dm["title"] = dm["title"] + utils.clean_soup(d) + ' '

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find_all('div', class_='occhiello'):
            for d in c.find_all('p'):
                dt["text"] = dt["text"] + utils.clean_soup(d) + ' '

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)