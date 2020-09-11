''' This python file implements parsers for single websites '''


''' LIBRARIES IMPORTED '''
import sys, time
import hashlib, requests
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
import single_facebook as sif
import single_twitter as sit
import single_web as siw
import single_youtube as siy


''' METHOD FOR SCANNING AND SCRAPING WEBSITES '''
def download(url):

    # download website
    hash = int(hashlib.sha1(url.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    try:
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(url, headers=headers)
        content = resp.text
        print('Fetched {} with status {}'.format(url, resp.status_code))
    except:
        content = ''
        print('Error at fetching {}'.format(filename))

    # parse data
    results = []
    soup = BeautifulSoup(content, "html.parser")

    # 01 Facebook
    if url.find('facebook.') > 0:
        sif.scrape(url, hash, soup, results)
        name = 'facebook'
    # 02 Twitter
    elif url.find('twitter.') > 0:
        sit.scrape(url, hash, soup, results)
        name = 'twitter'
    # 03 YouTube
    elif url.find('youtube.') > 0:
        siy.scrape(url, hash, soup, results)
        name = 'youtube'
    # 04 Web
    else:
        siw.scrape(url, hash, soup, results)
        name = 'web'

    # write results
    file = open('Data\\' + 'single_'+ name +'_data.json', 'a', encoding='utf-8-sig')
    print('{} items added...'.format(len(results)))
    for result in results:  file.write(result + '\n')
    file.close()