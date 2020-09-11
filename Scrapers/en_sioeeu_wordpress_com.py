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
    print('Found sioeeu.wordpress.com...')

    # article
    for t in soup.select('article.type-post.format-standard'):
        if len(t.select('div.single-entry-content > p')) > 0:
            print('Getting wordpress article...')

            dt = {}
            dm = {}
            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            for c in t.select('header.single-entry-header > p'):
                dm["meta"] = utils.clean_soup(c)
            for c in t.find_all('h1', class_='entry-title'):
                dm["title"] = utils.clean_soup(c)
            dt["meta"] = dm

            dt["text"] = ''
            for c in t.select('div.single-entry-content > p'):
                dt["text"] = dt["text"] + ' ' + utils.clean_soup(c)

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    for t in soup.find_all('div', id='comments'):
        print('Getting wordpress comments...')
        for c in t.select('div.comment-body > p'):

            dt = {}
            dm = {}
            dm["id"] = str(hash)
            dm["type"] = 'comment'
            dm["source"] = curr_url
            dt["meta"] = dm
            dt["text"] = utils.clean_soup(c)

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)