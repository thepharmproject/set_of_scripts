from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils

def scrape(curr_url, soup, results):
    print('Found manos-limpias.es...')
    for t in soup.find_all('div', class_='col-md-9'):
        print('Getting asp article...')
        result = '{'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        c = t.find_all('h3', class_='')[0]
        result = result + '\"title\":\"' + utils.clean_soup(c) + '\",'
        for c in t.find_all('div', class_='content-box'):
            result = result + '\"body\":\"' + utils.clean_soup(c) + '\"'
        result = result + '}'
        results.append(result)
        print(result)