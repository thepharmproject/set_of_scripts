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
    print('Found tradicionviva.es...')

    # article
    for t in soup.find_all('div', class_='zox-article-wrap'):
        print('Getting wordpress article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        dm["meta"] = ''
        for c in t.find_all('div', class_='zox-post-info-wrap'):
            dm["meta"] = dm["meta"] + utils.clean_soup(c)
        dm["title"] = ''
        for c in t.find_all('h1', class_='zox-post-title'):
            dm["title"] = dm["title"] + utils.clean_soup(c)

        dt["meta"] = dm
        dt["text"] = ''
        for c in t.find_all('div', class_='zox-post-body'):
            dt["text"] = dt["text"] + utils.clean_soup(c)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # comments
    if len(soup.find_all('div', class_='fb-comments')) > 0:
        print('Getting facebook comments...')

        options = FirefoxOptions()
        options.set_headless()
        with webdriver.Firefox(log_path='Xtra/geckodriver.log', options=options) as driver:

            driver.implicitly_wait(5)

            content = ''
            try:
                driver.get(curr_url)
                driver.execute_script("document.getElementById('zox-comments-button').scrollIntoView();setTimeout(function(){},2000);")
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'fb-comments')))
                for i in driver.find_elements_by_tag_name('iframe'):
                    if i.get_attribute('src').find('facebook.com') >= 0:
                        driver.get(i.get_attribute('src'))
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_3-8m')))
                        for j in driver.find_elements_by_class_name('_5v47'):
                            j.click()
                        content = driver.page_source
                        break
            except:
                #
                print('webdriver timeout... ')

            driver.close()

        for t in BeautifulSoup(content, "html.parser").find_all('div', class_='_3-8m'):

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