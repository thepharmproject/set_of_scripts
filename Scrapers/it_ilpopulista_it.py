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
    print('Found ilpopulista.it...')

    for t in soup.find_all('body', class_='news'):
        if len(soup.find_all('div', class_='vc_article_body')) > 0:
            print('Getting custom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('p', class_='autore_articolo'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            for c in t.find_all('p', class_='data_articolo'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            dm["title"] = ''
            for c in t.find_all('h1', class_='titolo_articolo'):
                dm["title"]  = dm["title"]  + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='vc_article_body'):
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)