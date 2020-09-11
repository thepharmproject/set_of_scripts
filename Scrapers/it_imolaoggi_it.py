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
    print('Found imolaoggi.it...')

    # article
    for t in soup.find_all('article', class_='post'):
        if len(t.find_all('h1', class_='entry-title')) > 0:
            print('Getting wordpress article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('span', class_='post-author'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            for c in t.find_all('span', class_='posted-on'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            for c in t.find_all('span', class_='cat-links'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            dm["title"] = ''
            for c in t.find_all('h1', class_='entry-title'):
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all(class_=''):
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    for t in soup.find_all('ol', class_='commentlist'):
        print('Getting wordpress comments...')
        for c in t.find_all('li', class_='comment'):

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'comment'
            dm["source"] = curr_url

            dt["meta"] = dm
            dt["text"] = ''
            for d in c.find_all('p', class_=''):
                dt["text"] = dt["text"] + utils.clean_soup(d) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)