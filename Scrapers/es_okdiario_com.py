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
    print('Found okdiario.com...')

    for t in soup.find_all('article', class_='post'):
        if len(t.find_all('div', class_='entry-content')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"meta\":\"'
            for c in t.find_all('address', class_='autor'):
                result = result + utils.clean_soup(c)
            result = result + '\",'
            result = result + '\"title\":\"'
            for c in t.find_all('h1', class_='entry-title'):
                result = result + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            for c in t.find_all('div', class_='entry-content'):
                result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)