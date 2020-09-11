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
    print('Found rainews.it...')

    # article
    for t in soup.find_all('div', class_='boxArticle'):
        if len(t.find_all('article', class_='')) > 0:
            print('Getting custom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('div', class_='text'):
                for d in c.find_all('time', class_='articleDate'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
            dm["title"] = ''
            for c in t.find_all('div', class_='title'):
                for d in c.find_all('h1', class_=''):
                    dm["title"] = dm["title"] + utils.clean_soup(d) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='text'):
                #
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)