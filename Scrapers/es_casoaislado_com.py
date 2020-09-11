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
    print('Found casoaislado.com...')

    # article
    for t in soup.find_all('article', class_='post'):
        print('Getting wordpress article...')

        dt = {}
        dm = {}

        dm["id"] = str(hash)
        dm["type"] = 'article'
        dm["source"] = curr_url
        for c in t.find_all('div', class_='td-module-meta-info'):
            dm["meta"] = utils.clean_soup(c)
        for c in t.find_all('h1', class_='entry-title'):
            dm["title"] =  utils.clean_soup(c)

        dt["meta"] = dm
        for c in t.find_all('div', class_='td-post-content'):
            dt["text"] = utils.clean_soup(c)

        result = json.dumps(dt, ensure_ascii=False)
        results.append(result)
        print(result)

    # comments
    if len(soup.find_all('div', id='disqus_thread')) > 0:
        print('Getting disqus comments...')

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        try:
            driver.get(curr_url)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);setTimeout(function(){},2000);")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
            for i in driver.find_elements_by_tag_name('iframe'):
                if i.get_attribute('src').find('disqus.com') >= 0:
                    driver.get(i.get_attribute('src'))
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
                    content = driver.page_source
                    break
        except:
            #
            print('webdriver timeout... ')
        driver.close()

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