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
    print('Found huelvainformacion.es...')

    # article
    for t in soup.find_all('article', class_='pg-content'):
        if len(t.find_all('div', class_='mce-body')) > 0:
            print('Getting custom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('time', class_='dateline'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            dm["title"] = ''
            for c in t.find_all('h1', class_='pg-bkn-headline'):
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='mce-body'):
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    for t in soup.find_all('section', id='comments'):
        print('Getting custom comments...')

        # reload with selenium
        with webdriver.Firefox() as driver:

            content = ''
            try:
                driver.implicitly_wait(5)
                driver.get(curr_url)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment-message')))
                content = driver.page_source
            except:
                content = ''
                print('webdriver timeout... ')
            driver.close()

        # parse data
        for c in BeautifulSoup(content, "html.parser").find_all('div', class_='comment-message'):
            if len(utils.clean_soup(c)) > 0:

                dt = {}
                dm = {}

                dm["id"] = str(hash)
                dm["type"] = 'comment'
                dm["source"] = curr_url

                dt["meta"] = dm
                dt["text"] = utils.clean_soup(c)

                result = json.dumps(dt, ensure_ascii=False)
                results.append(result)
                print(result)