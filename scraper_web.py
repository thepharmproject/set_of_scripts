''' This python file implements a web spider for the supported websites '''


''' PYTHON SETUP '''
# a list of the required packages is listed here based on anaconda setup commands.

# conda install selenium
# conda install beautifulsoup4
# conda install -c conda-forge geckodriver


''' LIBRARIES IMPORTED '''
import sys, time
import random
import hashlib, requests
from urllib.parse import urlsplit, urlunsplit
from bs4 import BeautifulSoup
from Scrapers import *
import utilities as utils


''' METHOD FOR SCANNING AND SCRAPING WEBSITES '''
def download(base_url, curr_url, cycles):

    # split_url = urlsplit(URL)
    hash = int(hashlib.sha1(curr_url.encode('utf-8')).hexdigest(), 16) % (10 ** 8)
    filename = '{:}_{:}'.format(base_url, hash)

    # Fetch the website
    try:
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(curr_url, headers=headers)
        content = resp.text
        # if resp.status_code == 200:
        #     print('Saving html file...')
        #     file = open('Data\\' + filename + '.txt', "w", encoding='utf-8')
        #     file.write(content)
        #     file.close()
        # file = open('Data\\'+filename+'.txt', 'r', encoding='utf-8')
        # text = file.read()
        # file.close()
        print('Fetched {} with status {}'.format(filename, resp.status_code))
    except:
        content = ''
        print('Error at fetching {}'.format(filename))


    ''' PARSE AND ROUTE DATA '''
    # Init results and parser
    results = []
    soup = BeautifulSoup(content, "html.parser")

    # 01 EN - sioeeu.wordpress.com - WordPress
    if curr_url.find('sioeeu.wordpress.com') > 0:           en_sioeeu_wordpress_com.scrape(curr_url, hash, soup, results)
    
    # 01 ES - okdiario.com - WordPress
    if curr_url.find('okdiario.com') > 0:                   es_okdiario_com.scrape(curr_url, hash, soup, results)
    # 02 ES - alertadigital.com -  WordPress
    if curr_url.find('alertadigital.com') > 0:              es_alertadigital_com.scrape(curr_url, hash, soup, results)
    # 03 ES - periodistadigital.com -  WordPress
    if curr_url.find('periodistadigital.com') > 0:          es_periodistadigital_com.scrape(curr_url, hash, soup, results)
    # 04 ES - elespanol.com - Custom / Custom
    if curr_url.find('elespanol.com') > 0:                  es_elespanol_com.scrape(curr_url, hash, soup, results)
    # 05 ES - diarioya.es - Drupal
    if curr_url.find('diarioya.es') > 0:                    es_diarioya_es.scrape(curr_url, hash, soup, results)
    # 06 ES - gaceta.es - Wordpress
    if curr_url.find('gaceta.es') > 0:                      es_gaceta_es.scrape(curr_url, hash, soup, results)
    # 07 ES - voxespana.es - WordPress
    if curr_url.find('voxespana.es') > 0:                   es_voxespana_es.scrape(curr_url, hash, soup, results)
    # 08 ES - actuall.com - Wordpress / Facebook
    if curr_url.find('actuall.com') > 0:                    es_actuall_com.scrape(curr_url, hash, soup, results)
    # 09 ES - casoaislado.com - Wordpress / DISQUS
    if curr_url.find('casoaislado.com') > 0:                es_casoaislado_com.scrape(curr_url, hash, soup, results)
    # 10 ES - outono.net - Wordpress / Facebook + Custom
    if curr_url.find('outono.net') > 0:                     es_outono_net.scrape(curr_url, hash, soup, results)
    # 11 ES - lasvocesdelpueblo.com - Wordpress
    if curr_url.find('lasvocesdelpueblo.com') > 0:          es_lasvocesdelpueblo_com.scrape(curr_url, hash, soup, results)
    # 12 ES - disidentia.com - Wordpress / Custom
    if curr_url.find('disidentia.com') > 0:                 es_disidentia_com.scrape(curr_url, hash, soup, results)
    # 13 ES - elcorreodeespana.com - Wordpress / DISQUS
    if curr_url.find('elcorreodeespana.com') > 0:           es_elcorreodeespana_com.scrape(curr_url, hash, soup, results)
    # 14 ES - mediterraneodigital.com - Joomla
    if curr_url.find('mediterraneodigital.com') > 0:        es_mediterraneodigital_com.scrape(curr_url, hash, soup, results)
    # 15 ES - elcorreo.com - Custom / Custom
    if curr_url.find('elcorreo.com') > 0:                   es_elcorreo_com.scrape(curr_url, hash, soup, results)
    # 16 ES - diariosur.es - Custom / Custom
    if curr_url.find('diariosur.es') > 0:                   es_elcorreo_com.scrape(curr_url, hash, soup, results)
    # 17 ES - huelvainformacion.es - Custom / Custom
    if curr_url.find('huelvainformacion.es') > 0:           es_huelvainformacion_es.scrape(curr_url, hash, soup, results)
    # 18 ES - hoy.es - Custom / Custom
    if curr_url.find('hoy.es') > 0:                         es_hoy_es.scrape(curr_url, hash, soup, results)
    # 19 ES - somatemps.me - Wordpress / Wordpress
    if curr_url.find('somatemps.me') > 0:                   es_somatemps_me.scrape(curr_url, hash, soup, results)
    # 20 ES - espana2000.es - Wordpress / Wordpress
    if curr_url.find('espana2000.es') > 0:                  es_espana2000_es.scrape(curr_url, hash, soup, results)
    # 21 ES - tradicionviva.es - Wordpress / Facebook
    if curr_url.find('tradicionviva.es') > 0:               es_tradicionviva_es.scrape(curr_url, hash, soup, results)
    # 22 ES - manos-limpias.es - Custom
    if curr_url.find('manos-limpias.es') > 0:               es_manos_limpias_es.scrape(curr_url, hash, soup, results)
    # 23 ES - laverdad.es - Custom / Custom
    if curr_url.find('laverdad.es') > 0:                    es_laverdad_es.scrape(curr_url, hash, soup, results)

    # 01 IT - termometropolitico.it - WordPress
    if curr_url.find('termometropolitico.it') > 0:          it_termometropolitico_it.scrape(curr_url, hash, soup, results)
    # 02 IT - termometropolitico.it - Custom / Custom
    if curr_url.find('gazzetta.it') > 0:                    it_gazzetta_it.scrape(curr_url, hash, soup, results)
    # 03 IT - liberoquotidiano.it - Custom / DISQUS + Facebook
    if curr_url.find('liberoquotidiano.it') > 0:            it_liberoquotidiano_it.scrape(curr_url, hash, soup, results)
    # 04 IT - fratelli-italia.it - WordPress
    if curr_url.find('fratelli-italia.it') > 0:             it_fratelli_italia_it.scrape(curr_url, hash, soup, results)
    # 05 IT - la7.it - Drupal
    if curr_url.find('la7.it') > 0:                         it_la7_it.scrape(curr_url, hash, soup, results)
    # 06 IT - ilpopulista.it - Custom
    if curr_url.find('ilpopulista.it') > 0:                 it_ilpopulista_it.scrape(curr_url, hash, soup, results)
    # 07 IT - imolaoggi.it - WordPress
    if curr_url.find('imolaoggi.it') > 0:                   it_imolaoggi_it.scrape(curr_url, hash, soup, results)
    # 08 IT - destra.it - WordPress / WordPress
    if curr_url.find('destra.it') > 0:                      it_destra_it.scrape(curr_url, hash, soup, results)
    # 09 IT - identità.com - Custom
    if curr_url.find('xn--identit-fwa.com') > 0:            it_identità_it.scrape(curr_url, hash, soup, results)
    # 10 IT - cartadiroma.org - WordPress
    if curr_url.find('cartadiroma.org') > 0:                it_cartadiroma_org.scrape(curr_url, hash, soup, results)
    # 11 IT - rainews.it - Custom
    if curr_url.find('rainews.it') > 0:                     it_rainews_it.scrape(curr_url, hash, soup, results)
    # 12 IT - ilprimatonazionale.it - WordPress
    if curr_url.find('ilprimatonazionale.it') > 0:          it_ilprimatonazionale_it.scrape(curr_url, hash, soup, results)

    # 01 EL - pentapostagma.gr - Drupal / DISQUS
    if curr_url.find('pentapostagma.gr') > 0:               el_pentapostagma_gr.scrape(curr_url, hash, soup, results)
    # 02 EL - makeleio.gr - WordPress / Wordpress
    if curr_url.find('makeleio.gr') > 0:                    el_makeleio_gr.scrape(curr_url, hash, soup, results)
    # 03 EL - katohika.gr - WordPress / Wordpress
    if curr_url.find('katohika.gr') > 0:                    el_katohika_gr.scrape(curr_url, hash, soup, results)
    # 04 EL - infognomonpolitics.gr - WordPress / DISQUS
    if curr_url.find('infognomonpolitics.gr') > 0:          el_infognomonpolitics_gr.scrape(curr_url, hash, soup, results)
    # 05 EL - defencereview.gr - WordPress
    if curr_url.find('defencereview.gr') > 0:               el_defencereview_gr.scrape(curr_url, hash, soup, results)
    # 06 EL - olympia.gr - WordPress / DISQUS
    if curr_url.find('olympia.gr') > 0:                     el_olympia_gr.scrape(curr_url, hash, soup, results)
    # 07 EL - voicenews.gr - WordPress
    if curr_url.find('voicenews.gr') > 0:                   el_voicenews_gr.scrape(curr_url, hash, soup, results)
    # 08 EL - vimaorthodoxias.gr - WordPress
    if curr_url.find('vimaorthodoxias.gr') > 0:             el_vimaorthodoxias_gr.scrape(curr_url, hash, soup, results)
    # 09 EL - arxaiaithomi.gr - WordPress
    if curr_url.find('arxaiaithomi.gr') > 0:                el_arxaiaithomi_gr.scrape(curr_url, hash, soup, results)
    # 10 EL - ekklisiaonline.gr - WordPress
    if curr_url.find('ekklisiaonline.gr') > 0:              el_ekklisiaonline_gr.scrape(curr_url, hash, soup, results)
    # 11 EL - hellenicns.gr - WordPress
    if curr_url.find('hellenicns.gr') > 0:                  el_hellenicns_gr.scrape(curr_url, hash, soup, results)
    # 12 EL - elikoncc.info - WordPress
    if curr_url.find('elikoncc.info') > 0:                  el_elikoncc_info.scrape(curr_url, hash, soup, results)
    # 13 EL - skai.gr - Drupal / DISQUS
    if curr_url.find('skai.gr') > 0:                        el_skai_gr.scrape(curr_url, hash, soup, results)
    # 14 EL - protothema.gr - ATCOM / ATCOM
    if curr_url.find('protothema.gr') > 0:                  el_protothema_gr.scrape(curr_url, hash, soup, results)
    # 15 EL - pronews.gr - WordPress / DISQUS
    if curr_url.find('pronews.gr') > 0:                     el_pronews_gr.scrape(curr_url, hash, soup, results)
    # 16 EL - pronews.gr - WordPress / DISQUS
    if curr_url.find('thepressproject.gr') > 0:             el_thepressproject_gr.scrape(curr_url, hash, soup, results)

    #  Write results
    file = open('Data\\scraper_web\\' + urlsplit(base_url).netloc + '_data.json', 'a', encoding='utf-8-sig')
    print('{} items added...'.format(len(results)))
    for result in results:  file.write(result + '\n')
    file.close()


    ''' DETECT LINKS '''
    # Load listed links
    try:
        file = open('Data\\scraper_web\\' + urlsplit(base_url).netloc + '_links.txt', 'r', encoding='utf-8')
        links = file.read().splitlines()
        file.close()
    except:
        #
        links = []
    already = len(links)
    print('{:} links already listed...'.format(already))

    # Detect new and update listed links
    for a in soup.find_all('a'):
        link = ''
        if a.has_attr('href'):
            a['href'] = a['href'].replace('https', 'http')
            # if a['href'].find('#') >= 0:  a['href'], sep, tail = a['href'].partition('#')
            if a['href'].startswith(base_url) > 0:
                link = a['href'].replace('\n', '').replace('\r', '').replace('\t', '').strip()
                # print(link)
            elif a['href'].find('http') < 0:
                link = base_url + '/' + a['href'].lstrip('/').replace('\n', '').replace('\r', '').replace('\t', '').strip()
                # print(link)
        if (link not in links) and ('!'+link not in links) and (len(link) > 0) and (link.find('#') < 0) and (link.find('reply') < 0) and (link.find('png') < 0) and (link.find('jpg') < 0) and (link.find('pdf') < 0) and (link.find('zip') < 0):
            links.append(link)

    # Display some link stats
    visited = 0
    for l in links:
        if l.startswith('!'):
            visited += 1
    print('{:} new links detected...'.format(len(links)-already))
    print('{:} links in total and {:} visited...'.format(len(links), visited))
    print('{:.1f}% of the site has been scraped...'.format(100 * visited / (len(links)+1)))
    if visited / (len(links)+1) > 0.8 or len(links) < 10:
        print('Most of the site has been scraped. Terminating...')
        sys.exit()


    ''' FIND A DESTINATION '''
    print('{} cycles remaining...'.format(cycles))

    # Find a new destination
    if cycles > 0:
        destination = base_url
        while len(links) > 0:
            r = random.randint(0, len(links) - 1)
            destination = links[r]
            if destination.startswith('!') == False:
                links[r] = '!' + destination
                break
            else:
                time.sleep(1)
                print("Selected an already visited link. Retrying...")
        print('Going to {}\n'.format(destination[:min(100, len(destination))]))

    # Update link list
    with open('Data\\scraper_web\\' + urlsplit(base_url).netloc + '_links.txt', 'w', encoding='utf-8') as file:
        #
        for link in links:  file.write(link + '\n')

    #  Go to the new destination
    if cycles > 0:
        time.sleep(1)
        cycles -= 1
        download(base_url, destination, cycles)