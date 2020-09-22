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
    print('Found olympia.gr...')

    # reload with selenium
    with webdriver.Firefox() as driver:

        try:
            driver.implicitly_wait(5)
            driver.maximize_window()
            driver.get(curr_url)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
            content = driver.page_source
            # for i in cont.find_all('iframe'):
            #     if i.has_attr('src') and i['src'].find('disqus.com/embed') >= 0:
            #         ds_url = i['src']
            #         print('found discus thread with url:', ds_url)
            #         break
        except:
            content = ''
            print('webdriver timeout... ')

        driver.close()

    # article
    for t in BeautifulSoup(content, "html.parser").find_all('article', class_='post'):
        if len(soup.find_all('body', class_='single-post')) > 0:
            print('Getting wordpress article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.select('div.tdb-block-inner > time.entry-date'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            for c in t.select('ul.tdb-tags > li > a'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ' '
            dm["title"] = ''
            for c in t.select('h1.tdb-title-text'):
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.select('div.wpb_wrapper > div.tdb_single_content > div.tdb-block-inner'):
                for d in c.find_all('p', class_=None):
                    dt["text"] = dt["text"] + utils.clean_soup(d) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)