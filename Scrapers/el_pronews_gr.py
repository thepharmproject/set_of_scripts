from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils
import time, json

def scrape(curr_url, soup, results):
    print('Found pronews.gr...')

    # article
    for t in soup.find_all('body', class_='page-node'):
        if len(soup.find_all('article', class_='js-infinite')) > 0:
            print('Getting drupal article...')

            result = '{'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'

            result = result + '\"meta\":\"'
            for c in t.find_all('div', class_='article__top-info'):
                for d in c.select('div > time'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('article__category > a'):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\",'

            result = result + '\"title\":\"'
            for c in t.select('h1.article__title'):
                result = result + utils.clean_soup(c)
            result = result + '\",'

            result = result + '\"body\":\"'
            for c in t.find_all('div', class_='body'):
                # for d in c.find_all(class_=None, recursive=False):
                result = result + utils.clean_soup(c) + ' '
            result = result + '\"'
            result = result + '}'

            results.append(result)
            print(result)

    # comments
    options = FirefoxOptions()
    # options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)

    ds_url = ''
    # try:
    driver.get(curr_url)
    driver.execute_script("document.getElementsByClassName('article__comments')[0].scrollIntoView();")
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus-thread-885983')))
    cont = BeautifulSoup(driver.page_source, "html.parser")
    for i in cont.find_all('iframe'):
        if i.has_attr('src'): # and i['src'].find('disqus.com/embed') >= 0:
            ds_url = i['src']
            print(ds_url)
            break
    print(ds_url)
    if driver.page_source.find('disqus.com/embed/comm') > 0:
        print('found')
    # except:
        #
        # print('site webdriver timeout...')

    try:
        driver.get(ds_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
    except:
        #
        print('disqus webdriver timeout...')

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