''' This python file implements a scraper for posts of a single facebook group '''


''' LIBRARIES IMPORTED '''
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils
import time, json


''' METHOD FOR COLLECTING POSTS FROM A SINGLE FACEBOOK GROUP '''
def scrape(curr_url, hash, soup, results):
    print('Found facebook...')

    # load and manipulate the website
    with webdriver.Firefox(options=FirefoxOptions()) as driver:

        driver.maximize_window()
        driver.implicitly_wait(5)

        # load the website
        try:
            driver.get(curr_url)
            time.sleep(5)
            for item in range(10):
                # driver.find_element_by_tag_name('img').send_keys(Keys.END)
                # driver.find_elements_by_id('seo_h1_tag')[0].send_keys(Keys.END)
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                time.sleep(5)
            content = driver.page_source
        except:
            print('webdriver timeout... ')
            content = ''

        # close the driver
        driver.close()

    # parse posts (old facebook)
    for t in BeautifulSoup(content, "html.parser").find_all('div', class_='_5pbx userContent _3576'):

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'fb_post'
        dm["source"] = curr_url

        dt["meta"] = dm
        dt["text"] = utils.clean_soup(t)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # parse posts (new facebook)
    for t in BeautifulSoup(content, "html.parser").find_all('div', class_='ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a'):

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'fb_post'
        dm["source"] = curr_url

        dt["meta"] = dm
        dt["text"] = utils.clean_soup(t)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # parse comments (old facebook)
    for t in BeautifulSoup(content, "html.parser").find_all('span', class_='_3l3x'):

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'fb_comment'
        dm["source"] = curr_url

        dt["meta"] = dm
        dt["text"] = utils.clean_soup(t)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # parse comments (new facebook)
    for t in BeautifulSoup(content, "html.parser").find_all('div', class_='ecm0bbzt e5nlhep0 a8c37x1j'):

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'fb_comment'
        dm["source"] = curr_url

        dt["meta"] = dm
        dt["text"] = utils.clean_soup(t)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)
