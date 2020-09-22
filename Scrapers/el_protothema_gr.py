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
    print('Found protothema.gr...')

    # article
    for t in soup.find_all('main', class_='inner'):
        if len(soup.find_all('div', class_='cntTxt')) > 0:
            print('Getting atcom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('div', class_='infoBar'):
                for d in c.select('div.tags > div.cnt > a'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
                for d in c.select('div.tags > div.cnt > a'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
            for c in t.select('div.articleInfo'):
                dm["meta"] = dm["meta"] + utils.clean_soup(c) + ''
            dm["title"] = ''
            for c in t.select('div.title > h1'):
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='cntTxt'):
                # for d in c.find_all(class_=None, recursive=False):
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    if len(soup.find_all('div', class_='cntTxt')) > 0:
        print('Getting atcom comments...')

        # reload main website
        with webdriver.Firefox(log_path='Xtra/geckodriver.log', options=FirefoxOptions()) as driver:

            content = ''
            try:
                driver.implicitly_wait(5)
                driver.maximize_window()
                driver.get(curr_url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'comCnt')))
                for i in range(10):
                    print('load more')
                    content = driver.page_source
                    driver.execute_script("document.getElementsByClassName('btn full')[0].scrollIntoView();")
                    driver.execute_script("document.getElementsByClassName('btn full')[0].click();")
                    time.sleep(2)
            except:
                #
                print('atcom webdriver timeout...')

        # parse comments
        for t in BeautifulSoup(content, "html.parser").find_all('div', class_='comSection'):
            for c in t.find_all('div', class_='txt'):

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