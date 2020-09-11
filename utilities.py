''' This python file implements some text cleaning methods '''


''' LIBRARIES IMPORTED '''
import numpy
from bs4 import BeautifulSoup


def clean_soup(soup):
    t = soup.get_text(separator=' ')
    t = t.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('\"', ' ').replace('\'', ' ').strip()
    while '  ' in t:
        t = t.replace('  ', ' ')
    # print(repr(t))
    return t

def clean_whitespaces(text):
    t = text
    t = t.strip()
    while '  ' in t:
        t = t.replace('  ', ' ')
    return t

def clean_accent(text):
    t = text
    t = t.replace('ά', 'α')
    t = t.replace('έ', 'ε')
    t = t.replace('ί', 'ι')
    t = t.replace('ή', 'η')
    t = t.replace('ό', 'ο')
    t = t.replace('ώ', 'ω')
    t = t.replace('ύ', 'υ')
    return t

def correct_unicode():
    with open('Data/stream_none.json') as f:
        for data in f.readlines():
            # print(data)
            data = data.replace("\\n", " ").replace("\\r", " ")
            data = data.encode("ascii", "strict").decode('unicode-escape', 'strict')
            data = data.encode('utf-16', 'surrogatepass').decode('utf-16')
            print(data)
            # data = json.load(f)
            # print(data)

'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import time

#consumer key, consumer secret, access token, access secret.
#Max1
ckey=""
csecret=""
atoken=""
asecret=""


class listener(StreamListener):
    def on_status(self, status):
        if not status.retweeted and 'RT @' not in status.text:
            try:
                tweet = status.extended_tweet['full_text'].replace('\n', '').replace('\"', '').replace('\r', '')
            except AttributeError:
                tweet = status.text
            #print tweet.replace('\n', '').replace('\"', '').replace('\r', '')
            print "{", "\"id\" :", "\"",status.id,"\"",",", "\"user\":", "\"",status.user.screen_name,"\"",",", "\"date\":", "\"",status.created_at,"\"",",", "\"text\":", "\"",tweet.replace('\n', '').replace('\"', '').replace('\r', ''),"\"", "}"

            #If we want aditional information such as time or user
            #print status.created_at, status.user.screen_name, tweet

        else:
            return

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

word = ['sin\npapeles', 'cierre\nfrontera', 'cierre\nfronteras', 'anti\ninmigracion', u'anti\ninmigración', u'invasión\neuropea', 'invasion\neuropea', u'invasión\nsilenciosa', 'invasion\nsilenciosa', 'efecto\nllamada', u'inmigración\nmasiva', u'migración\nmasiva', u'inmigracion\nmasiva', u'migración\nmasa' u'inmigración\nmasa', u'inmigracion\nmasa', 'panchito', 'panchita', 'panchitos', 'panchitas', 'machupichu', 'machu\npichu', 'machupicchu', 'machu\npicchu', 'guachupin', u'guachupín', 'guachupino', 'guachupina', 'sudaca', u'tráfico\nmigrante', u'tráfico\nmigrantes', u'tráfico\ninmigrante', u'tráfico\ninmigrantes', 'repatriar', 'repatriarlo', 'repatriarlos', u'repatriación', 'repatriacion', 'deportar', 'deportarlos', u'deportación', 'deportacion', 
       'desplazado\nputo', 'desplazado\njodido', 'desplazado\nmaldito', 'desplazado\nsucio', 'desplazado\nasqueroso', 'desplazado\nasco', 'desplazado\nmierda', 'desplazados\nputos', 'desplazados\njodidos', 'desplazados\nmalditos', 'desplazados\nsucios', 'desplazados\nasquerosos', 'desplazados\nasco', 'desplazados\nmierda', 'refugiado\nputo', 'refugiado\njodido', 'refugiado\nmaldito', 'refugiado\nsucio', 'refugiado\nasqueroso', 'refugiado\nasco', 'refugiado\nmierda', 'refugiados\nputos', 'refugiados\njodidos', 'refugiados\nmalditos', 'refugiados\nsucios', 'refugiados\nasquerosos', 'refugiados\nasco', 'refugiados\nmierda',
       'moro\nputo', 'moro\nsucio', 'moro\nasco', 'moro\nmierda', 'moro\njodido', 'moro\nmaldito', 'moro\nasqueroso', 'moros\nputos', 'moros\nmierda', 'moros\njodidos', 'moros\nmalditos', 'moros\nasquerosos', 'moros\nsucios', 'moros\nasco', 'mora\nputa', 'mora\nmaldita', 'mora\njodida', 'mora\nasquerosa', 'mora\nmierda', 'mora\nsucia', 'mora\nasco', 'moras\nputas', 'moras\nmalditas', 'moras\njodidas', 'moras\nasquerosas', 'moras\nmierda', 'moras\nsucias', 'moras\nasco', 
       'chino\mandarin', u'chino\mandarín', 'chino\nmandarino', 'china\nmandarina', 'chino\namarillo', 'china\namarilla', 'chino\nputo', 'china\nputa', 'chino\njodido', 'chino\nmierda', 'chino\nasqueroso', 'chino\nsucio', 'chino\nasco', 'chino\nmaldito', 'chinos\nputos', 'chinos\njodidos', 'chinos\nmalditos', 'chinos\nsucios', 'chinos\nasquerosos', 'chinos\nasco', 'chinos\nmierda', 'china\namarilla', 'china\njodida', 'china\nmierda', 'china\nasquerosa', 'china\nsucia', 'china\nmaldita', 'chinas\nputas', 'chinas\njodidas', 'chinas\nmalditas', 'chinas\nsucias', 'chinas\nasquerosas', 'chinas\nasco', 'chinas\nmierda', 
       u'asiático\nputo', u'asiático\njodido', u'asiático\nmaldito', u'asiático\nsucio', u'asiático\nasqueroso', u'asiático\nasco', u'asiático\nmierda', u'asiática\nputa', u'asiática\njodida', u'asiática\nmaldita', u'asiática\nsucia', u'asiática\nasquerosa', u'asiática\nasco', u'asiática\nmierda', u'asiáticos\nputos', u'asiáticos\njodidos', u'asiáticos\nmalditos', u'asiáticos\nsucios', u'asiáticos\nasquerosos', u'asiáticos\nasco', u'asiáticos\nmierda', u'asiáticos\nputas', u'asiáticos\njodidas', u'asiáticos\nmalditas', u'asiáticos\nsucias', u'asiáticos\nasquerosas', u'asiáticos\nasco', u'asiáticos\nmierda', 
       'latino\nputo', 'latino\njodido', 'latino\nmaldito', 'latino\nsucio', 'latino\nasqueroso', 'latino\nasco', 'latino\nmierda', 'latinos\nputos', 'latina\nputa', 'latina\njodida', 'latina\nmaldita', 'latina\nsucia', 'latina\nasquerosa', 'latina\nasco', 'latina\nmierda', 'latinos\njodidos', 'latinos\nmalditos', 'latinos\nsucios', 'latinos\nasquerosos', 'latinos\nasco', 'latinos\nmierda', 'latinas\nputas', 'latinas\njodidas', 'latinas\nmalditas', 'latinas\nsucias', 'latinas\nasquerosas', 'latinas\nasco', 'latinas\nmierda', 
       'negro\nputo', 'negro\njodido', 'negro\nmaldito', 'negro\nsucio', 'negro\nasqueroso', 'negro\nasco', 'negro\nmierda', 'negra\nputa', 'negra\njodida', 'negra\nmaldita', 'negra\nsucia', 'negra\nasquerosa', 'negra\nasco', 'negra\nmierda', 'negros\nputos', 'negros\njodidos', 'negros\nmalditos', 'negros\nsucios', 'negros\nasquerosos', 'negros\nasco', 'negros\nmierda', 'negras\nputas', 'negras\njodidas', 'negras\nmalditas', 'negras\nsucias', 'negras\nasquerosas', 'negras\nasco', 'negras\nmierda',
       'africano\nputo', 'africano\njodido', 'africano\nmaldito', 'africano\nsucio', 'africano\nasqueroso', 'africano\nasco', 'africano\nmierda', 'africana\nputa', 'africana\njodida', 'africana\nmaldita', 'africana\nsucia', 'africana\nasquerosa', 'africana\nasco', 'africana\nmierda', 'africanos\nputos', 'africanos\njodidos', 'africanos\nmalditos', 'africanos\nsucios', 'africanos\nasquerosos', 'africanos\nasco', 'africanos\nmierda', 'africanas\nputas', 'africanas\njodidas', 'africanas\nmalditas', 'africanas\nsucias', 'africanas\nasquerosas', 'africanas\nasco', 'africanas\nmierda', 
       'mulato\nputo', 'mulato\njodido', 'mulato\nmaldito', 'mulato\nsucio', 'mulato\nasqueroso', 'mulato\nasco', 'mulato\nmierda', 'mulata\nputa', 'mulata\njodida', 'mulata\nmaldita', 'mulata\nsucia', 'mulata\nasquerosa', 'mulata\nasco', 'mulata\nmierda', 'mulatos\nputos', 'mulatos\njodidos', 'mulatos\nmalditos', 'mulatos\nsucios', 'mulatos\nasquerosos', 'mulatos\nasco', 'mulatos\nmierda', 'mulatas\nputas', 'mulatas\njodidas', 'mulatas\nmalditas', 'mulatas\nsucias', 'mulatas\nasquerosas', 'mulatas\nasco', 'mulatas\nmierda', 
       'inmigrante\nilegal', u'inmigrante\neconómico', 'inmigrante\ninvasor', 'inmigrante\ninvade', u'inmigrante\ninvasión', 'inmigrante\nroba', 'inmigrante\nrobar', 'inmigrante\nrobos', 'inmigrante\ncriminal', 'inmigrante\ndelinque', 'inmigrante\ndelinquir', 'inmigrante\ndelincuencia', 'inmigrante\nvago', u'inmigrante\nzángano', 'inmigrante\ndelincuente', 'inmigrante\nlacra', 'inmigrante\nviola', 'inmigrante\nviolar', 'inmigrante\nviolador', 'inmigrante\ntraficante', 'inmigrante\ncarterista', 'inmigrante\namenaza', 'inmigrante\ncarga', 'inmigrante\nindocumentado', u'inmigrante\ndeportación', 'inmigrante\ndeportar', u'inmigrante\nváyase', 'inmigrante\nfuera', u'inmigrante\nsaquear', 'inmigrante\nradical', 'inmigrante\nmierda', 'inmigrante\nviolencia', 'inmigrante\ninseguridad', 'inmigrante\nseguridad', 'inmigrante\nasalto', 'inmigrante\nasalta', 'inmigrante\nputo', 'inmigrante\nputa', 'inmigrante\npeligro', 'inmigrante\npeligroso', 'inmigrante\npeligrosa', 'inmigrante\nmiedo', 'inmigrante\nasco', 'inmigrante\nasqueroso', 'inmigrante\nasquerosa', 'inmigrante\nsucio', 'inmigrante\nterror', 'inmigrante\nterrorista', 'inmigrante\ngentuza', 'inmigrante\nbasura', 'inmigrante\nescoria', 'inmigrante\nmaldito', 'inmigrante\nmaldita', 'inmigrante\nviolento', 'inmigrante\nviolenta', 'inmigrante\ndestrozar', 'inmigrante\ndestrozarlo', 'inmigrante\nreventar', 'inmigrante\nreventarlo', 'inmigrante\nmatar', 'inmigrante\nmatarlo', 'inmigrante\nexterminar', 'inmigrante\nexterminarlo', 
       'inmigrantes\nilegales', u'inmigrantes\neconómicos', 'inmigrantes\ninvasores', 'inmigrantes\ninvaden', u'inmigrantes\ninvasión', 'inmigrantes\nroban', 'inmigrantes\nrobar', 'inmigrantes\nrobos', 'inmigrantes\npaguitas', 'inmigrantes\ncriminal', 'inmigrantes\ndelinque', 'inmigrantes\ndelincuentes', 'inmigrantes\ndelinquir', 'inmigrantes\ndelincuencia', 'inmigrantes\nvago', u'inmigrantes\nzángano', 'inmigrantes\nlacra', 'inmigrantes\nviolan', 'inmigrantes\nviolar', 'inmigrantes\nvioladores', 'inmigrantes\ntraficantes', 'inmigrantes\ncarteristas', 'inmigrantes\namenaza', 'inmigrantes\ncarga', 'inmigrantes\nindocumentados', u'inmigrantes\ndeportación', 'inmigrantes\ndeportar', u'inmigrantes\nváyanse', 'inmigrantes\nfuera', u'inmigrantes\nsaquear', u'inmigrantes\nsaquean', 'inmigrantes\nradical', 'inmigrantes\nmierda', 'inmigrantes\nviolencia', 'inmigrantes\ninseguridad', 'inmigrantes\nseguridad', 'inmigrantes\nasalto', 'inmigrantes\nasaltan', 'inmigrantes\nputo', 'inmigrantes\nputa', 'inmigrantes\npeligro', 'inmigrantes\npeligrosos', 'inmigrantes\nmiedo', 'inmigrantes\nasco', 'inmigrantes\nasquerosos', 'inmigrantes\nsucios', 'inmigrantes\nterror', 'inmigrantes\nterroristas', 'inmigrantes\ngentuza', 'inmigrantes\nbasura', 'inmigrantes\nescoria', 'inmigrantes\nmalditos', 'inmigrantes\nviolentos', 'inmigrantes\ndestrozar', 'inmigrantes\ndestrozarlos', 'inmigrantes\nreventar', 'inmigrantes\nreventarlos', 'inmigrantes\nmatar', 'inmigrantes\nmatarlos', 'inmigrantes\nexterminar', 'inmigrantes\nexterminarlos']


twitterStream = Stream(auth, listener())
twitterStream.filter(track=word, languages = ["es"])
'''
