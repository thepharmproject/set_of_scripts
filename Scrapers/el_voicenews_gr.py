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
    print('Found voicenews.gr...')

    # webdriver
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)
    driver.get(curr_url)
    try:
        print('deploying webdriver...')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'brm-more-link')))
        driver.execute_script("document.getElementsByClassName('brm-more-link')[0].scrollIntoView();setTimeout(function(){},2000);")
        driver.execute_script("document.getElementsByClassName('brm-more-link')[0].click();setTimeout(function(){},2000);")
        soup = BeautifulSoup(driver.page_source, "html.parser")
    except:
        #
        print('webdriver timeout... ')
    driver.close()

    # article
    for t in soup.find_all('div', class_='post-inner'):
        if len(soup.find_all('body', class_='single-post')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"meta\":\"'
            for c in t.find_all('p', class_='post-meta'):
                for d in c.select('span.tie-date'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('span.post-cats > a'):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\",'
            result = result + '\"title\":\"'
            for c in t.select('div.post-inner > h1.post-title'):
                #
                result = result + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            result = result + '\"text\":\"'
            for c in t.find_all('div', class_='entry'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            for c in t.find_all('div', class_='brm'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)