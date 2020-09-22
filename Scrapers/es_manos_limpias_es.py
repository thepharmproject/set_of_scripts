from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils
import time, json

def scrape(curr_url, hash, soup, results):
    print('Found manos-limpias.es...')
    for t in soup.find_all('div', class_='col-md-9'):
        print('Getting asp article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''

        dm["title"] = ''
        for c in t.find_all('h3', class_=''):
            dm["title"] = dm["title"] + utils.clean_soup(c)
            break

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find_all('div', class_='content-box'):
            dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)