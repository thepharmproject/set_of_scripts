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
    print('Found vimaorthodoxias.gr...')

    for t in soup.find_all('div', class_='post-wrap'):
        if len(soup.find_all('body', class_='single-post')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"meta\":\"'
            for c in t.find_all('div', class_='jeg_meta_container'):
                for d in c.select('div.jeg_meta_author'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('div.jeg_meta_date > a'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('div.jeg_meta_category > span > a'):
                    result = result + utils.clean_soup(d) + ' '
            for c in t.select('div.jeg_post_tags > a'):
                #
                result = result + utils.clean_soup(c) + ' '
            result = result + '\",'
            result = result + '\"title\":\"'
            for c in t.select('div.entry-header > h1.jeg_post_title'):
                #
                result = result + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            result = result + '\"text\":\"'
            for c in t.find_all('div', class_='content-inner'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)