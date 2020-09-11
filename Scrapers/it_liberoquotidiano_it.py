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
    print('Found liberoquotidiano.it...')

    options = FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(5)

    # articles
    try:
        driver.maximize_window()
        driver.get(curr_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'article-data')))
        driver.execute_script("document.getElementById('disqus_thread').scrollIntoView();setTimeout(function(){},2000);")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
        driver.execute_script("document.getElementsByClassName('fb-comments')[0].scrollIntoView();setTimeout(function(){},2000);")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fb-comments')))
        content = driver.page_source
    except:
        #
        print('webdriver timeout... ')

    try:
        soup = BeautifulSoup(content, "html.parser")
        for t in soup.find_all('body', class_='article'):
            print('Getting custom article...')

            dt = {}
            dm = {}

            dm["id"] = str(hash)
            dm["type"] = 'article'
            dm["source"] = curr_url
            dm["meta"] = ''
            c = t.find('main').find('div', class_='main-wrapper').find('section').find('div', class_='article-data').find('time')
            dm["meta"] = dm["meta"] + utils.clean_soup(c)
            dm["title"] = ''
            c = t.find('main').find('h1')
            dm["title"] = dm["title"] + utils.clean_soup(c)

            dt["meta"] = dm
            dt["text"] = ''
            # c = t.find('main').find('div', class_='main-wrapper').find('section').find('div', class_='article-data').find_next('p')
            for c in t.find('main').find('div', class_='main-wrapper').find('section').find_all('p', _class=''):
                dt["text"] =  dt["text"] + utils.clean_soup(c) + ' '

            result = json.dumps(dt, ensure_ascii=False)
            results.append(result)
            print(result)

            ds_url = ''
            for i in soup.find_all('iframe'):
                if i.has_attr('src') and i['src'].find('disqus.com/embed') >= 0:
                    ds_url = i['src']
                    print('disqus:', ds_url)
                    break
            fb_url = ''
            for i in soup.find_all('iframe'):
                if i.has_attr('src') and i['src'].find('facebook.com') >= 0:
                    fb_url = i['src']
                    print('facebook:', fb_url)
                    break
    except:
        #
        print('webdriver empty...')

    # disqus
    try:
        driver.get(ds_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
    except:
        #
        print('disqus webdriver error')

    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for t in soup.find_all('div', class_='post-message'):
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
    except:
        #
        print('disqus webdriver empty')

    # facebook
    try:
        driver.get(fb_url)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, '_3-8m')))
        for j in driver.find_elements_by_class_name('_5v47'):
            j.click()
        for j in driver.find_elements_by_class_name('_50f7'):
            j.click()
    except:
        #
        print('facebook webdriver error')

    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for t in soup.find_all('div', class_='_3-8m'):
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
    except:
        #
        print('facebook webdriver empty...')

    driver.close()