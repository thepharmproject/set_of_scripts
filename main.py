''' This python file implements various nlp analysis methods '''


''' PYTHON SETUP '''
# a list of the required packages is listed here based on anaconda setup commands.
# conda create --name NLP python=3.7
# conda activate NLP


''' LIBRARIES IMPORTED '''
import sys, time, glob, argparse, string, json, re
import analysis_nlp as an
import scraper_twitter as st
import scraper_web as sw
import scraper_youtube as sy
import single


''' EXTERNAL INITIALIZATION - DATA & METADATA GATHERING (T2.1) & (T2.5) '''
# the following code lines assist in reading the main configuration file ("Config/main.txt").
# the processes that can be initialized are related to semi-structured (text) web scraping
# and text analyses. in specific:
# [TWITTER-STREAM] parameter invokes the routine for collecting tweets from twitter.
# "scraper_twitter.py" implements this specific routine
# the specified parameter can be "EL", "EN", "ES", "IT", exploiting the appropriate dictionary
# with terms for filtering tweets via the twitter stream method. the results are stored to
# "Data/scraper_twitter.json" file. the twitter api is used.
# [YOUTUBE-SEARCH] parameter invokes the routine for collecting video comments from youtube.
# "scraper_youtube.py" implements this routine. the corresponding argument should be a keyword
# (or list of keywords separated by spaces) for executing the search procedure. the results
# are stored to "Data/scraper_youtube.json" file. the google api is used.
# [WEBSITE-SINGLE] parameter invokes the routine for collecting posts from facebook groups,
# youtube videos and websites. data from facebook and youtube is structured, whereas for the
# websites is unstructured. "single_facebook.py", "single_youtube.py" and "single_web.py"
# implement the required routines. data are stored to "Data/single_facebook_data.json",
# "Data/single_youtube_data.json" and "Data/single_web_data.json" files. you should set the
# url of the website to by scraped as argument.
# [WEBSITE-MASS] parameter invokes the routine for collecting video comments from youtube.
# "scraper_web.py" implements this specific routine and all py files under the "Scrapers"
# dictionary
# the corresponding argument can be a keyword (or list of keywords separeted by spaces) for
# executing a search procedure. the
# [ANALYZE-DATA] parameter invokes the routine for collecting video comments from youtube.
# "scraper_youtube.py" implements this specific routine.
# the corresponding argument can be a keyword (or list of keywords separeted by spaces) for
# executing a search procedure. the
print('\nScript started...\n')
def start():
    with open('Config\\main.txt', 'r', encoding='utf-8') as file:
        lines = file.read().splitlines()

        par1 = None
        par2 = None

        for line in lines:
            if line.find("[TWITTER-STREAM]") == 0:
                par1 = re.search("\"(.*?)\"", line).group(1)
                print("Initializing twitter stream with parameter:", par1)
                st.stream(par1)
            elif line.find("[YOUTUBE-SEARCH]") == 0:
                #
                par1 = re.search("\"(.*?)\"", line).group(1)
            elif line.find("[YOUTUBE-SEARCH-NRESULTS]") == 0:
                par2 =  int(re.search("\"(.*?)\"", line).group(1))
                print("Initializing youtube search with parameters:", par1, par2)
                sy.search(par1, par2)
            elif line.find("[WEBSITE-SINGLE]") == 0:
                par1 = re.search("\"(.*?)\"", line).group(1)
                print("Initializing single website scrape with parameter:", par1)
                single.download(par1)
            elif line.find("[WEBSITE-MASS]") == 0:
                #
                par1 = re.search("\"(.*?)\"", line).group(1)
            elif line.find("[WEBSITE-MASS-CYCLES]") == 0:
                par2 = int(re.search("\"(.*?)\"", line).group(1))
                print("Initializing mass website scrape with parameters:", par1, par2)
                sw.download(par1, par1, par2)
            elif line.find("[ANALYZE-DATA]") == 0:
                par1 = re.search("\"(.*?)\"", line).group(1)
                print("Initializing data analysis with parameter:", par1)
                analyze_data(par1)

        if par1 is None:    print('No valid parameter found, please check "Config/main.txt" file.')


''' HATE-SPEECH DETECTION (T2.2) | GEOLOCATION ESTIMATION (T2.3) | LANGUAGE DETECTION (T2.4) '''
# this helper function assists the initialization of the implemented text analyses methods.
# data that is stored in JSON format ("Data" directory) is read and routed (as arguments) to
# the analysis methods that are implemented in the analysis_nlp.py file. the corresponding results
# are returned. these results will be stored in separate data files (*_processed.json) in the future
# to be routed for annotation and database storing.
def analyze_data(path='Data\\scraper_web\\*es_data.json', type='all'):

    # read all files from path
    for file_path in glob.glob(path):

        data_upd = []
        corpus = []

        # read all data from each file
        print(' ')
        print('analyzing file:', file_path)
        file = open(file_path, 'r', encoding='utf-8-sig')
        data = file.read().splitlines()
        file.close()

        # read and analyze the text for each entry
        for datum_i, datum in enumerate(data):
            # if datum_i > 10: break
            print(' ')
            print('loading entry #{}...'.format(datum_i))
            datum_json = json.loads(datum)
            try:
                print('type:', datum_json['meta']['type'])
                text = datum_json['text']
                try:    meta = datum_json['meta']['meta']
                except: meta = None
                if datum_json['meta']['type'] != type and type != 'all':
                    print('data does not match type...')
                    continue
            except:
                print('cannot load data... (JSON error)')
                continue

            print('start of text is: \'{}\''.format(text[:100]))

            # perform the analyses
            lang = an.detect_language(text)
            date = an.detect_datetime(text, meta, lang)
            hate = an.detect_hate(text, meta, lang)
            terms = an.detect_terms(text, meta, lang)
            loc = an.detect_location(text, meta, lang)

            # update the entry
            datum_json["meta"]["lang"] = lang
            datum_json["meta"]["date"] = date
            datum_json["meta"]["hate"] = hate
            datum_json["meta"]["terms"] = terms
            datum_json["meta"]["loc"] = loc
            data_upd.append(json.dumps(datum_json, ensure_ascii=False))

            # develop the corpus
            corpus.append(text)

        # write processed data to the file
        print(' ')
        print('writing processed file:', file_path[:-5] + '_processed.json')
        file = open(file_path[:-5] + '_processed.json', 'w', encoding='utf-8-sig')
        for datum_upd in data_upd:  file.write(datum_upd + '\n')
        file.close()

        # topics = an.topic_modeling_tfid('es')
        # topics = an.topic_modeling(corpus, language)


''' STARTING POINT OF THE SCRIPT '''
# the following line invokes the main method for running all available methods/workflows of
# the project
start()

''' SUPPLEMENTARY METHODS '''
# helper methods/scripts for testing/deploying implemented workdflows and analysis methods.
# these are not for deployment, as they have been replaced by the external file configuration
# logic.

# sw.download('http://sioeeu.wordpress.com', 'https://sioeeu.wordpress.com', False)
# sw.download('http://okdiario.com', 'http://okdiario.com', True)                                                   # OK
#sw.download('http://www.alertadigital.com', 'http://www.alertadigital.com', False)                                 # OK
#sw.download('http://www.periodistadigital.com', 'http://www.periodistadigital.com', False)                         # OK
#sw.download('http://www.elespanol.com', 'http://www.elespanol.com', False)                                         # OK
#sw.download('http://www.diarioya.es', 'http://www.diarioya.es', False)                                             # OK
#sw.download('http://gaceta.es', 'http://gaceta.es', False)                                                         # OK
#sw.download('http://www.voxespana.es', 'http://www.voxespana.es', False)                                           # OK
#sw.download('http://www.actuall.com', 'http://www.actuall.com', False)                                             # OK
#sw.download('http://casoaislado.com', 'http://casoaislado.com', False)                                             # OK
#sw.download('http://www.outono.net', 'http://www.outono.net', False)                                               # OK
#sw.download('http://www.lasvocesdelpueblo.com', 'http://www.lasvocesdelpueblo.com', False)                         # OK
#sw.download('http://disidentia.com', 'http://disidentia.com', False)                                               # OK
#sw.download('http://elcorreodeespana.com', 'http://elcorreodeespana.com', False)                                   # OK
#sw.download('http://www.mediterraneodigital.com', 'http://www.mediterraneodigital.com', False)                     # OK
#sw.download('http://www.elcorreo.com', 'http://www.elcorreo.com', False)                                           # OK
#sw.download('http://www.diariosur.es', 'http://www.diariosur.es', False)                                           # OK
#sw.download('http://www.huelvainformacion.es', 'http://www.huelvainformacion.es', False)                           # OK
#sw.download('http://www.hoy.es', 'http://www.hoy.es', False)                                                       # OK
#sw.download('http://somatemps.me', 'http://somatemps.me', False)                                                   # OK
#sw.download('http://espana2000.es', 'http://espana2000.es', False)                                                 # OK
#sw.download('http://www.tradicionviva.es', 'http://www.tradicionviva.es', False)                                   # OK
#sw.download('http://manos-limpias.es', 'http://manos-limpias.es', False)                                           # OK
#sw.download('http://www.laverdad.es', 'http://www.laverdad.es', False)                                             # OK

#sw.download('http://www.termometropolitico.it', 'http://www.termometropolitico.it', False)                         # OK
#sw.download('http://www.gazzetta.it', 'http://www.gazzetta.it', False)                                             # OK
#sw.download('http://www.liberoquotidiano.it', 'http://www.liberoquotidiano.it', False)                             # OK
#sw.download('http://www.fratelli-italia.it', 'http://www.fratelli-italia.it', False)                               # OK
#sw.download('http://www.la7.it', 'http://www.la7.it', False)                                                       # OK
#sw.download('http://www.ilpopulista.it', 'http://ilpopulista.it', False)                                           # OK
#sw.download('http://www.imolaoggi.it', 'http://www.imolaoggi.it', False)                                           # OK
#sw.download('http://www.ilprimatonazionale.it', 'http://www.ilprimatonazionale.it', False)                         # OK
#sw.download('http://www.destra.it', 'http://www.destra.it', False)                                                 # OK
#sw.download('http://xn--identit-fwa.com/', 'http://xn--identit-fwa.com', False)                                    # OK
#sw.download('http://www.cartadiroma.org/news', 'https://www.cartadiroma.org/news', False)                          # OK
#sw.download('http://www.libero.it', 'http://www.libero.it', False)                                                 # Problem with links
#sw.download('http://www.corriere.it', 'http://www.corriere.it', False)                                             # Custom CMS

#sw.download('http://www.pentapostagma.gr', 'http://www.pentapostagma.gr', False)                                    # OK
#sw.download('http://www.makeleio.gr', 'http://www.makeleio.gr', False)                                              # OK
#sw.download('http://katohika.gr', 'http://katohika.gr', False)                                                      # OK
#sw.download('http://infognomonpolitics.gr', 'http://infognomonpolitics.gr/', False)                                 # OK
#sw.download('http://defencereview.gr', 'http://defencereview.gr', False)                                            # OK
#sw.download('http://olympia.gr', 'http://olympia.gr', False)                                                        # OK
#sw.download('http://voicenews.gr', 'https://voicenews.gr', False)                                                   # OK
#sw.download('http://www.vimaorthodoxias.gr', 'http://www.vimaorthodoxias.gr', False)                                # OK
#sw.download('http://arxaiaithomi.gr', 'http://arxaiaithomi.gr', False)                                              # OK
#sw.download('http://www.ekklisiaonline.gr', 'http://www.ekklisiaonline.gr', False)                                  # OK
#sw.download('http://hellenicns.gr', 'http://hellenicns.gr', False)                                                  # OK
#sw.download('http://www.elikoncc.info', 'http://www.elikoncc.info', False)                                          # OK
#sw.download('http://www.skai.gr', 'http://www.skai.gr', False)                                                      # OK
#sw.download('http://www.protothema.gr', 'http://www.protothema.gr', False)                                          # OK
#sw.download('http://thepressproject.gr', 'http://thepressproject.gr', False)                                        # OK
#sw.download('http://skeftomasteellhnika.blogspot.com', 'http://skeftomasteellhnika.blogspot.com', False)            # OK
#sw.download('http://www.pronews.gr', 'http://www.pronews.gr', False)                                                # ERROR

# st.stream('el')
# st.stream('es')
# st.stream('it')

# youtube define search query and max number of results
# sy.search('refugees', 1000)

# single.download('https://www.facebook.com/groups/8080169598/')                                                    # facebook group
# single.download('https://twitter.com/Conclavios/status/1285176673214894080')                                      # twitter tweet
# single.download('https://www.youtube.com/watch?v=fDWFVI8PQOI')                                                    # youtube comments
# single.download('https://www.makeleio.gr/επικαιροτητα/Ο-υπουργός-παιδεραστής-και-η-αποκάλυ/')                     # website content
print('\nScript ended...')

