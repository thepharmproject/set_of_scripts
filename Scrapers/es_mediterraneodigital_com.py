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
    print('Found mediterraneodigital.com...')

    # article
    for t in soup.find_all('div', class_='item-page'):
        print('Getting joomla article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''
        for c in t.find_all('dl', class_='article-info'):
            dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
        dm["title"] = ''
        for c in t.find_all('h1', class_='article-title'):
            dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find_all('section', class_='article-content'):
            for d in c.find_all('p', class_=''):
                dt["text"] = dt["text"] + utils.clean_soup(d) + ' '

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)