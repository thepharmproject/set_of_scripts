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
    print('Found periodistadigital.com...')

    for t in soup.find_all('div', id='m4p-post-detail'):
        print('Getting wordpress article...')

        result = '{\"meta\":{'
        result = result + '\"id\":\"' + str(hash) + '\",'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        for c in t.find_all('div', class_='m4p-author_time'):
            result = result + '\"meta\":\"' + utils.clean_soup(c)
        result = result + '\",'
        for c in t.find_all('h1', class_='m4p-size-1'):
            result = result + '\"title\":\"' + utils.clean_soup(c)
        result = result + '\"'
        result = result + '},'

        for c in t.find_all('div', class_='m4p-post-content'):
            result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
        result = result + '}'

        result = utils.clean_whitespaces(result)
        results.append(result)
        print(result)