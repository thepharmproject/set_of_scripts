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
    print('Found katohika.gr...')

    # article
    for t in soup.find_all('div', id='content'):
        if len(soup.find_all('div', class_='entry-content')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            for c in t.find_all('div', class_='entry-author'):
                result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
            for c in t.find_all('h1', class_='entry-title'):
                result = result + '\"title\":\"' + utils.clean_soup(c) + '\"'
            result = result + '},'

            result = result + '\"text\":\"'
            for c in t.find_all('div', class_='entry-content'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)

    # comments
    for t in soup.find_all('div', id='comments-section'):
        print('Getting wordpress comments...')
        for c in t.find_all('div', class_='comment-content'):

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"comment\",'
            result = result + '\"source\":\"' + curr_url + '\"'
            result = result + '},'

            result = result + '\"text\":\"'
            for d in c.find_all('p', class_=''):
                result = result + utils.clean_soup(d)
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)