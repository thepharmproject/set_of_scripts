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
    print('Found infognomonpolitics.gr...')

    # article
    for t in soup.find_all('section', class_='entry'):
        if len(soup.find_all('article', class_='post')) > 0:
            print('Getting wordpress article...')

            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"meta\":\"'
            for c in t.find_all('div', class_='Meta'):
                for d in c.select('span.Date'):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.select('span.Categories > a'):
                    result = result + utils.clean_soup(d) + ' '
            result = result + '\",'
            result = result + '\"title\":\"'
            for c in t.select('div.Article > h2.Title'):
                #
                result = result + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            result = result + '\"text\":\"'
            for c in t.find_all('section', class_='Content'):
                for d in c.find_all(class_=None, recursive=False):
                    result = result + utils.clean_soup(d) + ' '
                for d in c.find_all('div', class_='content', recursive=False):
                    for e in d.find_all(class_=None, recursive=False):
                        result = result + utils.clean_soup(e) + ' '
            result = result + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)

    # comments
    if len(soup.find_all('article', class_='post')) > 0:

        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)

        ds_url = ''
        try:
            driver.get(curr_url)
            driver.execute_script("document.getElementById('disqus_thread').scrollIntoView();")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'disqus_thread')))
            cont = BeautifulSoup(driver.page_source, "html.parser")
            for i in cont.find_all('iframe'):
                if i.has_attr('src') and i['src'].find('disqus.com/embed') >= 0:
                    ds_url = i['src']
                    break
        except:
            #
            print('site webdriver timeout...')

        try:
            driver.get(ds_url)
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'post-message')))
        except:
            #
            print('disqus webdriver timeout...')

        try:
            print('Getting disqus comments...')
            soup = BeautifulSoup(driver.page_source, "html.parser")
            for t in soup.find_all('div', class_='post-message'):

                result = '{\"meta\":{'
                result = result + '\"id\":\"' + str(hash) + '\",'
                result = result + '\"type\":\"comment\",'
                result = result + '\"source\":\"' + curr_url + '\"'
                result = result + '},'

                result = result + '\"text\":\"' + utils.clean_soup(t) + '\"'
                result = result + '}'

                result = utils.clean_whitespaces(result)
                results.append(result)
                print(result)
        except:
            #
            print('disqus webdriver empty...')

        driver.close()