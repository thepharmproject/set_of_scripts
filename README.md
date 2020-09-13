# Project Description
Set of scripts of algorithms - The algorithm’s scripts will be made available in Github so they can be shared with the rest of the team, but also with external stakeholders. The URL of the scripts in Github will allow its evaluation by testing if all scripts can be run with the corresponding expected result (download of contents from different digital and social media, automated classification, etc.). 

## Sources Selection

* semi structured
- 22 spanish websites
12 italian websites
16 greek websites

twitter api
youtube api

single facebook groups & pages
single youtube videos

*unstructured 
any website

•	A spreadsheet in Google Docs (https://bit.ly/3jaWzEq) for adding sources of in-terest have been deployed. Each sheet refers to a country (i.e. International, Spanish, Greek, Italian).
•	Platforms that include relevant content (i.e. Twitter, YouTube) can be added and, if applicable, a specific source/channel for each type of platform. For exam-ple, there is no need to specify a source/user in Twitter, as the collection is ex-ecuted arbitrarily based on a keyword list (this will be discussed in the future).
•	An additional column (Notes) for adding our comments/notes on each entry is present, to discuss any difficulties/problems that may arise (e.g. some websites mostly have audiovisual content and very little text, or there is absence of comments).
•	An additional column with feedback, denoting also the current site's gathering status is also specified. If an "OK" note is present, then the scraper is already ca-pable of gathering data for the specific site.
•	As for the websites, much effort was put on scraping "difficult" websites (i.e., when JavaScript is used for article/comments loading). The implementation of a scraper has to be tuned for each website independently. This adaptive "scraping configuration" is generally a time-consuming process. Hence, if you want to add new entries to the online spreadsheet, precise/targeted additions are recom-mended. If comments are vital for our analysis, consider leaving out websites without/or will rare commenting. If a website is more probable to contain hate speech content, give it a higher priority than others.
Progress
•	The list is a preliminary attempt to review the most important/popular sources for each region/language, so as to examine/evaluate the technical needs/difficulties for developing data scraping algorithms for each individual website/platform. It is probable that some entries will not be includ-ed/implemented, so consider adding the most representa-tive/popular/interesting sources at this step.

## Scraping & Data Collection

### Approach
A method for detecting geolocation from text. Much emphasis was given in data gathering and formulation, as we think this is a prerequisite for seamlessly moving on the other tasks.A draft/prototype JSON-like data format with a simplified description scheme (source, title, text, metadata) has been formed, towards a unified description scheme for all sources (with an NoSQL approach, as the proposal specifies). This format is being used for storing content from websites (articles and comments), tweets and YouTube comments (for the case of twitter the description scheme is more complex). As for the websites, much effort was put on scraping "difficult" websites (i.e., when JavaScript is used for article/comments loading). All implementations have been refined to be more robust, accurate, providing data fully compatible with the doccano platform. Data format is compatible with the doccano platform. 

### Implementation
The aforementioned approach is coded in couple of python files. In specific scraper_twitter.py, scraper_web.py, scraper_youtube.py, single_facebook.py, single_web.py and single_youtube.py files implement the necessary routines for collecting text content from the web.

#### Twitter tweets via Twitter API
The project supports text collection from the twitter via the appropriate API and the stream method. Tweepy library for accessing the Twitter API is used. Four dictionaries for filtering tweets have been developed including greek, english, spanish and italian keywords. These can been found in the "Keywords" directory. Results are stored to the "Data/scraper_twitter_data.json" file.

#### YouTube comments via Google API
YouTube comment collection is also supoorted via the Google API. Please set keywords for searching content, e.g. "migration refugees". Results are stored to the "Data/scraper_youtube_data.json" file.

#### Posts and Replies from any open Facebook groups or page
The selenium package is used to automate web browser interaction from Python. Results are stored to the "Data/single_web_data.json" file.

#### Comments from any YouTube video
The selenium package is used to automate web browser interaction from Python.

#### Articles and comments from monitored websites
The selenium package is used to automate web browser interaction from Python, along with Beautiful Soup, which is a library that makes it easy to scrape information from web pages. It sits atop an HTML or XML parser, providing Pythonic idioms for iterating, searching, and modifying the parse tree.

#### Unstructured text data from any website
Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured.  

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
BeautifulSoup | Easy to use <br> Popular | Cannot parse dynamic content (i.e. Javascript) | https://anaconda.org/anaconda/beautifulsoup4 <br> https://pypi.org/project/beautifulsoup4/
selenium | Can manipulate dynamic content | More difficult to tune data parsers | https://anaconda.org/anaconda/selenium <br> https://pypi.org/project/selenium/
tweepy | Easy to use | Compatibility issues between versions | https://anaconda.org/conda-forge/tweepy <br> https://tweepi.com/

## Datetime Estimation
A detect datetime from metadata and text. 

### Approach
a chained approach is adopted here as well. dateparser, datefinder and parsedatetime packages are exploited ranked from higher accuracy to higher probability of returning a result. if the most accurate fails to detect the datetime object, the next service is called and so on. detection is based in metadata, where date date information is commonly present. if datetime detection fails for all services in metadata, the same workflow is applied to text data.

### Implementation
The aforementioned approach is implemented as a method (detect_datetime(text, meta, lang) -> datetime) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
dateparser | Relatively high accuracy. | Limited estimations. |  
datefinder | Lower accuracy. | More estimations, returns a list of estimations. |
parsedatetime | Baseline method. | Datetime scheme should be defined. |  

## Geolocation Estimation

### Approach
A method for detecting geolocation from text. geopy with nominatim geocoder are used. entities in the following ranking are preferred: GPE (countries, cities, states), LOC (mountains, bodies of water), FAC (buildings, airports, highways etc.), ORG (companies, agancies, institutions etc.).

### Implementation
The aforementioned approach is implemented as a method (detect_location(text, meta, lang) -> locations) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
Geopy | Easy to use, lots of geocoders. | None (so far). | https://anaconda.org/conda-forge/geopy  https://geopy.readthedocs.io

Geopy is a Python 2 and 3 client for several popular geocoding web services. Geopy makes it easy for Python developers to locate the coordinates of addresses, cities, coun-tries, and landmarks across the globe using third-party geocoders and other data sources. Geopy includes geocoder classes for the OpenStreetMap Nominatim, ESRI ArcGIS, Google Geocoding API, Baidu Maps, Bing Maps API, Yahoo! PlaceFinder, Yandex, IGN France, etc.
https://python.libhunt.com/geopy-alternatives
Geocoders for Geopy
https://github.com/geopy/geopy/issues/171
Nominatim
	Here's the example I've finally figured out (from some far-reaching pages...) - and yes, I've switched to the Google geocoder as Nominatim is pretty sensitive to missing information, Google hammers through it no problem
Google Geocoding
	One thing to note is that Google Maps currently has a per user geocoding limit of 2500/day if you are geocoding without an API key. See https://developers.google.com/maps/documentation/geocoding/usage-limits for more.
	Requires API, google cloud account with a credit card.
Others
	Most of them require an API with a paid subscription.


## Language Detection
PHARM scripts can detect hate speech in texts produced in Italian, Greek and Spanish, but many of the sources might have contents in other foreign languages or local dialects. To work with the three national languages, we find that we must select a procedure to detect the language of the media text when it is not properly declared. There already exist many algorithms designed to automatically detect the language in different kinds of texts within a range of probability. 

### Approach
A chained approach is adopted for improved robustness. textblob, google translate and langdetect services are exploited. If a service fails
the result form the next one is requested.  

### Implementation
The aforementioned approach is implemented as a method (detect_language(text) -> language) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Link
--------|------|------|-----
textblob | Accurate and easy to use | Limited requests. | https://anaconda.org/conda-forge/textblob
googletrans | Accurate and easy to use. | None (so far). | https://anaconda.org/conda-forge/googletrans
pycld2 | Reports estimation reliability. | Only for linux python envs. | https://anaconda.org/syllabs_admin/pycld2
langdetect | Seems accurate, easy to use. | None (so far). | https://anaconda.org/conda-forge/langdetect
alchemyapi | - | No anaconda package, no longer supported by IBM. | https://github.com/AlchemyAPI/alchemyapi_python


## Metadata Selection
Taking into account the requirements of the project (i.e. PHARM might use some rele-vant extra information for hate speech analysis), the sources that will be used for gath-ering the relevant content (i.e. Website articles and comments, YouTube comments and Twitter tweets), interoperability and compatibility considerations for import-ing/exporting data to third party applications that may/should be exploited (i.e. docca-no platform for annotation), the following general specifications have been set:

Format	| JSON
--------|------
Identifier	| doccano ID and/or PID
Data grouping |	PHARM ID (PID) or source url
Annotations	| labels from doccano – annotation data
Metadata |	fields may vary from across sources
Text |	payload

The main/base data field is the text (content), accompanied by the id, annotations and meta fields. Meta field is a container, including all additional data. A fundamen-tal/minimum set of metadata will be used for all platforms. These will be the Pharm ID (PID), the source URL, the title, author, date, tags and categories. These fields are more probable to be found for all records across different sources. The following figure gives a hierarchical view of the proposed data scheme.

A custom identifier has been designed, serving as a compact and unique representation of each record retrieved. This numerical value is composed as a synthesis of 2 digits for identifying language, 2 digits for identifying source, 8 digits derived as a hash from the corresponding URL, and 4 digits for enumerating items with the same language

## Hate Speech Detection
A couple of methods for finding search terms has been implemented. These include simple string matching, approximate string matching with the use of the suitable met-rics, such as Levenshtein Distance, Damerau-Levenshtein Distance, Jaro Distance, Jaro-Winkler Distance, Match Rating Approach Comparison, Hamming Distance. Term match-ing also aims at being word-suffix agnostic, accommodating the various suffixes that may exist in nouns for many languages (i.e. Greek language features different suffixes gen-der/singular-plural.  A word vector approach has also been tested, taking into account the semantic meaning of the terms. A fixed-dictionary approach (with predefined phrases or terms) and a more agile version featuring dynamic term combinations (i.e. adjectives combined with nouns) are under evaluation.

### Approach
Two approaches are implemented (mode=0,1,2). The first one is based in a dictionary of terms for four different languages, english, greek, italian and spanish. A language model is loaded (according to the language of the text), common practices are followed (lowercasing, lemmatization, stop word and punctuation removal), and the targeted terms are being searched in the text. If a term (or combination of terms) is found, text segments are denoted as "hate speech". The second one is based in word vectors allowing for a more semantic detection. The same workflow is followed for this method as well (lemmatization etc.). if mode is set to
"2" the union of the results from both methods is returned.

### Implementation
The aforementioned approach is implemented as a method (detect_hate(text, meta, lang, mode) -> matches[]) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
spacy | Pretrained models (en, es, it, el), lots of linguistic features (part of speech tagging, entity recognition, tokenization, lemmatization, rule based matching, word vectors, etc.). | Models with vectors are slow. | https://anaconda.org/conda-forge/spacy  https://spacy.io/usage  https://spacy.io/usage/linguistic-features#named-entities

## Topic Modeling

### Approach
a combined method (tfid + lda) is deployed for topic modeling. detected topics and most common terms are printed. a method for topic modeling based on tfid (term frequency–inverse document frequency) approach. a list of topics is created based on a corpus of text items. a method for topic modeling based on lda (latent dirichlet allocation) approach. a list of topics is created based on a corpus of text items.

### Implementation
The aforementioned approach is implemented as a method (topic_modeling(corpus, language) -> topics, common_words) in the analysis_nlp.py file.

## Hate speech related entity collection
Topic modeling.

# How to use
Please see the instructions in the Config/main.txt configuration file.

### [TWITTER-STREAM]

SET THIS PARAMETER FOR GATHERING TWEETS VIA THE TWITTER API USING THE STREAM FUNCTION. YOU CAN SET THE PARAMETER to "en",  "el", "es" or "it" FOR USING the greek, english, spanish, or italian keyword list. You can find and modify the keyword lists in the "Keywords" directory. Results are stored to "Data/scraper_twitter_data.json". Comment the following parameter if you do not want to use this method.
[TWITTER-STREAM]="el"

### [YOUTUBE-SEARCH] & [YOUTUBE-SEARCH-NRESULTS]
Set this parameter for collecting YouTube comments via the Google API.  Please set keywords for searching content, e.g. "migration refugees". Results are stored to "Data/scraper_youtube_data.json". Comment the following parameter if you do not want to use this method.
[YOUTUBE-SEARCH]="μετανάστες"  
[YOUTUBE-SEARCH-NRESULTS]="200"

### [WEBSITE-SINGLE]
Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured. Examples for each case:  
https://www.facebook.com/groups/8080169598  
https://www.youtube.com/watch?v=fDWFVI8PQOI  
https://www.makeleio.gr/επικαιροτητα/Ο-υπουργός-παιδεραστής-και-η-αποκάλυ/  
Comment the following parameter  line if you do not want to use this method.  
  
[WEBSITE-SINGLE]="https://www.facebook.com/groups/8080169598"  

### [WEBSITE-MASS] & [WEBSITE-MASS-CYCLES]
Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured. Comment the following parameter  line if you do not want to use this method.  
[WEBSITE-MASS]="http://www.voxespana.es"  
[WEBSITE-MASS-CYCLES]="0"

### [ANALYZE-DATA]
Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured. Comment the following parameter  line if you do not want to use this method.  

[ANALYZE-DATA]="Data\\scraper_web\\*vimaorthodoxias*_data.json"


