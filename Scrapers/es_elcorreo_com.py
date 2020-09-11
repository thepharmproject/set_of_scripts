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
    print('Found elcorreo.com/diariosur.es...')

    # article
    for t in soup.find_all('div', class_='wrapper voc-story'):
        print('Getting custom article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''
        for c in t.find_all('div', class_='voc-author-info'):
            dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
        dm["title"] = ''
        for c in t.find_all('h1', class_=''):
            dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find_all('p', class_=''):
            dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # comments
    if len(soup.find_all('div', class_='voc-comments-title')) > 0:
        print('Getting custom comments...')

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)

        try:
            driver.get(curr_url)
            driver.execute_script("document.getElementById('comments').scrollIntoView();setTimeout(function(){},3000);")
            driver.execute_script("document.getElementsByClassName('voc-comments-title')[0].click();setTimeout(function(){},3000);")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'voc-comment')))
            content = driver.page_source
        except:
            content =''
            print('webdriver timeout... ')

        driver.close()

        for t in BeautifulSoup(content, "html.parser").find_all('div', class_='gig-comment-body'):

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'comment'
            dm["source"] = curr_url

            dt["meta"] = dm
            dt["text"] = utils.clean_soup(t)

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)