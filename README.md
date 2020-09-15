# Project Description
Set of scripts of algorithms - The algorithm’s scripts will be made available in Github so they can be shared with the rest of the team, but also with external stakeholders. The URL of the scripts in Github will allow its evaluation by testing if all scripts can be run with the corresponding expected result (download of contents from different digital and social media, automated classification, etc.). 

## Sources Selection

Several sources have been selected for the collection of content related to hate speech. The sources include articles and comments from a list of specific Spanish, Italian and Greek websites, twitter, youtube and facebook comments. The website list includes 22 Spanish, 12 Italian and 16 Greek websites that are prone to publishing hate speech content in the articles or in the comments section. The list of websites and Facebook pages was initialized and updated by the media experts of the three participating universities. Site-specific scraping scripts have been developed for the collection of semi-structured content (includeing accompanying metadata) from the proposed websites. Websites that are not included in the list can be supported using the site-agnostic scraping script. Tweets are gathered using a list of hashtags and filters containing terms relevant to anti-immigration rhetoric. Youtube comments are gathered using search queries relevant to immigration.
A spreadsheet in Google Docs (https://bit.ly/3jaWzEq) for adding sources of interest have been deployed. Each sheet refers to the country of interest (i.e. International, Spanish, Greek, Italian). The selected sources (websites, keywords, search terms, facebook pages etc.) for each platform are included in the current version of the spreadsheet.



## Scraping & Data Collection
A multi-source platform for analysis of unstructured news and social media messages has been developed. It is important that chosen sources are valid and reliable to detect hate speech against refugees and migrants. In addition to this, hate speech data should include data (texts of the news or social media messages) and meta-data (location, language, date, etc.). For this reason, different types of sources (websites and social platforms) have been chosen and the necessary technical implementations have been made to collect the necessary data from these sources. JSON (JavaScript Object Notation) is the preferred format for storing the data. JSON is an open standard, containing labels and contents as an attribute-value pair. One of the advantages of JSON is the flexibility to store different fields depending on the features and information available for each text. In order to store, query, analyze and share news and social media messages, PHARM adopts a semi-structured format based on JSON, adapted to media features. 

### Approach
The existence of any public or private application program interface (API) to collect media data was in high priority. Hence, Twitter API and Google API are exploited for collecting data from the Twitter and YouTube platforms, BeautifulSoup and selenium for scraping texts from web pages and automating web browser interaction via the Python programming language. Semi-structured scrapers for over 50 websites (in English, Greek, Italian and Spanish) have been developed for collecting data massively, whereas routines for gathering data from Facebook groups and pages, YouTube videos and any other website have been also implemented. A prototype JSON-like data format with a simplified description scheme (source, title, text, meta-data) has been formed, towards a unified approach for all sources (with an NoSQL approach). This format is used for storing content from websites (articles and comments), tweets and YouTube comments (for the case of twitter and YouTube the description scheme is more complex). As for the websites, much effort was put on scraping targeted websites (i.e. when DISQUS or/and Facebook users' comments are present). All implementations have been refined to be more robust, accurate, being fully compatible with the doccano (https://github.com/doccano) platform for manual annotation. 

### Implementation
This approach is coded in couple of python files. In specific, scraper_twitter.py, scraper_web.py, scraper_youtube.py, single_facebook.py, single_web.py and single_youtube.py files implement the necessary routines for collecting the content.

#### Twitter tweets via streaming (Twitter API)
The project supports text collection from the twitter via the appropriate API and the stream method. Tweepy is used for accessing the Twitter API. Four dictionaries for filtering tweets have been developed including Greek, English, Spanish and Italian keywords. These can been found in the "Keywords" directory. Results are stored to the "Data/scraper_twitter_data.json" file.

#### Comments from YouTube videos via searching (Google API)
YouTube comment collection is supported via the Google API. A search query should be specified for searching content (e.g. "migration refugees") and the comments from the top results (videos) are collected. Results are stored to the "Data/scraper_youtube_data.json" file.

#### Posts and replies from open Facebook groups and pages
The selenium and BeautifulSoup packages are used to gather content from open Facebook groups and pages. A single URL should be specified. Results are stored to the "Data/single_facebook_data.json" file.

#### Comments from YouTube videos
The selenium and BeautifulSoup packages are used to gather content from a single YouTube video. The corresponding URL should be specified. Results are stored to the "Data/single_youtube_data.json" file.

#### Articles and comments from monitored websites
The selenium+BeautifulSoup duet is exploited once again. For the monitored websites a structured approach is followed. Articles, users' comments, meta-data are recognized and organized based on the selected description scheme. Results are stored to the "Data/scraper_web/" directory.

#### Unstructured text data from any website
This method can be used to collect texts from single web-pages. Results are stored to the "Data/single_web_data.json" file. Data via this method is unstructured.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
BeautifulSoup | Popular and easy to use | Cannot parse dynamic content (i.e. Java-script) | https://pypi.org/project/beautifulsoup4/ <br> https://anaconda.org/anaconda/beautifulsoup4
selenium | Can manipulate dynamic content | More difficult to tune data parsers | https://pypi.org/project/selenium/ <br> https://anaconda.org/anaconda/selenium
tweepy | Easy to use | Compatibility issues between versions | https://pypi.org/project/tweepi/ <br> https://anaconda.org/conda-forge/tweepy
Google API Client | Officially supported by Google | - | https://pypi.org/project/google-api-python-client/ <br> https://anaconda.org/conda-forge/google-api-python-client 

## Datetime Estimation
A method for detecting and standardizing datetime information from metadata and text has been implemented. Besides location and language, when metadata is available, PHARM might use some relevant extra information for hate speech analysis. Some of this extra information, such as date or time, might be available in all cases, but with different formats, which means the necessity of standardization. 

### Approach
For the needs of this requirement, dateparser, datefinder and parsedatetime python packages are exploited, ranked by higher accuracy to higher probability of returning a result. If the most accurate method fails to detect a datetime object, the next service is called. Detection is based in metadata, where date date information is commonly present. if datetime detection fails for all services for the metadata, the same workflow is applied to the text data.

### Implementation
The aforementioned approach is implemented as a method (detect_datetime(text, metadata, language) -> datetime) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
dateparser | Relatively high accuracy | Limited estimations | https://pypi.org/project/dateparser/ <br> https://anaconda.org/conda-forge/dateparser
datefinder | Lower accuracy | Returns a list of estimations | https://pypi.org/project/datefinder/ <br> https://pypi.org/project/datefinder/
parsedatetime | Baseline method | Datetime scheme should be defined | https://pypi.org/project/parsedatetime/ <br> https://anaconda.org/conda-forge/parsedatetime

## Geolocation Estimation

### Approach
A method for detecting geolocation from text data has been coded. The geopy library, along with the nominatim geocoder have been selected. Named entities (linguistic features) are isolated from texts, according to the following ranking: GPE (countries, cities, states), LOC (mountains, bodies of water), FAC (buildings, airports, highways etc.), ORG (companies, agencies, institutions etc.). Next, location estimation is performed for each one of the discovered entities. 

### Implementation
The aforementioned approach is implemented as a method (detect_location(text, metadata, language) -> locations[]) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
Geopy | Easy to use with a plenty of geocoders | None (so far) | https://pypi.org/project/geopy/ <br> https://anaconda.org/conda-forge/geopy  

Geopy is a Python client for several popular geocoding web services, enabling the detection of the coordinates of addresses, cities, countries, and landmarks across the globe using third-party geocoders and other data sources. Geopy includes geocoder classes for the OpenStreetMap Nominatim, ESRI ArcGIS, Google Geocoding API, Baidu Maps, Bing Maps API, Yahoo! PlaceFinder, Yandex, IGN France, etc.

## Language Detection
PHARM will mainly process text produced in Greek, Italian, and Spanish, but many of the sources might have contents in other foreign languages or local dialects. To work with these three national languages, a procedure to detect the language of the media text when it is not properly declared should be present. There already exist many algorithms designed to automatically detect the language in different kinds of texts within a range of probability. 

### Approach
A recursive approach is adopted for improved robustness. Textblob, googletrans and langdetect services are used. If a service fails the result form the next one is requested.  

### Implementation
The aforementioned approach is implemented as a method (detect_language(text) -> language) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Link
--------|------|------|-----
textblob | Accurate and easy to use | Limited requests | https://pypi.org/project/textblob/ <br> https://anaconda.org/conda-forge/textblob
googletrans | Accurate and easy to use | None (so far) | https://pypi.org/project/googletrans/ <br> https://anaconda.org/conda-forge/googletrans
pycld2 | Reports estimation reliability | Only for linux python envs | https://pypi.org/project/pycld2/ <br> https://anaconda.org/syllabs_admin/pycld2
langdetect | Accurate easy to use | None (so far) | https://pypi.org/project/langdetect/ <br> https://anaconda.org/conda-forge/langdetect


## Metadata Selection
Taking into account the requirements of the project (i.e. PHARM might use some relevant extra information for hate speech analysis), the sources that will be used for gath-ering the relevant content (i.e. Website articles and comments, YouTube comments and Twitter tweets), interoperability and compatibility considerations for import-ing/exporting data to third party applications that may/should be exploited (i.e. docca-no platform for annotation), the following general specifications have been set:

Format	| JSON
--------|------
Identifier	| doccano ID and/or PID
Data grouping |	PHARM ID (PID) or source url
Annotations	| labels from doccano – annotation data
Metadata |	fields may vary from across sources
Text |	payload

The main/base data field is the text (content), accompanied by the id, annotations and meta fields. Meta field is a container, including all additional data. A fundamental/minimum set of metadata will be used for all platforms. These will be the Pharm ID (PID), the source URL, the title, author, date, tags and categories. These fields are more probable to be found for all records across different sources. The following figure gives a hierarchical view of the proposed data scheme.

A custom identifier has been designed, serving as a compact and unique representation of each record retrieved. This numerical value is composed as a synthesis of 2 digits for identifying language, 2 digits for identifying source, 8 digits derived as a hash from the corresponding URL, and 4 digits for enumerating items with the same language

## Hate Speech Detection
A couple of methods for finding key terms for hate speech detection have been implemented. These include simple string matching, approximate string matching with the use of the appropriate metrics, such as Levenshtein Distance, Damerau-Levenshtein Distance, Jaro Distance, Jaro-Winkler Distance, Match Rating Approach Comparison, Hamming Distance. Term matching also aims at being suffix agnostic, accommodating the various suffixes that may exist in nouns for many languages (i.e. Greek language features different suffixes for gender or singular/plural versions). A word-vector approach has also been developed, taking into account the semantic meaning of the terms. A hybrid dictionary-based approach with predefined phrases, along with dynamic term combinations (i.e. adjectives combined with nouns) has been implemented and is under evaluation.

### Approach
Two modes can be used for filtering (mode=0,1,2). The first one is based in a dictionary of terms for four different languages: English, Greek, Italian and Spanish. A language model is loaded (according to the language of the text), common practices are followed (lowercasing, lemmatization, stop word and punctuation removal), and the targeted terms are being searched in the text. If a term (or combination of terms) is found, text segments are denoted as "hate speech". The second one is based in word vectors allowing for a more semantic detection. The same workflow is followed for this method as well (lemmatization etc.). if mode is set to "2" the union of the results from both methods is returned.

### Implementation
The aforementioned approach is implemented as a method (detect_hate(text, metadata, language, mode) -> matches[]) in the analysis_nlp.py file.

### Methods/Packages Evaluated
Package | Pros | Cons | Links
--------|------|------|-----
spacy | Pretrained models (EN, ES, IT, EL), lots of linguistic features (part of speech tagging, entity recognition, tokenization, lemmatization, rule based matching, word vectors, etc.) | Models with vectors are slow | https://pypi.org/project/spacy/ <br> https://anaconda.org/conda-forge/spacy

## Topic Modeling

### Approach
A combined method tfid (term frequency–inverse document frequency) plus lda (latent dirichlet allocation) is deployed for topic modeling. Detected topics and most common terms are returned. A list of topics is created based on a corpus of text items.

### Implementation
The aforementioned approach is implemented as a method (topic_modeling(corpus[], language) -> topics[], words[]) in the analysis_nlp.py file.

## Entity Collection for Hate Speech
Identifying what an unstructured text is about is a challenging task. Most of the studies use search terms (words, lemmas, stems, combination of words with rules, etc.) to filter the texts that correspond to a certain topic, but it often happens that some topic-related contents remain excluded or that some topic-unrelated contents pass the filter and become included. This fact makes highly relevant the chosen mechanism to detect the topic in a large collection of news or social media messages.

### Approach
A similar to topic modeling approach has been implemented, including named entity detection for the identified topics.

# How to run the project
Review the first lines of code (marked as "PYTHON SETUP") in the various Python files of the project to install the necessary libraries for executing the project. Use the "main.py" file as the starting script to run the code. The supported workflows/analyses can be controlled via the "Config/main.txt" configuration file. Instructions for controlling the workflow are following and are also included in the main configuration file. This set of scripts can execute various text collection and processing tasks, as specified by the requirements of the PHARM project. These tasks can be grouped into two main categories: data collection and data analysis.

### [TWITTER-STREAM]
Set this parameter to collect tweets via Twitter's stream function. Set the parameter to "en", "el", "es" or "it" to use the Greek, English, Spanish, or Italian keyword list. You can find and modify the keyword lists in the "Keywords" directory. Results are stored to "Data/scraper_twitter_data.json". Comment out the following line to skip this type of data collection.  

[TWITTER-STREAM]="el"

### [YOUTUBE-SEARCH] & [YOUTUBE-SEARCH-NRESULTS]
Set these parameters for collecting YouTube comments via the Google API. Use the [YOUTUBE-SEARCH] parameter to set the keywords for searching content, e.g. "migration refugees" and the [YOUTUBE-SEARCH-NRESULTS] parameter to regulate the number of returned results. Results are stored to "Data/scraper_youtube_data.json". Comment the following lines if you do not want to use this method.  
  
[YOUTUBE-SEARCH]="μετανάστες"  
[YOUTUBE-SEARCH-NRESULTS]="200"

### [WEBSITE-SINGLE]
Set this parameter for collecting texts from a single webpage. Simply set the URL of the webpage. The URL can point to an open Facebook Group or Page, a YouTube video or any other website. Results are stored to "Data/single_facebook_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Data management is semi-structured for the Facebook and YouTube platfors, whereas is unstructured for the rest of the webpages. Comment out the following lines to skip this type of data collection.
  
[WEBSITE-SINGLE]="https://www.facebook.com/groups/8080169598"  
[WEBSITE-SINGLE]="https://www.facebook.com/playcompass"  
[WEBSITE-SINGLE]="https://www.youtube.com/watch?v=fDWFVI8PQOI"  
[WEBSITE-SINGLE]="https://bit.ly/33b7jLZ"

### [WEBSITE-MASS] & [WEBSITE-MASS-CYCLES]
Set these two parameters for collecting articles and comments from the supported websites for structured scraping. The list of the supported websites is stored in the "Config/websites.txt" file. Make use of the [WEBSITE-MASS] and [WEBSITE-MASS-CYCLES] to set the URL and to define the number of scans/cycles the spider will perform to the site, respectively. The algorithm automatically discovers  different pages/articles within the site, keeps a list of already visited hyperlinks, stores content and continues to a new unvisited destination. Results are stored to seperate, according the name of the site, files in the "Data/scraper_web/" directory. Comment out the following lines for skipping this type of data collection. 
   
[WEBSITE-MASS]="http://www.voxespana.es"  
[WEBSITE-MASS-CYCLES]="100"

### [ANALYZE-DATA]
Set this parameter for executing the data analyses procedures, acoording to the project's requirements, such as topic modeling, language detection, geolocation estimation, daterime parsing, hate speech detection etc. These analyses will be refined and updated with new functions, according to the project's timeline. The analyses can be applied to the data that is collected and stored in the "Data" directory. Use the following parameter to point to a specific file. Once the script finishes, a new file with the same name as the original and with the "_processed" suffix will be generated. Derived data can be used for manual annotation (for hate speech), or, generally, for developing a "hate speech" corpus.

[ANALYZE-DATA]="Data\\scraper_web\\*vimaorthodoxias*_data.json"
