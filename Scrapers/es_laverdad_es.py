from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils

def scrape(curr_url, soup, results):
    print('Found laverdad.es...')
    for t in soup.find_all('div', class_='wrapper voc-story'):
        print('Getting custom article...')
        result = '{'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        for c in t.find_all('div', class_='voc-author-info'):
            result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
        for c in t.find_all('h1', class_=''):
            result = result + '\"title\":\"' + utils.clean_soup(c) + '\",'
        result = result + '\"body\":\"'
        for c in t.find_all('p', class_=''):
            result = result + utils.clean_soup(c)
        result = result + '\"'
        result = result + '}'
        results.append(result)
        print(result)
    if len(soup.find_all('div', class_='voc-comments-title')) > 0:
        print('Getting custom comments...')
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        try:
            driver.get(curr_url)
            driver.execute_script("document.getElementById('comments').scrollIntoView();setTimeout(function(){},3000);")
            driver.execute_script("document.getElementsByClassName('voc-comments-title')[0].click();setTimeout(function(){},3000);")
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'voc-comment')))
            content = driver.page_source
        except:
            print('webdriver timeout... ')
            content = ''
        driver.close()
        soup_s = BeautifulSoup(content, "html.parser")
        for t in soup_s.find_all('div', class_='gig-comment-body'):
            result = '{'
            result = result + '\"type\":\"comment\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"body\":\"' + utils.clean_soup(t) + '\"'
            result = result + '}'
            results.append(result)
            print(result)