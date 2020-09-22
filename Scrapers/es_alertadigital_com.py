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
    print('Found alertadigital.com...')

    for t in soup.find_all('div', id='homepost'):
        if len(t.find_all('div', class_='post')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            for c in t.find_all('div', id='datemeta'):
                result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
            for c in t.find_all('h2', class_=''):
                result = result + '\"title\":\"' + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            for c in t.find_all('div', class_='entry'):
                result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)