from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils

def scrape(curr_url, hash, soup, results):
    print('Found disidentia.com...')
    counter = 0

    # article
    for t in soup.find_all('article', class_='type-post'):
        print('Getting wordpress article...')

        counter += 1
        result = '{\"meta\":{'
        result = result + '\"id\":\"' + str(hash) + str(counter) + '\",'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        for c in t.find_all('div', class_='td-module-meta-info'):
            result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
            break
        for c in t.find_all('h1', class_='entry-title'):
            result = result + '\"title\":\"' + utils.clean_soup(c)
            break
        result = result + '\"'
        result = result + '},'

        for c in t.find_all('div', class_='td-post-content tagdiv-type'):
            result = result + '\"text\":\"'
            for d in c.find_all('p', class_=''):
                result = result + utils.clean_soup(d)
            result = result + '\"'
        result = result + '}'

        result = utils.clean_whitespaces(result)
        results.append(result)
        print(result)

    # comments
    if len(soup.find_all('ol', class_='comment-list')) > 0:
        print('Getting custom comments...')
        for t in soup.find_all('div', class_='comment-content'):

            counter += 1
            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + str(counter) + '\",'
            result = result + '\"type\":\"comment\",'
            result = result + '\"source\":\"' + curr_url + '\"'
            result = result + '},'

            result = result + '\"text\":\"' + utils.clean_soup(t) + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)