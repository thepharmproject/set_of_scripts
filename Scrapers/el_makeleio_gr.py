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
    print('Found makeleio.gr...')

    # article
    for t in soup.find_all('div', class_='single-style1-wrap'):
        print('Getting wordpress article...')

        result = '{\"meta\":{'
        result = result + '\"id\":\"' + str(hash) + '\",'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        for c in t.find_all('div', class_='single-style1-meta-tag'):
            result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
        for c in t.find_all('div', class_='single-style1-title'):
            result = result + '\"title\":\"' + utils.clean_soup(c) + '\"'
        result = result + '},'

        for c in t.find_all('div', class_='single-style1-content'):
            result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
        result = result + '}'

        result = utils.clean_whitespaces(result)
        results.append(result)
        print(result)

    # comments
    for t in soup.find_all('div', class_='comments-area'):
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