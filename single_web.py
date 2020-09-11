''' This python file implements a text parser for any website '''


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


''' METHOD FOR SCRAPING A SINGLE WEBPAGE '''
def scrape(curr_url, hash, soup, results):
    print('Found a website...')

    # load and manipulate the website
    with webdriver.Firefox(options=FirefoxOptions()) as driver:

        # options.add_argument("--headless")
        driver.implicitly_wait(5)

        # load the website
        try:
            driver.get(curr_url)
            for item in range(10):
                driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
                time.sleep(1)
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            content = driver.page_source
        except:
            print('webdriver timeout... ')
            content = ''

        # close the driver
        driver.close()

    # parse the data
    dt = {}
    dm = {}

    dm["id"] = str(hash)
    dm["type"] = 'web_unstructured'
    dm["source"] = curr_url

    dt["meta"] = dm
    dt["text"] = utils.clean_soup(BeautifulSoup(content, "html.parser"))

    result = json.dumps(dt, ensure_ascii=False)
    results.append(result)
    print(result)

