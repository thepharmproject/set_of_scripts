''' This python file serves as the starting script of the project '''


''' PYTHON SETUP '''
# a list of the required packages is listed here based on anaconda setup commands.
# conda create --name NLP python=3.7
# conda activate NLP


''' LIBRARIES IMPORTED '''
import os, sys, time, glob, argparse, string, json, re, random
from sklearn.metrics import classification_report
import analysis_nlp as an
import scraper_twitter as st
import scraper_web as sw
import scraper_youtube as sy
import single


''' EXTERNAL CONFIGURATION | DATA & METADATA COLLECTION (T2.1) & (T2.5) | CORPUS DEVELOPMENT (T2.9) '''
# ******************************************************************************************
# the following code lines assist in reading the main configuration file ("Config/main.txt").
# the processes that can be initialized are related to web scraping and text analyses.
def start():

    print('\nScript started...\n')

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
            elif line.find("[TEST-FUNCTIONS]") == 0:
                par1 = ''
                print("Initializing data testing")
                test()

        if par1 is None:    print('No valid parameter found, please check "Config/main.txt" file.')

    if os.path.exists('geckodriver.log'):
        os.remove('geckodriver.log')

    print('\nScript ended...')


''' HATE SPEECH DETECTION (T2.2) | GEOLOCATION ESTIMATION (T2.3) | LANGUAGE DETECTION (T2.4) | ENTITY COLLECTION (T2.7) | SENTIMENT ANALYSIS (T2.8) '''
# ******************************************************************************************
# this helper function assists the initialization of the implemented text analyses methods.
# data that is stored in JSON format ("Data" directory) is read and routed (as arguments) to
# the analysis methods that are implemented in the analysis_nlp.py file. the corresponding
# results are returned. these results will be stored in separate data files (*_processed.json)
# in the future to be routed for annotation and database storing.
def analyze_data(path, type='all', lang_ana=True, date_ana=True, hate_ana=True, term_ana=True, loc_ana=True, topic_ana=True, ent_ana=True):

    # read all files from path
    for file_path in glob.glob(path):

        data_upd = []
        corpus = []

        # read all data from each file
        print(' ')
        print('analyzing file:', file_path)
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            data = file.read().splitlines()

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

            # perform the analyses and update the entry
            if lang_ana:
                lang = an.detect_language(text)
                datum_json["meta"]["lang"] = lang
            if date_ana:
                date = an.detect_datetime(text, meta, lang)
                datum_json["meta"]["date"] = date
            if hate_ana:
                hate = an.detect_hate_fast(text, meta, lang)
                datum_json["meta"]["hate"] = hate
            if term_ana:
                terms = an.detect_terms(text, meta, lang)
                datum_json["meta"]["terms"] = terms
            if loc_ana:
                loc = an.detect_location(text, meta, lang)
                datum_json["meta"]["loc"] = loc
            data_upd.append(json.dumps(datum_json, ensure_ascii=False))

            # develop the corpus
            corpus.append(text)

        # write processed data to the file
        print(' ')
        print('writing processed file:', file_path[:-5] + '_processed.json')
        with open(file_path[:-5] + '_processed.json', 'w', encoding='utf-8-sig') as file:
            for datum_upd in data_upd:  file.write(datum_upd + '\n')

        # perform topic and entity modeling
        if len(corpus) > 10:
            print('\nanalyzing corpus for topics...')
            if topic_ana:   _, topics = an.topic_modeling(corpus)
            if ent_ana:     _, entities = an.entity_modeling(corpus)
        else:
            #
            print('\ncorpus too small to execute topic modeling...')

''' SUPPLEMENTARY METHODS FOR DEVELOPMENT & TESTING '''
# ******************************************************************************************
# helper methods/scripts for testing/deploying implemented workdflows and analysis methods.
# these are not for deployment, as they have been replaced by the external file configuration
# initialization.

# sw.download('http://sioeeu.wordpress.com', 'https://sioeeu.wordpress.com', False)
# sw.download('http://okdiario.com', 'http://okdiario.com', True)                                                    # OK
# sw.download('http://www.alertadigital.com', 'http://www.alertadigital.com', False)                                 # OK
# sw.download('http://www.periodistadigital.com', 'http://www.periodistadigital.com', False)                         # OK
# sw.download('http://www.elespanol.com', 'http://www.elespanol.com', False)                                         # OK
# sw.download('http://www.diarioya.es', 'http://www.diarioya.es', False)                                             # OK
# sw.download('http://gaceta.es', 'http://gaceta.es', False)                                                         # OK
# sw.download('http://www.voxespana.es', 'http://www.voxespana.es', False)                                           # OK
# sw.download('http://www.actuall.com', 'http://www.actuall.com', False)                                             # OK
# sw.download('http://casoaislado.com', 'http://casoaislado.com', False)                                             # OK
# sw.download('http://www.outono.net', 'http://www.outono.net', False)                                               # OK
# sw.download('http://www.lasvocesdelpueblo.com', 'http://www.lasvocesdelpueblo.com', False)                         # OK
# sw.download('http://disidentia.com', 'http://disidentia.com', False)                                               # OK
# sw.download('http://elcorreodeespana.com', 'http://elcorreodeespana.com', False)                                   # OK
# sw.download('http://www.mediterraneodigital.com', 'http://www.mediterraneodigital.com', False)                     # OK
# sw.download('http://www.elcorreo.com', 'http://www.elcorreo.com', False)                                           # OK
# sw.download('http://www.diariosur.es', 'http://www.diariosur.es', False)                                           # OK
# sw.download('http://www.huelvainformacion.es', 'http://www.huelvainformacion.es', False)                           # OK
# sw.download('http://www.hoy.es', 'http://www.hoy.es', False)                                                       # OK
# sw.download('http://somatemps.me', 'http://somatemps.me', False)                                                   # OK
# sw.download('http://espana2000.es', 'http://espana2000.es', False)                                                 # OK
# sw.download('http://www.tradicionviva.es', 'http://www.tradicionviva.es', False)                                   # OK
# sw.download('http://manos-limpias.es', 'http://manos-limpias.es', False)                                           # OK
# sw.download('http://www.laverdad.es', 'http://www.laverdad.es', False)                                             # OK

# sw.download('http://www.termometropolitico.it', 'http://www.termometropolitico.it', False)                         # OK
# sw.download('http://www.gazzetta.it', 'http://www.gazzetta.it', False)                                             # OK
# sw.download('http://www.liberoquotidiano.it', 'http://www.liberoquotidiano.it', False)                             # OK
# sw.download('http://www.fratelli-italia.it', 'http://www.fratelli-italia.it', False)                               # OK
# sw.download('http://www.la7.it', 'http://www.la7.it', False)                                                       # OK
# sw.download('http://www.ilpopulista.it', 'http://ilpopulista.it', False)                                           # OK
# sw.download('http://www.imolaoggi.it', 'http://www.imolaoggi.it', False)                                           # OK
# sw.download('http://www.ilprimatonazionale.it', 'http://www.ilprimatonazionale.it', False)                         # OK
# sw.download('http://www.destra.it', 'http://www.destra.it', False)                                                 # OK
# sw.download('http://xn--identit-fwa.com/', 'http://xn--identit-fwa.com', False)                                    # OK
# sw.download('http://www.cartadiroma.org/news', 'https://www.cartadiroma.org/news', False)                          # OK
# sw.download('http://www.libero.it', 'http://www.libero.it', False)                                                 # Problem with links
# sw.download('http://www.corriere.it', 'http://www.corriere.it', False)                                             # Custom CMS

# sw.download('http://www.pentapostagma.gr', 'http://www.pentapostagma.gr', False)                                    # OK
# sw.download('http://www.makeleio.gr', 'http://www.makeleio.gr', False)                                              # OK
# sw.download('http://katohika.gr', 'http://katohika.gr', False)                                                      # OK
# sw.download('http://infognomonpolitics.gr', 'http://infognomonpolitics.gr/', False)                                 # OK
# sw.download('http://defencereview.gr', 'http://defencereview.gr', False)                                            # OK
# sw.download('http://olympia.gr', 'http://olympia.gr', False)                                                        # OK
# sw.download('http://voicenews.gr', 'https://voicenews.gr', False)                                                   # OK
# sw.download('http://www.vimaorthodoxias.gr', 'http://www.vimaorthodoxias.gr', False)                                # OK
# sw.download('http://arxaiaithomi.gr', 'http://arxaiaithomi.gr', False)                                              # OK
# sw.download('http://www.ekklisiaonline.gr', 'http://www.ekklisiaonline.gr', False)                                  # OK
# sw.download('http://hellenicns.gr', 'http://hellenicns.gr', False)                                                  # OK
# sw.download('http://www.elikoncc.info', 'http://www.elikoncc.info', False)                                          # OK
# sw.download('http://www.skai.gr', 'http://www.skai.gr', False)                                                      # OK
# sw.download('http://www.protothema.gr', 'http://www.protothema.gr', False)                                          # OK
# sw.download('http://thepressproject.gr', 'http://thepressproject.gr', False)                                        # OK
# sw.download('http://skeftomasteellhnika.blogspot.com', 'http://skeftomasteellhnika.blogspot.com', False)            # OK

# st.stream('el')
# st.stream('es')
# st.stream('it')

# youtube define search query and max number of results
# sy.search('refugees', 1000)

# single.download('https://www.facebook.com/groups/8080169598/')                                                    # facebook group
# single.download('https://twitter.com/Conclavios/status/1285176673214894080')                                      # twitter tweet
# single.download('https://www.youtube.com/watch?v=fDWFVI8PQOI')                                                    # youtube comments
# single.download('https://www.makeleio.gr/επικαιροτητα/Ο-υπουργός-παιδεραστής-και-η-αποκάλυ/')                     # website content
def test(sample_size=10, reset=True):

    # init vars
    cor = 0
    all = 0
    y_true = []
    y_pred = []

    # clean sample files
    if reset:
        if os.path.exists('Datasets/hate_migrants_sampled.txt'):
            os.remove('Datasets/hate_migrants_sampled.txt')
        if os.path.exists('Datasets/no_hate_migrants_sampled.txt'):
            os.remove('Datasets/no_hate_migrants_sampled.txt')

    # read and analyze hate speech data
    try:
        with open('Datasets/hate_migrants_sampled.txt', 'r', encoding='utf-8-sig') as file:
            samples = file.read().splitlines()
    except:
        with open('Datasets/hate_migrants.txt', 'r', encoding='utf-8-sig') as file:
            data = file.read().splitlines()
        samples = random.choices(data, k=int(sample_size/2))
        print('writing sampled hate speech data')
        with open('Datasets/hate_migrants_sampled.txt', 'w', encoding='utf-8-sig') as file:
            for datum in samples:  file.write(datum + '\n')
    print('\nanalyzing hate speech data with {} samples'.format(len(samples)))
    for datum in samples:
        print('\nAnalyzing item {}/{} with text {}'.format(all+1, len(samples), datum[:120]))
        lang = an.detect_language(datum)
        hate = an.detect_hate_fast(datum, None, lang)
        if len(hate) > 0:   y_pred.append(1)
        else:               y_pred.append(0)
        y_true.append(1)
        if len(hate) >= 1:   cor = cor + 1
        all = all + 1

    # read and analyze no hate speech data
    try:
        with open('Datasets/no_hate_migrants_sampled.txt', 'r', encoding='utf-8-sig') as file:
            samples = file.read().splitlines()
    except:
        with open('Datasets/no_hate_migrants.txt', 'r', encoding='utf-8-sig') as file:
            data = file.read().splitlines()
        samples = random.choices(data, k=int(sample_size / 2))
        print('writing sampled no hate speech data')
        with open('Datasets/no_hate_migrants_sampled.txt', 'w', encoding='utf-8-sig') as file:
            for datum in samples:  file.write(datum + '\n')
    print('\nanalyzing no hate speech data with {} samples'.format(len(samples)))
    for datum in samples:
        print('\nAnalyzing item {}/{} with text {}'.format(all + 1, len(samples), datum[:120]))
        lang = an.detect_language(datum)
        hate = an.detect_hate_fast(datum, None, lang)
        if len(hate) > 0:   y_pred.append(1)
        else:               y_pred.append(0)
        y_true.append(0)
        if len(hate) <= 0:  cor = cor + 1
        all = all + 1

    # present results
    print('\nClassification report')
    print(classification_report(y_true, y_pred, target_names=['No hate', 'Hate']))
    print('Classification accuracy: {:.2}'.format(cor/all))


''' STARTING POINT OF THE SCRIPT '''
# the following line invokes the main method for running all available processing flows
# of the project
start()