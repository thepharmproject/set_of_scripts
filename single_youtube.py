''' This python file implements a scraper for comments of a single youtube video '''


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


''' METHOD FOR COLLECTING COMMENTS FROM A SINGLE YOUTUBE VIDEO '''
def scrape(curr_url, hash, soup, results):
    print('Found youtube...')

    # load and manipulate the website
    with webdriver.Firefox(options=FirefoxOptions()) as driver:

        # options.add_argument("--headless")
        driver.implicitly_wait(5)

        # load the website
        try:
            driver.get(curr_url)
            time.sleep(5)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "info-text"))).click()
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.DOWN)
            for item in range(10):
                driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
                time.sleep(1)
            for item in range(10):
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(5)
            content = driver.page_source
        except:
            print('webdriver timeout... ')
            content = ''

        # close the driver
        driver.close()

    # parse the comments
    for t in BeautifulSoup(content, "html.parser").find_all('yt-formatted-string', id='content-text'):# class_='post-message'):

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'yt_comment'
        dm["source"] = curr_url

        dt["meta"] = dm
        dt["text"] = utils.clean_soup(t)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    #time.sleep(5)
    #driver.execute_script("document.getElementById('sort-menu').scrollIntoView();")
    #time.sleep(5)
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
    #cont = BeautifulSoup(driver.page_source, "html.parser")
    #for i in cont.find_all('iframe'):
    #    if i.has_attr('src') and i['src'].find('disqus.com/embed') >= 0:
    #        ds_url = i['src']
    #        break
    #driver.execute_script("document.getElementsByClassName('load-more__button')[0].scrollIntoView();")
    #driver.execute_script("document.getElementsByClassName('load-more__button')[0].click();")
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contenteditable-root')))