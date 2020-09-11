import utilities as utils

def scrape(curr_url, hash, soup, results):
    print('Found okdiario.com...')
    counter = 0
    for t in soup.find_all('div', id='homepost'):
        if len(t.find_all('div', class_='post')) > 0:
            counter += 1
            result = '{\"meta\":{'
            result = result + '\"id\":\"' + str(hash) + str(counter) + '\",'
            result = result + '\"type\":\"article\",'
            result = result + '\"source\":\"' + curr_url + '\",'
            for c in t.find_all('div', id='datemeta'):
                result = result + '\"meta\":\"' + utils.clean_soup(c) + '\",'
            for c in t.find_all('h2', class_=''):
                result = result + '\"title\":\"' + utils.clean_soup(c)
            result = result + '\"'
            result = result + '},'

            for c in t.find_all('div', class_='entry'):
                result = result + '\"text\":\"' + utils.clean_soup(c) + '\"'
            result = result + '}'

            result = utils.clean_whitespaces(result)
            results.append(result)
            print(result)