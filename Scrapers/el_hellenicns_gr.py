from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils

def scrape(curr_url, hash, soup, results):
    print('Found hellenicns.gr...')

    # articles
    for t in soup.find_all('body', class_='single-post'):
        if len(soup.find_all('article', class_='post')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"meta\":\"'
            for c in t.find_all('div', class_='below-entry-meta'):
                for d in c.select('time.published'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('span.author > a'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('span.tag-links'):
                    result = result + utils.clean_soup(d) + ' '
                break
            result = result + '\",'
            result = result + '\"title\":\"'
            for c in t.find_all('h1', class_='entry-title'):
                result = result + utils.clean_soup(c)
                break
            result = result + '\",'

            result = result + '\"text\":\"'
            for c in t.find_all('div', class_='entry-content'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            for c in t.find_all('div', class_='single-content'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)