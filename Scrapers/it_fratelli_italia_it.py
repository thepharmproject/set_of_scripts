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
    print('Found fratelli-italia.it...')

    for t in soup.find_all('body', class_='single-post'):
        print('Getting wordpress article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''
        for c in t.find_all('ul', class_='post-options'):
            for d in c.find_all('time'):
                dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
        for c in t.find_all('div', class_='post-tags'):
            for d in c.find_all('a'):
                dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
        dm["title"] = ''
        for c in t.find('div', id='wrappermain-cs').find('div', class_='breadcrumb').find_all('h1', class_='cs-page-title'):
            dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find('article', class_='type-post').find('div', class_='detail_text').find_all('p'):
            dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)