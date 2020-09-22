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
    print('Found pronews.gr...')

    # article
    for t in soup.find_all('body', class_='page-node'):
        if len(soup.find_all('article', class_='js-infinite')) > 0:
            print('Getting drupal article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            for c in t.find_all('div', class_='article__top-info'):
                for d in c.select('div > time'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
                for d in c.select('article__category > a'):
                    dm["meta"] = dm["meta"] + utils.clean_soup(d) + ' '
            dm["title"] = ''
            for c in t.select('h1.article__title'):
                dm["title"] = dm["title"] + utils.clean_soup(c) + ' '

            dt["meta"] = dm
            dt["text"] = ''
            for c in t.find_all('div', class_='body'):
                # for d in c.find_all(class_=None, recursive=False):
                dt["text"] = dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

    # comments
    quit_v = False
    if quit_v == True:
        with webdriver.Firefox() as driver:
            driver.implicitly_wait(5)
            driver.maximize_window()

            ds_url = ''
            # try:
            driver.get(curr_url)
            time.sleep(2)
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'article__comments-intro')))
            # WebDriverWait(driver, 5).until(EC.visibility_of_element_located(By.CLASS_NAME, 'article__comments-intro'))
            time.sleep(5)

            for i in driver.find_elements_by_tag_name('iframe'):
                if i.get_attribute('src').find('disqus') >= 0:
                    print(i.get_attribute('src'))

            # except:
                #
                # print('site webdriver timeout...')

            # open disqus
            try:
                driver.get(ds_url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
            except:
                #
                print('disqus webdriver timeout...')

            # collect disqus
            try:
                soup = BeautifulSoup(driver.page_source, "html.parser")
                for t in soup.find_all('div', class_='post-message'):
                    result = '{'
                    result = result + '\"type\":\"comment\",'
                    result = result + '\"source\":\"' + curr_url + '\",'
                    result = result + '\"body\":\"' + utils.clean_soup(t) + '\"'
                    result = result + '}'
                    results.append(result)
                    print(result)
            except:
                #
                print('disqus webdriver empty')

            driver.close()