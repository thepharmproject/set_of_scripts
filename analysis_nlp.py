''' This python file implements various nlp analysis methods '''


''' PYTHON SETUP '''
# a list of the required packages is listed here based on anaconda setup commands.
# conda install -c conda-forge parsedatetime
# conda install -c conda-forge dateparser
# conda install -c conda-forge datefinder
# conda install -c conda-forge textblob
# conda install -c conda-forge googletrans
# conda install -c conda-forge langdetect
# conda install -c conda-forge geopy
# conda install -c conda-forge jellyfish
# conda install -c conda-forge matplotlib
# conda install -c anaconda scikit-learn
# conda install -c conda-forge spacy
# python -m spacy download en_core_web_sm
# python -m spacy download en_core_web_md
# python -m spacy download el_core_news_sm
# python -m spacy download el_core_news_md
# python -m spacy download es_core_news_sm
# python -m spacy download es_core_news_md
# python -m spacy download it_core_news_sm
# python -m spacy download it_core_news_md


''' LIBRARIES IMPORTED '''
import time, argparse, string, json, sys
from textblob import TextBlob
from googletrans import Translator
from langdetect import detect
import parsedatetime, dateparser, datefinder
from geopy.geocoders import Nominatim, GoogleV3
from difflib import SequenceMatcher
import jellyfish
import spacy
from spacy import displacy
from spacy.matcher import Matcher, PhraseMatcher
# from spacy.lang.en import English, Spanish, Italian

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from collections import Counter

import utilities as utils


''' ANALYSIS METHODS '''
# detect language from text. a chained approach is adopted for improved robustness.
# textblob, google translate and langdetect services are used. if a service fails
# the result form the next one is requested.
def detect_language(text):
    print('* language detection')

    lang = None
    try:
        lang = TextBlob(text[:100]).detect_language()
        print('\tlanguage is (TextBlob):', lang)
    except:
        print('\tTextBlob failed')
        try:
            lang = Translator().detect(text[:100]).lang
            print('\tlanguage is (Google Translator):', lang,)
        except:
            print('\tGoogle Translator failed')
            try:
                lang = detect(text[:100])
                print('\tlanguage is (langdetect):', lang)
            except:
                print('\tlangdetect failed')

    if lang is None: print('\tlanguage detection failed...')
    return lang

# detect datetime from metadata and text. a chained approach is adopted here as well.
# dateparser, datefinder and parsedatetime packages are exploited ranked from higher
# accuracy to higher probability of returning a result. if the most accurate fails to
# detect the datetime object, the next service is called and so on. detection is based
# in metadata, where date date information is commonly present. if datetime detection
# fails for all services in metadata, the same workflow is applied to text data.
def detect_datetime(text, meta, lang):

    print('* datetime detection')

    # initialize results
    results = []

    date = None
    print('\tmeta:', meta)
    if len(results) == 0:
        try:
            date = dateparser.parse(meta)
            if date is not None:
                print('\tdateparser meta:', date)
                results.append(str(date))
        except: print('\tdateparser meta failed')
    if len(results) == 0:
        print('\tdateparser meta: none')
        try:
            dates = datefinder.find_dates(meta)
            for date_item in dates:
                date = date_item
                print('\tdatefinder meta:', date)
                results.append(str(date))
                break
        except: print('\tdatefinder meta failed')
    if len(results) == 0:
        print('\tdatefinder meta: none')
        try:
            date = dateparser.parse(text)
            if date is not None:
                print('\tdateparser text:', date)
                results.append(str(date))
        except: print('\tdateparser text failed')
    if len(results) == 0:
        print('\tdateparser text: none')
        try:
            dates = datefinder.find_dates(text)
            for date_item in dates:
                date = date_item
                print('\tdatefinder meta:', date)
                results.append(str(date))
                break
        except: print('\tdatefinder text failed')
    if len(results) == 0:
        print('\tdatefinder text: none')
        print('\tno datetime information found in text')
        # datetime = parsedatetime.Calendar().parse(meta)
        date = ''
        results.append(str(date))

    return results[0]

# detect hate speech in text. two approaches are implemented (mode=0,1,2). the first one
# is based in a dictionary of terms for four different languages, english, greek, italian
# and spanish. a language model is loaded (according to the language of the text), common
# practices are followed (lowercasing, lemmatization, stop word and punctuation removal), and
# the targeted terms are being searched in the text. if found, text segments are denoted as
# "hate speech". the second one is based in word vectors allowing for a more semantic detection.
# the same workflow is followed for this method as well (lemmatization etc.). if mode is set to
# "2" the union of the results from both methods is returned.
def detect_hate(text, meta, lang, mode=2):

    print('* hate speech detection with mode', mode)

    # initialize the results list
    results = []

    # load the appropriate language model
    if mode == 1 or mode == 2:                          model_suffix = 'md'
    else:                                               model_suffix = 'sm'
    if lang == 'en':                                    nlp = spacy.load(lang + '_core_web_' + model_suffix)
    if lang == 'el' or lang == 'es' or lang == 'it':    nlp = spacy.load(lang + '_core_news_' + model_suffix)
    else:                                               return

    # load the filter terms from the dictionaries - safe words and phrases first
    with open('Dictionaries\\dictionary_' + lang + '_s.txt', 'r', encoding='utf-8') as file:    terms_list = file.read().splitlines()
    # load secondary words
    with open('Dictionaries\\dictionary_' + lang + '_a.txt', 'r', encoding='utf-8') as file:    terms_a = file.read().splitlines()
    # load primary words
    with open('Dictionaries\\dictionary_' + lang + '_b.txt', 'r', encoding='utf-8') as file:    terms_b = file.read().splitlines()
    # synthesize phrases
    for term_a in terms_a:
        for term_b in terms_b:
            # find all suffixes and make all possible combinations
            if term_a.find("/") > 0:    term_a = term_a[:term_a.find("/")]
            if term_b.find("/") > 0:    term_b = term_b[:term_b.find("/")]
            # if the suffix ends with a "-" join the words instead of making a phrase
            if term_a[-1] =='-':        terms_list.append(term_a[:-1] + term_b)
            else:                       terms_list.append(term_a + ' ' + term_b)

    time_c = time.time()
    # print('\tload dictionary:', time_c - time_b)

    # find matches in text and search phrases
    words_token = nlp(text)

    # for each search phrase
    for terms in terms_list:
        # print('analyzing search term \'{}\''.format(terms))
        matches = []

        # for each word of the search phrase
        for term_token in nlp(terms): #terms.split()

            if len(matches) > 0 and matches[0] < 0:
                #
                break

            word_pos = -1
            matches.append(word_pos)
            term_t = utils.clean_accent(term_token.lemma_.lower())
            # term_t = utils.clean_accent(term_token.lower())

            # for each word of the text
            for word_token in words_token:

                word_pos += 1
                word_t = utils.clean_accent(word_token.lemma_.lower())

                # string manipulation
                if mode == 0 or mode == 2:
                    score = SequenceMatcher(None, word_t, term_t).ratio()
                    match = word_t.find(term_t[:max(5, len(term_t)-3)])
                    if score > 0.7 and match == 0:
                        # print('\tstring manipulation for term \"{}\" and word \"{}\" with score {:.2f}'.format(term_token, word_token, score))
                        if not word_pos in matches: matches[len(matches)-1] = word_pos
                        break

                # word-vector similarity
                if mode == 1 or mode == 2:   # word vectors
                    if word_token.has_vector and term_token.has_vector and len(word_token.text) > 5:
                        score = term_token.similarity(word_token)
                        if score > 0.8:
                            # print('\tword-vector for term \"{}\" and word \"{}\" with score {:.2f}:'.format(term_token, word_token, score))
                            if not word_pos in matches: matches[len(matches)-1] = word_pos
                            break

        # confirm matches and locate text
        match = True
        for i in range(len(matches)):
            if matches[i] < 0:
                match = False
                matches.sort()
        if match == True:
            # print('\tfound hate-speech for term \'{}\' positions are {}'.format(terms, matches))

            # print the whole segment
            # results.append('')
            # for i in range(matches[0], matches[-1]+1):    results[-1] += words_token[i].text + ' '
            # print('\tpart of text:', results[-1])

            # print just the phrase
            results.append('(')
            for i in range(len(matches)):   results[-1] += words_token[matches[i]].text + ' '
            results[-1] += '| ' + terms + ')'

    time_d = time.time()
    print('\tanalyze phrase: {:.2f}'.format(time_d - time_c))

    # transform results to text
    results_txt = ''
    for result in results:
        #
        results_txt = results_txt + result + ", "
    results_txt = results_txt[:-2]
    print('\thate speech:', results_txt)

    return results_txt

# a simple approach for suggesting frequent words found in texts. this can help for expanding the
# list of terms found in the dictionaries for filtering data for hate speech. this method can be
# used in texts that already have been marked as "hate speech".
def detect_terms(text, meta, lang):

    print('* term detection')

    # initialize results
    results = []

    # load the appropriate spacy model and isolate terms named entity gpe, loc, fac, org
    if lang == 'en':                                    nlp = spacy.load('en_core_web_sm')
    elif lang == 'el' or lang == 'es' or lang == 'it':  nlp = spacy.load(lang + '_core_news_sm')
    else:                                               return

    # remove stopwords, punctuation marks and make characters lowercase
    words = [token.lemma_.lower() for token in nlp(text) if token.is_stop != True and token.is_punct != True]

    # count frequency of words
    word_freq = Counter(words)
    common_words = word_freq.most_common(5)
    # print('\t', common_words)

    # filter frequent terms
    for common_word in common_words:
        if common_word[1] >= 3 and len(common_word[0]) >= 3:
            results.append(common_word[0])
            # print('\tcommnon word:', common_word[0])

    # transform results to text
    results_txt = ''
    for result in results:
        #
        results_txt = results_txt + result + ", "
    results_txt = results_txt[:-2]
    print('\tcommnon words:', results_txt)

    return results_txt

# a method for detecting geolocation from text. geopy with nominatim geocoder are used. entities in
# the following ranking are preferred: GPE (countries, cities, states), LOC (mountains, bodies of
# water), FAC (buildings, airports, highways etc.), ORG (companies, agancies, institutions etc.).
def detect_location(text, meta, lang):

    print('* location detection')

    # initialize results
    results = []

    # load the nominatim geopy geocoder
    n = Nominatim(user_agent="http")

    # load the appropriate spacy model and isolate terms named entity gpe, loc, fac, org
    if lang == 'en':                                    nlp = spacy.load('en_core_web_sm')
    elif lang == 'el' or lang == 'es' or lang == 'it':  nlp = spacy.load(lang + '_core_news_sm')
    else:                                               return
    ents = nlp(text).ents

    # find gpe entities
    if len(results) == 0:
        for ent in ents:
            # print(ent.text, ent.start_char, ent.end_char, ent.label_) #label_ -> ORG, GPE, MONEY
            if ent.label_ == 'GPE':
                geo = n.geocode(ent.text, language='en')
                if geo is not None:
                    results.append([ent.text, geo.raw["display_name"].split(",")[-1], geo.raw["lat"], geo.raw["lon"]])
                    # print('\tpossible locations (GPE):', results[-1])
    # try for fac entities
    if len(results) == 0:
        for ent in ents:
            if ent.label_ == 'FAC':
                geo = n.geocode(ent.text, language='en')
                if geo is not None:
                    results.append([ent.text, geo.raw["display_name"].split(",")[-1], geo.raw["lat"], geo.raw["lon"]])
                    # print('\tpossible locations (FAC):', results[-1])
    # try for org entities
    if len(results) == 0:
        for ent in ents:
            if ent.label_ == 'ORG':
                geo = n.geocode(ent.text, language='en')
                if geo is not None:
                    results.append([ent.text, geo.raw["display_name"].split(",")[-1], geo.raw["lat"], geo.raw["lon"]])
                    # print('\tpossible locations (ORG):', results[-1])
    # try for loc entities
    if len(results) == 0:
        for ent in ents:
            if ent.label_ == 'LOC':
                geo = n.geocode(ent.text, language='en')
                if geo is not None:
                    results.append([ent.text, geo.raw["display_name"].split(",")[-1], geo.raw["lat"], geo.raw["lon"]])
                    # print('\tpossible locations (LOC):', results[-1])

    # estimate only one location
    words = []
    for result in results:  words.append(utils.clean_whitespaces(result[1]))
    word_freq = Counter(words)
    common_words = word_freq.most_common(5)
    results = []
    for common_word in common_words:
        results.append(common_word[0])
        # break
    #print('\testimated location:', results)

    # transform results to text
    results_txt = ''
    for result in results:
        #
        results_txt = results_txt + result + ", "
    results_txt = results_txt[:-2]
    print('\testimated locations:', results_txt)

    return results_txt

# a method for topic modeling based on tfid (term frequency–inverse document frequency) approach. a
# list of topics is created based on a corpus of text items.
def topic_modeling_tfid(corpus):

    print('* topic modeling tfid')

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())

# a method for topic modeling based on lda (latent dirichlet allocation) approach. a list of topics
# is created based on a corpus of text items.
def topic_modeling_lda(corpus):

    print('* topic modeling lda')

    ####_____additional stop words_____####
    # from sklearn.feature_extraction import text
    # stop_words = text.ENGLISH_STOP_WORDS.union(my_additional_stop_words)
    # italian stopwords
    # ["a","abbastanza","abbia","abbiamo","abbiano","abbiate","accidenti","ad","adesso","affinché","agl","agli","ahime","ahimè","ai","al","alcuna","alcuni","alcuno","all","alla","alle","allo","allora","altre","altri","altrimenti","altro","altrove","altrui","anche","ancora","anni","anno","ansa","anticipo","assai","attesa","attraverso","avanti","avemmo","avendo","avente","aver","avere","averlo","avesse","avessero","avessi","avessimo","aveste","avesti","avete","aveva","avevamo","avevano","avevate","avevi","avevo","avrai","avranno","avrebbe","avrebbero","avrei","avremmo","avremo","avreste","avresti","avrete","avrà","avrò","avuta","avute","avuti","avuto","basta","ben","bene","benissimo","brava","bravo","buono","c","caso","cento","certa","certe","certi","certo","che","chi","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cinque","cio","cioe","cioè","circa","citta","città","ciò","co","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","cominci","comprare","comunque","con","concernente","conclusione","consecutivi","consecutivo","consiglio","contro","cortesia","cos","cosa","cosi","così","cui","d","da","dagl","dagli","dai","dal","dall","dalla","dalle","dallo","dappertutto","davanti","degl","degli","dei","del","dell","della","delle","dello","dentro","detto","deve","devo","di","dice","dietro","dire","dirimpetto","diventa","diventare","diventato","dopo","doppio","dov","dove","dovra","dovrà","dovunque","due","dunque","durante","e","ebbe","ebbero","ebbi","ecc","ecco","ed","effettivamente","egli","ella","entrambi","eppure","era","erano","eravamo","eravate","eri","ero","esempio","esse","essendo","esser","essere","essi","ex","fa","faccia","facciamo","facciano","facciate","faccio","facemmo","facendo","facesse","facessero","facessi","facessimo","faceste","facesti","faceva","facevamo","facevano","facevate","facevi","facevo","fai","fanno","farai","faranno","fare","farebbe","farebbero","farei","faremmo","faremo","fareste","faresti","farete","farà","farò","fatto","favore","fece","fecero","feci","fin","finalmente","finche","fine","fino","forse","forza","fosse","fossero","fossi","fossimo","foste","fosti","fra","frattempo","fu","fui","fummo","fuori","furono","futuro","generale","gente","gia","giacche","giorni","giorno","giu","già","gli","gliela","gliele","glieli","glielo","gliene","grande","grazie","gruppo","ha","haha","hai","hanno","ho","i","ie","ieri","il","improvviso","in","inc","indietro","infatti","inoltre","insieme","intanto","intorno","invece","io","l","la","lasciato","lato","le","lei","li","lo","lontano","loro","lui","lungo","luogo","là","ma","macche","magari","maggior","mai","male","malgrado","malissimo","me","medesimo","mediante","meglio","meno","mentre","mesi","mezzo","mi","mia","mie","miei","mila","miliardi","milioni","minimi","mio","modo","molta","molti","moltissimo","molto","momento","mondo","ne","negl","negli","nei","nel","nell","nella","nelle","nello","nemmeno","neppure","nessun","nessuna","nessuno","niente","no","noi","nome","non","nondimeno","nonostante","nonsia","nostra","nostre","nostri","nostro","novanta","nove","nulla","nuovi","nuovo","o","od","oggi","ogni","ognuna","ognuno","oltre","oppure","ora","ore","osi","ossia","ottanta","otto","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","peggio","per","perche","perchè","perché","percio","perciò","perfino","pero","persino","persone","però","piedi","pieno","piglia","piu","piuttosto","più","po","pochissimo","poco","poi","poiche","possa","possedere","posteriore","posto","potrebbe","preferibilmente","presa","press","prima","primo","principalmente","probabilmente","promesso","proprio","puo","pure","purtroppo","può","qua","qualche","qualcosa","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quarto","quasi","quattro","quel","quella","quelle","quelli","quello","quest","questa","queste","questi","questo","qui","quindi","quinto","realmente","recente","recentemente","registrazione","relativo","riecco","rispetto","salvo","sara","sarai","saranno","sarebbe","sarebbero","sarei","saremmo","saremo","sareste","saresti","sarete","sarà","sarò","scola","scopo","scorso","se","secondo","seguente","seguito","sei","sembra","sembrare","sembrato","sembrava","sembri","sempre","senza","sette","si","sia","siamo","siano","siate","siete","sig","solito","solo","soltanto","sono","sopra","soprattutto","sotto","spesso","sta","stai","stando","stanno","starai","staranno","starebbe","starebbero","starei","staremmo","staremo","stareste","staresti","starete","starà","starò","stata","state","stati","stato","stava","stavamo","stavano","stavate","stavi","stavo","stemmo","stessa","stesse","stessero","stessi","stessimo","stesso","steste","stesti","stette","stettero","stetti","stia","stiamo","stiano","stiate","sto","su","sua","subito","successivamente","successivo","sue","sugl","sugli","sui","sul","sull","sulla","sulle","sullo","suo","suoi","tale","tali","talvolta","tanto","te","tempo","terzo","th","ti","titolo","tra","tranne","tre","trenta","triplo","troppo","trovato","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","ulteriore","ultimo","un","una","uno","uomo","va","vai","vale","vari","varia","varie","vario","verso","vi","vicino","visto","vita","voi","volta","volte","vostra","vostre","vostri","vostro","è"]
    # spanish stopwords
    # ["0","1","2","3","4","5","6","7","8","9","_","a","actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño","ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla","aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","b","bajo","bastante","bien","breve","buen","buena","buenas","bueno","buenos","c","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos","cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","d","da","dado","dan","dar","de","debajo","debe","deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después","detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","día","días","dónde","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","enfrente","enseguida","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan","estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías","estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese","estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos","estáis","están","estás","esté","estéis","estén","estés","ex","excepto","existe","existen","explicó","expresó","f","fin","final","fue","fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos","fuésemos","g","general","gran","grandes","gueno","h","ha","haber","habia","habida","habidas","habido","habidos","habiendo","habla","hablan","habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais","habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta","hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","horas","hoy","hube","hubiera","hubierais","hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","hubiéramos","hubiésemos","hubo","i","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","j","junto","k","l","la","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","m","mal","manera","manifestó","mas","mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","n","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","p","pais","para","parece","parte","partir","pasada","pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero","primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","q","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién","quiénes","qué","r","raras","realizado","realizar","realizó","repente","respecto","s","sabe","sabeis","sabemos","saben","saber","sabes","sal","salvo","se","sea","seamos","sean","seas","segun","segunda","segundo","según","seis","ser","sera","seremos","será","serán","serás","seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto","sus","suya","suyas","suyo","suyos","sé","sí","sólo","t","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano","tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened","teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos","teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda","todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvieras","tuvieron","tuviese","tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo","tuyos","tú","u","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes","v","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z","él","éramos","ésa","ésas","ése","ésos","ésta","éstas","éste","éstos","última","últimas","último","últimos"]
    # greek stopwords
    # ["ένα","έναν","ένας","αι","ακομα","ακομη","ακριβως","αληθεια","αληθινα","αλλα","αλλαχου","αλλες","αλλη","αλλην","αλλης","αλλιως","αλλιωτικα","αλλο","αλλοι","αλλοιως","αλλοιωτικα","αλλον","αλλος","αλλοτε","αλλου","αλλους","αλλων","αμα","αμεσα","αμεσως","αν","ανα","αναμεσα","αναμεταξυ","ανευ","αντι","αντιπερα","αντις","ανω","ανωτερω","αξαφνα","απ","απεναντι","απο","αποψε","από","αρα","αραγε","αργα","αργοτερο","αριστερα","αρκετα","αρχικα","ας","αυριο","αυτα","αυτες","αυτεσ","αυτη","αυτην","αυτης","αυτο","αυτοι","αυτον","αυτος","αυτοσ","αυτου","αυτους","αυτουσ","αυτων","αφοτου","αφου","αἱ","αἳ","αἵ","αὐτόσ","αὐτὸς","αὖ","α∆ιακοπα","βεβαια","βεβαιοτατα","γάρ","γα","γα^","γε","γι","για","γοῦν","γρηγορα","γυρω","γὰρ","δ'","δέ","δή","δαί","δαίσ","δαὶ","δαὶς","δε","δεν","δι","δι'","διά","δια","διὰ","δὲ","δὴ","δ’","εαν","εαυτο","εαυτον","εαυτου","εαυτους","εαυτων","εγκαιρα","εγκαιρως","εγω","ειθε","ειμαι","ειμαστε","ειναι","εις","εισαι","εισαστε","ειστε","ειτε","ειχα","ειχαμε","ειχαν","ειχατε","ειχε","ειχες","ει∆εμη","εκ","εκαστα","εκαστες","εκαστη","εκαστην","εκαστης","εκαστο","εκαστοι","εκαστον","εκαστος","εκαστου","εκαστους","εκαστων","εκει","εκεινα","εκεινες","εκεινεσ","εκεινη","εκεινην","εκεινης","εκεινο","εκεινοι","εκεινον","εκεινος","εκεινοσ","εκεινου","εκεινους","εκεινουσ","εκεινων","εκτος","εμας","εμεις","εμενα","εμπρος","εν","ενα","εναν","ενας","ενος","εντελως","εντος","εντωμεταξυ","ενω","ενός","εξ","εξαφνα","εξης","εξισου","εξω","επ","επί","επανω","επειτα","επει∆η","επι","επισης","επομενως","εσας","εσεις","εσενα","εστω","εσυ","ετερα","ετεραι","ετερας","ετερες","ετερη","ετερης","ετερο","ετεροι","ετερον","ετερος","ετερου","ετερους","ετερων","ετουτα","ετουτες","ετουτη","ετουτην","ετουτης","ετουτο","ετουτοι","ετουτον","ετουτος","ετουτου","ετουτους","ετουτων","ετσι","ευγε","ευθυς","ευτυχως","εφεξης","εχει","εχεις","εχετε","εχθες","εχομε","εχουμε","εχουν","εχτες","εχω","εως","εἰ","εἰμί","εἰμὶ","εἰς","εἰσ","εἴ","εἴμι","εἴτε","ε∆ω","η","ημασταν","ημαστε","ημουν","ησασταν","ησαστε","ησουν","ηταν","ητανε","ητοι","ηττον","η∆η","θα","ι","ιι","ιιι","ισαμε","ισια","ισως","ισωσ","ι∆ια","ι∆ιαν","ι∆ιας","ι∆ιες","ι∆ιο","ι∆ιοι","ι∆ιον","ι∆ιος","ι∆ιου","ι∆ιους","ι∆ιων","ι∆ιως","κ","καί","καίτοι","καθ","καθε","καθεμια","καθεμιας","καθενα","καθενας","καθενος","καθετι","καθολου","καθως","και","κακα","κακως","καλα","καλως","καμια","καμιαν","καμιας","καμποσα","καμποσες","καμποση","καμποσην","καμποσης","καμποσο","καμποσοι","καμποσον","καμποσος","καμποσου","καμποσους","καμποσων","κανεις","κανεν","κανενα","κανεναν","κανενας","κανενος","καποια","καποιαν","καποιας","καποιες","καποιο","καποιοι","καποιον","καποιος","καποιου","καποιους","καποιων","καποτε","καπου","καπως","κατ","κατά","κατα","κατι","κατιτι","κατοπιν","κατω","κατὰ","καὶ","κι","κιολας","κλπ","κοντα","κτλ","κυριως","κἀν","κἂν","λιγακι","λιγο","λιγωτερο","λογω","λοιπα","λοιπον","μέν","μέσα","μή","μήτε","μία","μα","μαζι","μακαρι","μακρυα","μαλιστα","μαλλον","μας","με","μεθ","μεθαυριο","μειον","μελει","μελλεται","μεμιας","μεν","μερικα","μερικες","μερικοι","μερικους","μερικων","μεσα","μετ","μετά","μετα","μεταξυ","μετὰ","μεχρι","μη","μην","μηπως","μητε","μη∆ε","μιά","μια","μιαν","μιας","μολις","μολονοτι","μοναχα","μονες","μονη","μονην","μονης","μονο","μονοι","μονομιας","μονος","μονου","μονους","μονων","μου","μπορει","μπορουν","μπραβο","μπρος","μἐν","μὲν","μὴ","μὴν","να","ναι","νωρις","ξανα","ξαφνικα","ο","οι","ολα","ολες","ολη","ολην","ολης","ολο","ολογυρα","ολοι","ολον","ολονεν","ολος","ολοτελα","ολου","ολους","ολων","ολως","ολως∆ιολου","ομως","ομωσ","οποια","οποιαν","οποιαν∆ηποτε","οποιας","οποιας∆ηποτε","οποια∆ηποτε","οποιες","οποιες∆ηποτε","οποιο","οποιοι","οποιον","οποιον∆ηποτε","οποιος","οποιος∆ηποτε","οποιου","οποιους","οποιους∆ηποτε","οποιου∆ηποτε","οποιο∆ηποτε","οποιων","οποιων∆ηποτε","οποι∆ηποτε","οποτε","οποτε∆ηποτε","οπου","οπου∆ηποτε","οπως","οπωσ","ορισμενα","ορισμενες","ορισμενων","ορισμενως","οσα","οσα∆ηποτε","οσες","οσες∆ηποτε","οση","οσην","οσην∆ηποτε","οσης","οσης∆ηποτε","οση∆ηποτε","οσο","οσοι","οσοι∆ηποτε","οσον","οσον∆ηποτε","οσος","οσος∆ηποτε","οσου","οσους","οσους∆ηποτε","οσου∆ηποτε","οσο∆ηποτε","οσων","οσων∆ηποτε","οταν","οτι","οτι∆ηποτε","οτου","ου","ουτε","ου∆ε","οχι","οἱ","οἳ","οἷς","οὐ","οὐδ","οὐδέ","οὐδείσ","οὐδεὶς","οὐδὲ","οὐδὲν","οὐκ","οὐχ","οὐχὶ","οὓς","οὔτε","οὕτω","οὕτως","οὕτωσ","οὖν","οὗ","οὗτος","οὗτοσ","παλι","παντοτε","παντου","παντως","παρ","παρά","παρα","παρὰ","περί","περα","περι","περιπου","περισσοτερο","περσι","περυσι","περὶ","πια","πιθανον","πιο","πισω","πλαι","πλεον","πλην","ποια","ποιαν","ποιας","ποιες","ποιεσ","ποιο","ποιοι","ποιον","ποιος","ποιοσ","ποιου","ποιους","ποιουσ","ποιων","πολυ","ποσες","ποση","ποσην","ποσης","ποσοι","ποσος","ποσους","ποτε","που","πουθε","πουθενα","ποῦ","πρεπει","πριν","προ","προκειμενου","προκειται","προπερσι","προς","προσ","προτου","προχθες","προχτες","πρωτυτερα","πρόσ","πρὸ","πρὸς","πως","πωσ","σαν","σας","σε","σεις","σημερα","σιγα","σου","στα","στη","στην","στης","στις","στο","στον","στου","στους","στων","συγχρονως","συν","συναμα","συνεπως","συνηθως","συχνα","συχνας","συχνες","συχνη","συχνην","συχνης","συχνο","συχνοι","συχνον","συχνος","συχνου","συχνους","συχνων","συχνως","σχε∆ον","σωστα","σόσ","σύ","σύν","σὸς","σὺ","σὺν","τά","τήν","τί","τίς","τίσ","τα","ταυτα","ταυτες","ταυτη","ταυτην","ταυτης","ταυτο,ταυτον","ταυτος","ταυτου","ταυτων","ταχα","ταχατε","ταῖς","τα∆ε","τε","τελικα","τελικως","τες","τετοια","τετοιαν","τετοιας","τετοιες","τετοιο","τετοιοι","τετοιον","τετοιος","τετοιου","τετοιους","τετοιων","τη","την","της","τησ","τι","τινα","τιποτα","τιποτε","τις","τισ","το","τοί","τοι","τοιοῦτος","τοιοῦτοσ","τον","τος","τοσα","τοσες","τοση","τοσην","τοσης","τοσο","τοσοι","τοσον","τοσος","τοσου","τοσους","τοσων","τοτε","του","τουλαχιστο","τουλαχιστον","τους","τουτα","τουτες","τουτη","τουτην","τουτης","τουτο","τουτοι","τουτοις","τουτον","τουτος","τουτου","τουτους","τουτων","τούσ","τοὺς","τοῖς","τοῦ","τυχον","των","τωρα","τό","τόν","τότε","τὰ","τὰς","τὴν","τὸ","τὸν","τῆς","τῆσ","τῇ","τῶν","τῷ","υπ","υπερ","υπο","υποψη","υποψιν","υπό","υστερα","φετος","χαμηλα","χθες","χτες","χωρις","χωριστα","ψηλα","ω","ωραια","ως","ωσ","ωσαν","ωσοτου","ωσπου","ωστε","ωστοσο","ωχ","ἀλλ'","ἀλλά","ἀλλὰ","ἀλλ’","ἀπ","ἀπό","ἀπὸ","ἀφ","ἂν","ἃ","ἄλλος","ἄλλοσ","ἄν","ἄρα","ἅμα","ἐάν","ἐγώ","ἐγὼ","ἐκ","ἐμόσ","ἐμὸς","ἐν","ἐξ","ἐπί","ἐπεὶ","ἐπὶ","ἐστι","ἐφ","ἐὰν","ἑαυτοῦ","ἔτι","ἡ","ἢ","ἣ","ἤ","ἥ","ἧς","ἵνα","ὁ","ὃ","ὃν","ὃς","ὅ","ὅδε","ὅθεν","ὅπερ","ὅς","ὅσ","ὅστις","ὅστισ","ὅτε","ὅτι","ὑμόσ","ὑπ","ὑπέρ","ὑπό","ὑπὲρ","ὑπὸ","ὡς","ὡσ","ὥς","ὥστε","ὦ","ᾧ","∆α","∆ε","∆εινα","∆εν","∆εξια","∆ηθεν","∆ηλα∆η","∆ι","∆ια","∆ιαρκως","∆ικα","∆ικο","∆ικοι","∆ικος","∆ικου","∆ικους","∆ιολου","∆ιπλα","∆ιχως"]

    count_vectorizer = CountVectorizer(stop_words='english')    # Fit and transform the processed titles
    count_data = count_vectorizer.fit_transform(corpus)         # Visualise the 10 most common words
    plot_common_words(count_data, count_vectorizer)

    # import warnings
    # warnings.simplefilter("ignore", DeprecationWarning)  # Load the LDA model from sk-learn
    number_topics = 3
    number_words = 10  # Create and fit the LDA model
    lda = LDA(n_components=number_topics) #, n_jobs=-1)
    lda.fit(count_data)  # Print the topics found by the LDA model
    print("Topics found via LDA:")
    print_topics(lda, count_vectorizer, number_words)

    print('')

# a combined method (tfid + lda) is deployed for topic modeling. detected topics and most common
# terns are printed.
def topic_modeling(corpus, language):

    print('* topic modeling')
    print (language)

    if language == 'en':
        stop_words = 'english'
    elif language == 'es':
        stop_words = ["0","1","2","3","4","5","6","7","8","9","_","a","actualmente","acuerdo","adelante","ademas","además","adrede","afirmó","agregó","ahi","ahora","ahí","al","algo","alguna","algunas","alguno","algunos","algún","alli","allí","alrededor","ambos","ampleamos","antano","antaño","ante","anterior","antes","apenas","aproximadamente","aquel","aquella","aquellas","aquello","aquellos","aqui","aquél","aquélla","aquéllas","aquéllos","aquí","arriba","arribaabajo","aseguró","asi","así","atras","aun","aunque","ayer","añadió","aún","b","bajo","bastante","bien","breve","buen","buena","buenas","bueno","buenos","c","cada","casi","cerca","cierta","ciertas","cierto","ciertos","cinco","claro","comentó","como","con","conmigo","conocer","conseguimos","conseguir","considera","consideró","consigo","consigue","consiguen","consigues","contigo","contra","cosas","creo","cual","cuales","cualquier","cuando","cuanta","cuantas","cuanto","cuantos","cuatro","cuenta","cuál","cuáles","cuándo","cuánta","cuántas","cuánto","cuántos","cómo","d","da","dado","dan","dar","de","debajo","debe","deben","debido","decir","dejó","del","delante","demasiado","demás","dentro","deprisa","desde","despacio","despues","después","detras","detrás","dia","dias","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","donde","dos","durante","día","días","dónde","e","ejemplo","el","ella","ellas","ello","ellos","embargo","empleais","emplean","emplear","empleas","empleo","en","encima","encuentra","enfrente","enseguida","entonces","entre","era","erais","eramos","eran","eras","eres","es","esa","esas","ese","eso","esos","esta","estaba","estabais","estaban","estabas","estad","estada","estadas","estado","estados","estais","estamos","estan","estando","estar","estaremos","estará","estarán","estarás","estaré","estaréis","estaría","estaríais","estaríamos","estarían","estarías","estas","este","estemos","esto","estos","estoy","estuve","estuviera","estuvierais","estuvieran","estuvieras","estuvieron","estuviese","estuvieseis","estuviesen","estuvieses","estuvimos","estuviste","estuvisteis","estuviéramos","estuviésemos","estuvo","está","estábamos","estáis","están","estás","esté","estéis","estén","estés","ex","excepto","existe","existen","explicó","expresó","f","fin","final","fue","fuera","fuerais","fueran","fueras","fueron","fuese","fueseis","fuesen","fueses","fui","fuimos","fuiste","fuisteis","fuéramos","fuésemos","g","general","gran","grandes","gueno","h","ha","haber","habia","habida","habidas","habido","habidos","habiendo","habla","hablan","habremos","habrá","habrán","habrás","habré","habréis","habría","habríais","habríamos","habrían","habrías","habéis","había","habíais","habíamos","habían","habías","hace","haceis","hacemos","hacen","hacer","hacerlo","haces","hacia","haciendo","hago","han","has","hasta","hay","haya","hayamos","hayan","hayas","hayáis","he","hecho","hemos","hicieron","hizo","horas","hoy","hube","hubiera","hubierais","hubieran","hubieras","hubieron","hubiese","hubieseis","hubiesen","hubieses","hubimos","hubiste","hubisteis","hubiéramos","hubiésemos","hubo","i","igual","incluso","indicó","informo","informó","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","j","junto","k","l","la","lado","largo","las","le","lejos","les","llegó","lleva","llevar","lo","los","luego","lugar","m","mal","manera","manifestó","mas","mayor","me","mediante","medio","mejor","mencionó","menos","menudo","mi","mia","mias","mientras","mio","mios","mis","misma","mismas","mismo","mismos","modo","momento","mucha","muchas","mucho","muchos","muy","más","mí","mía","mías","mío","míos","n","nada","nadie","ni","ninguna","ningunas","ninguno","ningunos","ningún","no","nos","nosotras","nosotros","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","os","otra","otras","otro","otros","p","pais","para","parece","parte","partir","pasada","pasado","paìs","peor","pero","pesar","poca","pocas","poco","pocos","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","podrá","podrán","podría","podrían","poner","por","por qué","porque","posible","primer","primera","primero","primeros","principalmente","pronto","propia","propias","propio","propios","proximo","próximo","próximos","pudo","pueda","puede","pueden","puedo","pues","q","qeu","que","quedó","queremos","quien","quienes","quiere","quiza","quizas","quizá","quizás","quién","quiénes","qué","r","raras","realizado","realizar","realizó","repente","respecto","s","sabe","sabeis","sabemos","saben","saber","sabes","sal","salvo","se","sea","seamos","sean","seas","segun","segunda","segundo","según","seis","ser","sera","seremos","será","serán","serás","seré","seréis","sería","seríais","seríamos","serían","serías","seáis","señaló","si","sido","siempre","siendo","siete","sigue","siguiente","sin","sino","sobre","sois","sola","solamente","solas","solo","solos","somos","son","soy","soyos","su","supuesto","sus","suya","suyas","suyo","suyos","sé","sí","sólo","t","tal","tambien","también","tampoco","tan","tanto","tarde","te","temprano","tendremos","tendrá","tendrán","tendrás","tendré","tendréis","tendría","tendríais","tendríamos","tendrían","tendrías","tened","teneis","tenemos","tener","tenga","tengamos","tengan","tengas","tengo","tengáis","tenida","tenidas","tenido","tenidos","teniendo","tenéis","tenía","teníais","teníamos","tenían","tenías","tercera","ti","tiempo","tiene","tienen","tienes","toda","todas","todavia","todavía","todo","todos","total","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","trata","través","tres","tu","tus","tuve","tuviera","tuvierais","tuvieran","tuvieras","tuvieron","tuviese","tuvieseis","tuviesen","tuvieses","tuvimos","tuviste","tuvisteis","tuviéramos","tuviésemos","tuvo","tuya","tuyas","tuyo","tuyos","tú","u","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","usted","ustedes","v","va","vais","valor","vamos","van","varias","varios","vaya","veces","ver","verdad","verdadera","verdadero","vez","vosotras","vosotros","voy","vuestra","vuestras","vuestro","vuestros","w","x","y","ya","yo","z","él","éramos","ésa","ésas","ése","ésos","ésta","éstas","éste","éstos","última","últimas","último","últimos"]
    elif language == 'it':
        stop_words = ["a","abbastanza","abbia","abbiamo","abbiano","abbiate","accidenti","ad","adesso","affinché","agl","agli","ahime","ahimè","ai","al","alcuna","alcuni","alcuno","all","alla","alle","allo","allora","altre","altri","altrimenti","altro","altrove","altrui","anche","ancora","anni","anno","ansa","anticipo","assai","attesa","attraverso","avanti","avemmo","avendo","avente","aver","avere","averlo","avesse","avessero","avessi","avessimo","aveste","avesti","avete","aveva","avevamo","avevano","avevate","avevi","avevo","avrai","avranno","avrebbe","avrebbero","avrei","avremmo","avremo","avreste","avresti","avrete","avrà","avrò","avuta","avute","avuti","avuto","basta","ben","bene","benissimo","brava","bravo","buono","c","caso","cento","certa","certe","certi","certo","che","chi","chicchessia","chiunque","ci","ciascuna","ciascuno","cima","cinque","cio","cioe","cioè","circa","citta","città","ciò","co","codesta","codesti","codesto","cogli","coi","col","colei","coll","coloro","colui","come","cominci","comprare","comunque","con","concernente","conclusione","consecutivi","consecutivo","consiglio","contro","cortesia","cos","cosa","cosi","così","cui","d","da","dagl","dagli","dai","dal","dall","dalla","dalle","dallo","dappertutto","davanti","degl","degli","dei","del","dell","della","delle","dello","dentro","detto","deve","devo","di","dice","dietro","dire","dirimpetto","diventa","diventare","diventato","dopo","doppio","dov","dove","dovra","dovrà","dovunque","due","dunque","durante","e","ebbe","ebbero","ebbi","ecc","ecco","ed","effettivamente","egli","ella","entrambi","eppure","era","erano","eravamo","eravate","eri","ero","esempio","esse","essendo","esser","essere","essi","ex","fa","faccia","facciamo","facciano","facciate","faccio","facemmo","facendo","facesse","facessero","facessi","facessimo","faceste","facesti","faceva","facevamo","facevano","facevate","facevi","facevo","fai","fanno","farai","faranno","fare","farebbe","farebbero","farei","faremmo","faremo","fareste","faresti","farete","farà","farò","fatto","favore","fece","fecero","feci","fin","finalmente","finche","fine","fino","forse","forza","fosse","fossero","fossi","fossimo","foste","fosti","fra","frattempo","fu","fui","fummo","fuori","furono","futuro","generale","gente","gia","giacche","giorni","giorno","giu","già","gli","gliela","gliele","glieli","glielo","gliene","grande","grazie","gruppo","ha","haha","hai","hanno","ho","i","ie","ieri","il","improvviso","in","inc","indietro","infatti","inoltre","insieme","intanto","intorno","invece","io","l","la","lasciato","lato","le","lei","li","lo","lontano","loro","lui","lungo","luogo","là","ma","macche","magari","maggior","mai","male","malgrado","malissimo","me","medesimo","mediante","meglio","meno","mentre","mesi","mezzo","mi","mia","mie","miei","mila","miliardi","milioni","minimi","mio","modo","molta","molti","moltissimo","molto","momento","mondo","ne","negl","negli","nei","nel","nell","nella","nelle","nello","nemmeno","neppure","nessun","nessuna","nessuno","niente","no","noi","nome","non","nondimeno","nonostante","nonsia","nostra","nostre","nostri","nostro","novanta","nove","nulla","nuovi","nuovo","o","od","oggi","ogni","ognuna","ognuno","oltre","oppure","ora","ore","osi","ossia","ottanta","otto","paese","parecchi","parecchie","parecchio","parte","partendo","peccato","peggio","per","perche","perchè","perché","percio","perciò","perfino","pero","persino","persone","però","piedi","pieno","piglia","piu","piuttosto","più","po","pochissimo","poco","poi","poiche","possa","possedere","posteriore","posto","potrebbe","preferibilmente","presa","press","prima","primo","principalmente","probabilmente","promesso","proprio","puo","pure","purtroppo","può","qua","qualche","qualcosa","qualcuna","qualcuno","quale","quali","qualunque","quando","quanta","quante","quanti","quanto","quantunque","quarto","quasi","quattro","quel","quella","quelle","quelli","quello","quest","questa","queste","questi","questo","qui","quindi","quinto","realmente","recente","recentemente","registrazione","relativo","riecco","rispetto","salvo","sara","sarai","saranno","sarebbe","sarebbero","sarei","saremmo","saremo","sareste","saresti","sarete","sarà","sarò","scola","scopo","scorso","se","secondo","seguente","seguito","sei","sembra","sembrare","sembrato","sembrava","sembri","sempre","senza","sette","si","sia","siamo","siano","siate","siete","sig","solito","solo","soltanto","sono","sopra","soprattutto","sotto","spesso","sta","stai","stando","stanno","starai","staranno","starebbe","starebbero","starei","staremmo","staremo","stareste","staresti","starete","starà","starò","stata","state","stati","stato","stava","stavamo","stavano","stavate","stavi","stavo","stemmo","stessa","stesse","stessero","stessi","stessimo","stesso","steste","stesti","stette","stettero","stetti","stia","stiamo","stiano","stiate","sto","su","sua","subito","successivamente","successivo","sue","sugl","sugli","sui","sul","sull","sulla","sulle","sullo","suo","suoi","tale","tali","talvolta","tanto","te","tempo","terzo","th","ti","titolo","tra","tranne","tre","trenta","triplo","troppo","trovato","tu","tua","tue","tuo","tuoi","tutta","tuttavia","tutte","tutti","tutto","uguali","ulteriore","ultimo","un","una","uno","uomo","va","vai","vale","vari","varia","varie","vario","verso","vi","vicino","visto","vita","voi","volta","volte","vostra","vostre","vostri","vostro","è"]
    elif language == 'el':
        stop_words = ["ένα","έναν","ένας","αι","ακομα","ακομη","ακριβως","αληθεια","αληθινα","αλλα","αλλαχου","αλλες","αλλη","αλλην","αλλης","αλλιως","αλλιωτικα","αλλο","αλλοι","αλλοιως","αλλοιωτικα","αλλον","αλλος","αλλοτε","αλλου","αλλους","αλλων","αμα","αμεσα","αμεσως","αν","ανα","αναμεσα","αναμεταξυ","ανευ","αντι","αντιπερα","αντις","ανω","ανωτερω","αξαφνα","απ","απεναντι","απο","αποψε","από","αρα","αραγε","αργα","αργοτερο","αριστερα","αρκετα","αρχικα","ας","αυριο","αυτα","αυτες","αυτεσ","αυτη","αυτην","αυτης","αυτο","αυτοι","αυτον","αυτος","αυτοσ","αυτου","αυτους","αυτουσ","αυτων","αφοτου","αφου","αἱ","αἳ","αἵ","αὐτόσ","αὐτὸς","αὖ","α∆ιακοπα","βεβαια","βεβαιοτατα","γάρ","γα","γα^","γε","γι","για","γοῦν","γρηγορα","γυρω","γὰρ","δ'","δέ","δή","δαί","δαίσ","δαὶ","δαὶς","δε","δεν","δι","δι'","διά","δια","διὰ","δὲ","δὴ","δ’","εαν","εαυτο","εαυτον","εαυτου","εαυτους","εαυτων","εγκαιρα","εγκαιρως","εγω","ειθε","ειμαι","ειμαστε","ειναι","εις","εισαι","εισαστε","ειστε","ειτε","ειχα","ειχαμε","ειχαν","ειχατε","ειχε","ειχες","ει∆εμη","εκ","εκαστα","εκαστες","εκαστη","εκαστην","εκαστης","εκαστο","εκαστοι","εκαστον","εκαστος","εκαστου","εκαστους","εκαστων","εκει","εκεινα","εκεινες","εκεινεσ","εκεινη","εκεινην","εκεινης","εκεινο","εκεινοι","εκεινον","εκεινος","εκεινοσ","εκεινου","εκεινους","εκεινουσ","εκεινων","εκτος","εμας","εμεις","εμενα","εμπρος","εν","ενα","εναν","ενας","ενος","εντελως","εντος","εντωμεταξυ","ενω","ενός","εξ","εξαφνα","εξης","εξισου","εξω","επ","επί","επανω","επειτα","επει∆η","επι","επισης","επομενως","εσας","εσεις","εσενα","εστω","εσυ","ετερα","ετεραι","ετερας","ετερες","ετερη","ετερης","ετερο","ετεροι","ετερον","ετερος","ετερου","ετερους","ετερων","ετουτα","ετουτες","ετουτη","ετουτην","ετουτης","ετουτο","ετουτοι","ετουτον","ετουτος","ετουτου","ετουτους","ετουτων","ετσι","ευγε","ευθυς","ευτυχως","εφεξης","εχει","εχεις","εχετε","εχθες","εχομε","εχουμε","εχουν","εχτες","εχω","εως","εἰ","εἰμί","εἰμὶ","εἰς","εἰσ","εἴ","εἴμι","εἴτε","ε∆ω","η","ημασταν","ημαστε","ημουν","ησασταν","ησαστε","ησουν","ηταν","ητανε","ητοι","ηττον","η∆η","θα","ι","ιι","ιιι","ισαμε","ισια","ισως","ισωσ","ι∆ια","ι∆ιαν","ι∆ιας","ι∆ιες","ι∆ιο","ι∆ιοι","ι∆ιον","ι∆ιος","ι∆ιου","ι∆ιους","ι∆ιων","ι∆ιως","κ","καί","καίτοι","καθ","καθε","καθεμια","καθεμιας","καθενα","καθενας","καθενος","καθετι","καθολου","καθως","και","κακα","κακως","καλα","καλως","καμια","καμιαν","καμιας","καμποσα","καμποσες","καμποση","καμποσην","καμποσης","καμποσο","καμποσοι","καμποσον","καμποσος","καμποσου","καμποσους","καμποσων","κανεις","κανεν","κανενα","κανεναν","κανενας","κανενος","καποια","καποιαν","καποιας","καποιες","καποιο","καποιοι","καποιον","καποιος","καποιου","καποιους","καποιων","καποτε","καπου","καπως","κατ","κατά","κατα","κατι","κατιτι","κατοπιν","κατω","κατὰ","καὶ","κι","κιολας","κλπ","κοντα","κτλ","κυριως","κἀν","κἂν","λιγακι","λιγο","λιγωτερο","λογω","λοιπα","λοιπον","μέν","μέσα","μή","μήτε","μία","μα","μαζι","μακαρι","μακρυα","μαλιστα","μαλλον","μας","με","μεθ","μεθαυριο","μειον","μελει","μελλεται","μεμιας","μεν","μερικα","μερικες","μερικοι","μερικους","μερικων","μεσα","μετ","μετά","μετα","μεταξυ","μετὰ","μεχρι","μη","μην","μηπως","μητε","μη∆ε","μιά","μια","μιαν","μιας","μολις","μολονοτι","μοναχα","μονες","μονη","μονην","μονης","μονο","μονοι","μονομιας","μονος","μονου","μονους","μονων","μου","μπορει","μπορουν","μπραβο","μπρος","μἐν","μὲν","μὴ","μὴν","να","ναι","νωρις","ξανα","ξαφνικα","ο","οι","ολα","ολες","ολη","ολην","ολης","ολο","ολογυρα","ολοι","ολον","ολονεν","ολος","ολοτελα","ολου","ολους","ολων","ολως","ολως∆ιολου","ομως","ομωσ","οποια","οποιαν","οποιαν∆ηποτε","οποιας","οποιας∆ηποτε","οποια∆ηποτε","οποιες","οποιες∆ηποτε","οποιο","οποιοι","οποιον","οποιον∆ηποτε","οποιος","οποιος∆ηποτε","οποιου","οποιους","οποιους∆ηποτε","οποιου∆ηποτε","οποιο∆ηποτε","οποιων","οποιων∆ηποτε","οποι∆ηποτε","οποτε","οποτε∆ηποτε","οπου","οπου∆ηποτε","οπως","οπωσ","ορισμενα","ορισμενες","ορισμενων","ορισμενως","οσα","οσα∆ηποτε","οσες","οσες∆ηποτε","οση","οσην","οσην∆ηποτε","οσης","οσης∆ηποτε","οση∆ηποτε","οσο","οσοι","οσοι∆ηποτε","οσον","οσον∆ηποτε","οσος","οσος∆ηποτε","οσου","οσους","οσους∆ηποτε","οσου∆ηποτε","οσο∆ηποτε","οσων","οσων∆ηποτε","οταν","οτι","οτι∆ηποτε","οτου","ου","ουτε","ου∆ε","οχι","οἱ","οἳ","οἷς","οὐ","οὐδ","οὐδέ","οὐδείσ","οὐδεὶς","οὐδὲ","οὐδὲν","οὐκ","οὐχ","οὐχὶ","οὓς","οὔτε","οὕτω","οὕτως","οὕτωσ","οὖν","οὗ","οὗτος","οὗτοσ","παλι","παντοτε","παντου","παντως","παρ","παρά","παρα","παρὰ","περί","περα","περι","περιπου","περισσοτερο","περσι","περυσι","περὶ","πια","πιθανον","πιο","πισω","πλαι","πλεον","πλην","ποια","ποιαν","ποιας","ποιες","ποιεσ","ποιο","ποιοι","ποιον","ποιος","ποιοσ","ποιου","ποιους","ποιουσ","ποιων","πολυ","ποσες","ποση","ποσην","ποσης","ποσοι","ποσος","ποσους","ποτε","που","πουθε","πουθενα","ποῦ","πρεπει","πριν","προ","προκειμενου","προκειται","προπερσι","προς","προσ","προτου","προχθες","προχτες","πρωτυτερα","πρόσ","πρὸ","πρὸς","πως","πωσ","σαν","σας","σε","σεις","σημερα","σιγα","σου","στα","στη","στην","στης","στις","στο","στον","στου","στους","στων","συγχρονως","συν","συναμα","συνεπως","συνηθως","συχνα","συχνας","συχνες","συχνη","συχνην","συχνης","συχνο","συχνοι","συχνον","συχνος","συχνου","συχνους","συχνων","συχνως","σχε∆ον","σωστα","σόσ","σύ","σύν","σὸς","σὺ","σὺν","τά","τήν","τί","τίς","τίσ","τα","ταυτα","ταυτες","ταυτη","ταυτην","ταυτης","ταυτο,ταυτον","ταυτος","ταυτου","ταυτων","ταχα","ταχατε","ταῖς","τα∆ε","τε","τελικα","τελικως","τες","τετοια","τετοιαν","τετοιας","τετοιες","τετοιο","τετοιοι","τετοιον","τετοιος","τετοιου","τετοιους","τετοιων","τη","την","της","τησ","τι","τινα","τιποτα","τιποτε","τις","τισ","το","τοί","τοι","τοιοῦτος","τοιοῦτοσ","τον","τος","τοσα","τοσες","τοση","τοσην","τοσης","τοσο","τοσοι","τοσον","τοσος","τοσου","τοσους","τοσων","τοτε","του","τουλαχιστο","τουλαχιστον","τους","τουτα","τουτες","τουτη","τουτην","τουτης","τουτο","τουτοι","τουτοις","τουτον","τουτος","τουτου","τουτους","τουτων","τούσ","τοὺς","τοῖς","τοῦ","τυχον","των","τωρα","τό","τόν","τότε","τὰ","τὰς","τὴν","τὸ","τὸν","τῆς","τῆσ","τῇ","τῶν","τῷ","υπ","υπερ","υπο","υποψη","υποψιν","υπό","υστερα","φετος","χαμηλα","χθες","χτες","χωρις","χωριστα","ψηλα","ω","ωραια","ως","ωσ","ωσαν","ωσοτου","ωσπου","ωστε","ωστοσο","ωχ","ἀλλ'","ἀλλά","ἀλλὰ","ἀλλ’","ἀπ","ἀπό","ἀπὸ","ἀφ","ἂν","ἃ","ἄλλος","ἄλλοσ","ἄν","ἄρα","ἅμα","ἐάν","ἐγώ","ἐγὼ","ἐκ","ἐμόσ","ἐμὸς","ἐν","ἐξ","ἐπί","ἐπεὶ","ἐπὶ","ἐστι","ἐφ","ἐὰν","ἑαυτοῦ","ἔτι","ἡ","ἢ","ἣ","ἤ","ἥ","ἧς","ἵνα","ὁ","ὃ","ὃν","ὃς","ὅ","ὅδε","ὅθεν","ὅπερ","ὅς","ὅσ","ὅστις","ὅστισ","ὅτε","ὅτι","ὑμόσ","ὑπ","ὑπέρ","ὑπό","ὑπὲρ","ὑπὸ","ὡς","ὡσ","ὥς","ὥστε","ὦ","ᾧ","∆α","∆ε","∆εινα","∆εν","∆εξια","∆ηθεν","∆ηλα∆η","∆ι","∆ια","∆ιαρκως","∆ικα","∆ικο","∆ικοι","∆ικος","∆ικου","∆ικους","∆ιολου","∆ιπλα","∆ιχως"]

    no_features = 1000

    # TFidVectorizer for NMF
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stop_words)
    tfidf = tfidf_vectorizer.fit_transform(corpus)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()

    # count vectorizer for LDA
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words=stop_words)
    tf = tf_vectorizer.fit_transform(corpus)
    tf_feature_names = tf_vectorizer.get_feature_names()

    plot_common_words(tf, tf_vectorizer)
    plot_common_words(tfidf, tfidf_vectorizer)
    no_topics = 5

    # Run NMF
    nmf = NMF(n_components=no_topics, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf)


    # Run LDA
    lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,
                                    random_state=0).fit(tf)

    def display_topics(model, feature_names, no_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print ("Topic %d:" % (topic_idx))
            print (" ".join([feature_names[i]
                      for i in topic.argsort()[:-no_top_words - 1:-1]]))

    no_top_words = 10
    print("Detected topics from NMF analysis:")
    display_topics(nmf, tfidf_feature_names, no_top_words)
    print("Detected topics from LDA analysis:")
    display_topics(lda, tf_feature_names, no_top_words)


''' HELPER METHODS '''
# a helper method for topic modeling methods to list the detected topics
def print_topics(model, count_vectorizer, n_top_words):
    words = count_vectorizer.get_feature_names()
    for topic_idx, topic in enumerate(model.components_):
        print("\nTopic #%d:" % topic_idx)
        print(" ".join([words[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))

# a helper method for topic modeling methods to plot most common words
def plot_common_words(count_data, count_vectorizer):

    sns.set_style('whitegrid')

    words = count_vectorizer.get_feature_names()
    total_counts = np.zeros(len(words))
    for t in count_data:
        total_counts += t.toarray()[0]

    count_dict = (zip(words, total_counts))
    count_dict = sorted(count_dict, key=lambda x: x[1], reverse=True)[0:50]
    words = [w[0] for w in count_dict]
    counts = [w[1] for w in count_dict]
    x_pos = np.arange(len(words))

    plt.figure(2, figsize=(15, 15 / 1.6180))
    plt.subplot(title='10 most common words')
    sns.set_context("notebook", font_scale=1.25, rc={"lines.linewidth": 2.5})
    sns.barplot(x_pos, counts, palette='husl')
    plt.xticks(x_pos, words, rotation=90)
    plt.xlabel('words')
    plt.ylabel('counts')
    plt.show()  # Initialise the count vectorizer with the English stop words


''' SUPPLEMENTARY METHODS '''
# a method primarily for testing various workflows and techniques. it is
# mostly based on the spacy library for executiong common nlp tasks.
def analyze_syntax(text):

    print('Syntax analysis')

    print(' ')
    word = TextBlob(text)
    lang = word.detect_language()
    print('The language is:', lang)

    if lang == 'el':    nlp = spacy.load('el_core_news_sm')
    elif lang == 'es':  nlp = spacy.load('es_core_news_sm')
    elif lang == 'it':  nlp = spacy.load('it_core_news_sm')
    else:               nlp = spacy.load('en_core_web_sm')
    nlp_text = nlp(text)

    # Extract sentences
    sentences = list(nlp_text.sents)
    print(' ')
    print('Sentences:', len(sentences))
    for sentence in sentences:
        #
        print('#', sentence)

    # Extract tokens
    print(' ')
    print('Tokens:', len(nlp_text))
    print('Lemma | Root | POS | Position | Shape | Alphabetic? | Stop? ')
    for token in nlp_text:
        print('#', token.text, token.lemma_, token.pos_, token.dep_, token.shape_, token.is_alpha, token.is_stop)
        #     spacy.explain(token.tag_)token.tag_

    # Noun chunks
    print(' ')
    print('Noun chunks analysis')
    print('Chunk | Root | POS | Head ')
    for chunk in nlp_text.noun_chunks:
        print('#', chunk.text, ' | ', chunk.root.text, ' | ', chunk.root.dep_, ' | ', chunk.root.head.text)

    print(' ')
    print(' ')

# a skeleton method for implementing hate speech detection. it is deprecated
# and kept here for retrieving algorithms/techinques that have not embedded in
# the deployed hate speech methods but may be used in the future.
def detect_hate_alt(data_path):

    file = open(data_path, 'r', encoding='utf-8')
    data = file.read().splitlines()
    file.close()

    counter = 0
    for datum in data:

        # load text
        try:
            datum = json.loads(datum)['text']
            counter += 1
        except:
            print('JSON error')
            continue

        # analyze text
        lang = Translator().detect(datum[:100]).lang
        print('{}. {}'.format(counter, datum[:100]))
        print('The language is: {}'.format(lang))
        if lang == 'el':    nlp = spacy.load('el_core_news_sm')
        elif lang == 'es':  nlp = spacy.load('es_core_news_sm')
        elif lang == 'it':  nlp = spacy.load('it_core_news_sm')
        elif lang == 'en':  nlp = spacy.load('en_core_web_sm')
        else:               continue

        # load dictionary
        file = open('Dictionaries\\dictionary_' + lang + '.txt', 'r', encoding='utf-8')
        terms = file.read().splitlines()
        file.close()

        # token matcher
        # matcher = Matcher(nlp.vocab)
        # pattern = [{"LOWER": "κάνει μήνυση"}, {"IS_PUNCT": True}]
        # matcher.add("HelloWorld", None, pattern)

        # phrase matcher
        terms = ["Ερντογάν", "μήνυση", "μΗνες"]
        for i in range(len(terms)):
            for token in nlp(terms[i]):
                terms[i] = utils.clean_accent(token.lemma_.lower())
        print(terms)
        # sys.exit()

        matcher = PhraseMatcher(nlp.vocab)
        patterns = [nlp.make_doc(text) for text in terms]
        matcher.add("TerminologyList", None, *patterns)

        datum_t = ''
        for token in nlp(datum):
            datum_t += utils.clean_accent(token.lemma_.lower()) + ' '
        print(datum_t)
        doc = nlp(datum_t)

        matches = matcher(doc)
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)

        # html = displacy.render(doc, style="ent", page=True, options={"ents": ["EVENT"]})

        # print(terms_t)
        # print(datum_t)
        time.sleep(3)

# a pilot method for executing sentiment analysis. it will be used as the base
# for the upcoming sentiment analysis methods.
def estimate_sentiment():
    nlp = English()  # We only want the tokenizer, so no need to load a model
    matcher = Matcher(nlp.vocab)

    pos_emoji = ["😀", "😃", "😂", "🤣", "😊", "😍"]  # Positive emoji
    neg_emoji = ["😞", "😠", "😩", "😢", "😭", "😒"]  # Negative emoji

    # Add patterns to match one or more emoji tokens
    pos_patterns = [[{"ORTH": emoji}] for emoji in pos_emoji]
    neg_patterns = [[{"ORTH": emoji}] for emoji in neg_emoji]

    # Function to label the sentiment
    def label_sentiment(matcher, doc, i, matches):
        match_id, start, end = matches[i]
        if doc.vocab.strings[match_id] == "HAPPY":  # Don't forget to get string!
            doc.sentiment += 0.1  # Add 0.1 for positive sentiment
        elif doc.vocab.strings[match_id] == "SAD":
            doc.sentiment -= 0.1  # Subtract 0.1 for negative sentiment

    matcher.add("HAPPY", label_sentiment, *pos_patterns)  # Add positive pattern
    matcher.add("SAD", label_sentiment, *neg_patterns)  # Add negative pattern

    # Add pattern for valid hashtag, i.e. '#' plus any ASCII token
    matcher.add("HASHTAG", None, [{"ORTH": "#"}, {"IS_ASCII": True}])

    doc = nlp("Hello world 😀 #MondayMotivation")
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = doc.vocab.strings[match_id]  # Look up string ID
        span = doc[start:end]
        print(string_id, span.text)
