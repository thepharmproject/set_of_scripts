from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils
import json

def scrape(curr_url, hash, soup, results):
    print('Found gazzetta.it...')

    # article
    if len(soup.find_all('section', class_='body-article')) > 0:
        for t in soup.find_all('body', class_=''):
            print('Getting custom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('div', class_='content'):
                for d in c.find_all(class_='is-author'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
                for d in c.find_all(class_='article-date'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            dm["title"] = ''
            for c in t.find_all('h1', id='mainTitle'):
                #
                dm["title"] = dm["title"] + utils.clean_soup(c)

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='content'):
                if not 'not-selectable-js' in c['class']:
                    dt["text"] = dt["text"] + ' ' + utils.clean_soup(c)

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    for t in soup.find_all('div', class_='bck-social-media'):
        print('Getting custom comments...')

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        try:
            driver.get(curr_url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'comments-list')))
            content = driver.page_source
        except:
            #
            print('webdriver timeout... ')
        driver.close()

        try:
            soup_s = BeautifulSoup(content, "html.parser")
            for c in soup_s.find_all('div', class_='comment__content'):

                dt = {}
                dm = {}

                dm["id"] = str(hash)
                dm["type"] = 'comment'
                dm["source"] = curr_url

                dt["meta"] = dm
                dt["text"] = ''
                for d in c.find_all('p', class_='text'):
                    dt["text"] = dt["text"] + utils.clean_soup(d) + ' '

                result = json.dumps(dt, ensure_ascii=False)
                results.append(result)
                print(result)

        except:
            #
            print('webdriver empty...')

