# Set of scripts for the PHARM project
Set of scripts of algorithms - The algorithm’s scripts will be made available in Github so they can be shared with the rest of the team, but also with external stakeholders. The URL of the scripts in Github will allow its evaluation by testing if all scripts can be run with the corresponding expected result (download of contents from different digital and social media, automated classification, etc.). 

# Sources selection

* semi structured
** 22 spanish websites
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

# Scraping & data collection
SET THIS PARAMETER FOR GATHERING TWEETS VIA THE TWITTER API USING THE STREAM FUNCTION. YOU CAN SET THE PARAMETER to "en",  "el", "es" or "it" FOR USING the greek, english, spanish, or italian keyword list. You can find and modify the keyword lists in the "Keywords" directory. Results are stored to "Data/scraper_twitter_data.json". Comment the following parameter if you do not want to use this method.

[TWITTER-STREAM]="el"

Set this parameter for collecting YouTube comments via the Google API.  Please set keywords for searching content, e.g. "migration refugees". Results are stored to "Data/scraper_youtube_data.json". Comment the following parameter if you do not want to use this method.

[YOUTUBE-SEARCH]="μετανάστες"
[YOUTUBE-SEARCH-NRESULTS]="200"

Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured.

[WEBSITE-SINGLE]="https://www.facebook.com/groups/8080169598"
[WEBSITE-SINGLE]="https://www.facebook.com/groups/129244443820851"
[WEBSITE-SINGLE]="https://www.youtube.com/watch?v=7lsj4mBU4_s"
[WEBSITE-SINGLE]="https://bit.ly/33b7jLZ"

Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured. Comment the following parameter  line if you do not want to use this method.

[WEBSITE-MASS]="http://www.liberoquotidiano.it"
[WEBSITE-MASS-CYCLES]="0"

Set this parameter for collecting texts from a single web page. Please set a URL. The URL can point to an open Facebook group, a single tweet from Twitter, a video from YouTube or any other website. Results are stored to "Data/single_facebook_data.json",  "Data/single_twitter_data.json", "Data/single_youtube_data.json" and  "Data/single_web_data.json" respectively. Website data is unstructured. Comment the following parameter  line if you do not want to use this method.

[ANALYZE-DATA]="Data\\scraper_web\\*vimaorthodoxias*_data.json"

# Geographical detection
Methods/Frameworks Evaluated
spacy
Pros: Pretrained models (en, es, it, el), lots of linguistic features (part of speech tagging, entity recognition, tokenization, lemmatization, rule based matching, word vectors, etc.). 
Cons: Models with vectors are slow.
https://anaconda.org/conda-forge/spacy
https://spacy.io/usage
https://spacy.io/usage/linguistic-features#named-entities
Geopy
Pros: Easy to use, lots of geocoders.
Cons: None (so far).
https://anaconda.org/conda-forge/geopy
https://geopy.readthedocs.io
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

# Language detection
Packages Evaluated
textblob
Pros: Accurate, easy to use.
Cons: Limited requests.
https://anaconda.org/conda-forge/textblob
googletrans
Pros: Seems accurate, easy to use.
Cons: None (so far).
https://anaconda.org/conda-forge/googletrans
pycld2 (Chromium Compact Language Detector)
Pros: Reports estimation reliability.
Cons: Only for linux python envs.
https://anaconda.org/syllabs_admin/pycld2
langdetect (Compact Language Detection Kit)
Pros: Seems accurate, easy to use.
Cons: None (so far).
https://anaconda.org/conda-forge/langdetect
alchemyapi (Alchemy API)
Pros: To be tested (maybe).
Cons: No anaconda package, no longer supported by IBM.
https://github.com/AlchemyAPI/alchemyapi_python

# Metadata selection
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

# Hate speech detection
A couple of methods for finding search terms has been implemented. These include simple string matching, approximate string matching with the use of the suitable met-rics, such as Levenshtein Distance, Damerau-Levenshtein Distance, Jaro Distance, Jaro-Winkler Distance, Match Rating Approach Comparison, Hamming Distance. Term match-ing also aims at being word-suffix agnostic, accommodating the various suffixes that may exist in nouns for many languages (i.e. Greek language features different suffixes gen-der/singular-plural.  A word vector approach has also been tested, taking into account the semantic meaning of the terms. A fixed-dictionary approach (with predefined phrases or terms) and a more agile version featuring dynamic term combinations (i.e. adjectives combined with nouns) are under evaluation.

# Hate speech related entity collection
Topic modeling.

# How to use the framework
Please see the instructions in the Config/main.txt configuration file.


