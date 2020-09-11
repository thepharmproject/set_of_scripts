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
    print('Found elespaniol.com...')

    # article
    for t in soup.find_all('div', id='article_body'):
        print('Getting custom article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        for c in t.find_all('span', class_='article-header__time'):
            dm["meta"] = utils.clean_soup(c)
        for c in t.find_all('h1', class_='article-header__heading'):
            dm["title"] =  utils.clean_soup(c)

        dt["meta"] = dm
        for c in t.find_all('div', class_='article-body__content'):
            dt["text"] = utils.clean_soup(c)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)


    for t in soup.find_all('div', id='article_body'):
        print('Getting custom comments...')
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        try:
            driver.get(curr_url)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'like_1')))
            content = driver.page_source
        except:
            print('webdriver timeout... ')
            content = ""
        driver.close()

        for c in  BeautifulSoup(content, "html.parser").find_all('div', class_='comment-text'):
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