# set_of_scripts

# Sources selection

# Hate speech detection
A couple of methods for finding search terms has been implemented. These include simple string matching, approximate string matching with the use of the suitable met-rics, such as Levenshtein Distance, Damerau-Levenshtein Distance, Jaro Distance, Jaro-Winkler Distance, Match Rating Approach Comparison, Hamming Distance. Term match-ing also aims at being word-suffix agnostic, accommodating the various suffixes that may exist in nouns for many languages (i.e. Greek language features different suffixes gen-der/singular-plural.  A word vector approach has also been tested, taking into account the semantic meaning of the terms. A fixed-dictionary approach (with predefined phrases or terms) and a more agile version featuring dynamic term combinations (i.e. adjectives combined with nouns) are under evaluation.


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


