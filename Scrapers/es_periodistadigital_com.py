import utilities as utils

def scrape(curr_url, hash, soup, results):
    print('Found periodistadigital.com...')
    counter = 0
    for t in soup.find_all('div', id='m4p-post-detail'):
        counter += 1
        result = '{\"meta\":{'
        result = result + '\"id\":\"' + str(hash) + str(counter) + '\",'
        result = result + '\"type\":\"article\",'
        result = result + '\"source\":\"' + curr_url + '\",'
        for c in t.find_all('div', class_='m4p-author_time'):
            result = result + '\"meta\":\"' + utils.clean_soup(c)
        result = result + '\",'
        for c in t.find_all('h1', class_='m4p-size-1'):
            result = result + '\"title\":\"' + utils.clean_soup(c)
        result = result + '\"'
        result = result + '},'

        for c in t.find_all('div', class_='m4p-post-content'):
            result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
        result = result + '}'

        print(result)
        results.append(result)