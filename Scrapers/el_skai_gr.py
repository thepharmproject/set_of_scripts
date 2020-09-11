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
    print('Found skai.gr...')

    # article
    for t in soup.find_all('article', class_='article'):
        if len(soup.find_all('div', class_='articleBody')) > 0:
            print('Getting drupal article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('div', class_='infoBar'):
                for d in c.select('div.dates > span'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
                    break
                for d in c.select('div.article-category > a'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
            dm["title"] = ''
            for c in t.select('div.mainInfo > h1'):
                #
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', id='articleHidder'):
                for d in c.find_all(class_=None, recursive=False):
                    dt["text"] =  dt["text"] + utils.clean_soup(d) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    if len(soup.find_all('div', class_='articleBody')) > 0:
        print('Getting disqus comments...')

        # reload main website
        with webdriver.Firefox(log_path='Xtra/geckodriver.log', options=FirefoxOptions()) as driver:

            ds_url = ''

            try:
                driver.implicitly_wait(5)
                driver.get(curr_url)
                driver.execute_script("document.getElementById('disqus_thread').scrollIntoView();")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
                cont = BeautifulSoup(driver.page_source, "html.parser")
                for i in cont.find_all('iframe'):
                    if i.has_attr('src') and i['src'].find('disqus.com/embed') >= 0:
                        ds_url = i['src']
                        print('found discus thread with url:', ds_url)
                        break
            except:
                #
                print('webdriver 1 timeout... ')

            driver.close()

        # load disqus iframe
        with webdriver.Firefox(log_path='Xtra/geckodriver.log', options=FirefoxOptions()) as driver:

            content = ''

            try:
                driver.implicitly_wait(5)
                driver.get(ds_url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
                for i in range(10):
                    print('load more')
                    driver.execute_script("document.getElementsByClassName('load-more__button')[0].scrollIntoView();")
                    driver.execute_script("document.getElementsByClassName('load-more__button')[0].click();")
                    time.sleep(2)
                content = driver.page_source
            except:
                print('webdriver 2 timeout... ')
                content = ''

            driver.close()

        # parse comments
        for t in BeautifulSoup(content, "html.parser").find_all('div', class_='post-message'):

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

