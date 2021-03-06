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
    print('Found termometropolitico.it...')
    for t in soup.find_all('body', class_='single-post'):
        # if t.has_attr('id') and t['id'].find('post') >= 0:
        print('Getting wordpress article...')

        dt = {}
        dm = {}
        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        for c in t.find_all('div', class_='single_info'):
            dm["meta"] = utils.clean_soup(c)
        for c in t.find_all('h1', class_='single_title'):
            dm["title"] = utils.clean_soup(c)

        dt["meta"] = dm
        for c in t.find_all('div', class_='single_content'):
            dt["text"] = utils.clean_soup(c)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)