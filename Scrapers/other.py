from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import utilities as utils

# Search with Google
def search(query):
    query = query.replace(' ', '+')
    URL = f"https://google.com/search?q={query}"
    download(URL)

def scrape(curr_url, soup, results):

    # Atcom comments
    if text.find('atcom') > 0:
        print('This is an atcom site...')
        for t in soup.find_all('div', class_='comCnt'):
            for c in t.findChildren('div', class_='txt'):
                result = c.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                results.append(result)
                # print(result)

    # Blogger
    if text.find('blogger') > 0:
        print('This is a blogger site...')
        for t in soup.find_all('div', class_='comments'):
            for c in t.find_all('p', class_='comment-content'):
                result = c.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                results.append(result)
                print(result)

    # Drupal comments
    if text.find('Drupal') > 0:
        print('This is a drupal site...')
        for t in soup.find_all('div', class_='comment-content'):
            result = t.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            results.append(result)

    # Joomla comments
    if text.find('Joomla') > 0:
        print('This is a joomla site...')
        for t in soup.find_all('div', class_='comment-content'):
            result = t.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            results.append(result)

    # Wordpress comments
    if text.find('WordPress') > 0:
        # print('This is a wordpress site...')
        for t in soup.find_all(class_='comment-list'):
            for c in t.find_all('div', class_='comment-content'):
                result = c.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                results.append(result)
                print(result)
        for t in soup.find_all(class_='comments-area'):
            for c in t.find_all('div', class_='wc-comment-text'):
                result = c.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                results.append(result)
                print(result)
        for t in soup.find_all(class_='commentlist'):
            for u in t.find_all('li', class_='comment'):
                for c in u.find_all('p'):
                    result = c.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
                    results.append(result)
                    print(result)

    # Disqus comments
    if text.find('disqus') > 0:
        print('This site implements disqus comments...')

        # Reload page dynamically
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        driver.get(curr_url)

        # trigger javascript render
        if len(driver.find_elements_by_class_name('show-comments')) > 0:
            print('show-comments')
            driver.find_elements_by_class_name('show-comments')[0].click()

        # open thread
        if len(driver.find_elements_by_id('disqus_thread')) > 0:
            print('Disqus thread found...')
            e = driver.find_element_by_id('disqus_thread')
            if len(e.find_elements_by_tag_name('iframe')) > 0:
                disqus_iframe = e.find_element_by_tag_name('iframe')
                iframe_url = disqus_iframe.get_attribute('src')
                print('Going to', iframe_url)
                try:
                    driver.get(iframe_url)
                    wait = WebDriverWait(driver, 5)
                    commentCountPresent = EC.presence_of_element_located((By.CLASS_NAME, 'post-message'))
                    wait.until(commentCountPresent)
                    content = driver.page_source
                except:
                    #
                    print('No comments')

        driver.close()

        soup_s = BeautifulSoup(content, "html.parser")
        for t in soup_s.find_all('div', class_='post-message'):
            # for c in t.findChildren('p'):
            result = t.text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
            results.append(result)
            print(result)

    # Facebook comments
    if text.find('facebook-comment-box') > 0:
        print('*** This site implements facebook comments ***')

        # reload page dynamically
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        try:
            driver.get(curr_url)
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            for i in  driver.find_elements_by_tag_name('iframe'):
                if i.get_attribute('src').find('facebook.com') > 0:
                    # print(i.get_attribute('src'))
                    driver.get(i.get_attribute('src'))
                    wait = WebDriverWait(driver, 5)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_3-8m')))
                    content = driver.page_source
                    break
        except:
            #
            print('Webdriver crashed... ')
        driver.close()

        # get comments
        soup_s = BeautifulSoup(content, "html.parser")
        for t in soup_s.find_all('div', class_='_3-8m'):
            result = '{'
            result = result + '\"type\":\"comment\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            result = result + '\"body\":\"' + utils.clean_soup(t) + '\"'
            result = result + '}'
            results.append(result)
            print(result)

    # Google results
    if text.find('Super Google') > 0:
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                }
                print(title, " - ", link)
                results.append(item)
        # print(results)