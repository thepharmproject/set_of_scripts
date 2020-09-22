''' Setup '''
# a list of the required packages is listed here based on anaconda setup commands.

# conda install -c conda-forge tweepy

''' Libraries '''
import time, argparse, string, json, sys, random
from datetime import datetime
import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener


# Helper functions
def get_parser():
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='twitter')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory",
                        default='Data')
    return parser

class MyListener(StreamListener):

    def __init__(self, data_dir, query):
        super(MyListener, self).__init__()
        # query_fname = format_filename(query)
        self.outfile = "%s/scraper_%s_data.json" % (data_dir, query)

    def on_status(self, status):
        print (status.text)
        # print (type(status))

        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        dt = {}
        dm = {}
        dm["type"] = 'twitter_comment'
        dm['date'] = status.created_at.strftime("%m/%d/%Y")
        dm['tweet_id'] = status.id
        dm['is_retweet'] = is_retweet
        dm['is_quote'] = is_quote
        dm['user_id'] = status.user.id
        dm['username'] = status.user.name
        dm['scr_name'] = status.user.screen_name
        dm['location'] = status.user.location
        dm['followers'] = status.user.followers_count
        dm['friends'] = status.user.friends_count
        dm['quoted_text'] = quoted_text
        dt["meta"] = dm
        dt["text"] = status.text

        # writer.writerow(
        #     {'date': status.created_at, 'is_retweet': is_retweet, 'is_quote': is_quote,


        try:

            f = open(self.outfile, 'a', encoding='utf-8-sig')
            result = json.dumps(dt, ensure_ascii=False)
            f.write(result + '\n')
            f.close()

            # with open(self.outfile, 'a', encoding='utf-8-sig') as f:
            #     f.write(dt)
            #     return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    # def on_data(self, data):
    #
    #     #data = data.replace("\\n", " ").replace("\\r", " ")
    #     #data = data.encode("ascii", "strict").decode('unicode-escape', 'strict')
    #     #data = data.encode('utf-16', 'surrogatepass').decode('utf-16')
    #
    #     # na epilegoume ta pedia tou riga
    #     # na valoume to pedio "type" sto "meta" kai genika na akoluthisoyme to format mas
    #
    #     try:
    #         with open(self.outfile, 'a', encoding='utf-8-sig') as f:
    #             f.write(data)
    #
    #             print("data")
    #             print(data)
    #             print ('type of data:')
    #             print (type(data))
    #             return True
    #     except BaseException as e:
    #         print("Error on_data: %s" % str(e))
    #         time.sleep(5)
    #     return True

    def on_error(self, status):
        print('error', status)
        return True

    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status

def stream(lang):

    print('Starting...')
    print('Encoding is... ', sys.getdefaultencoding())
    parser = get_parser()
    args = parser.parse_args()
    # args.query = 'hate'

    print('Start tweepy...')
    consumer_key = 'bk7wn33YtsA2W2HTtP9o6yr26'
    consumer_secret = 'YougqBSBRFpg9CdBbTBCDCJLD3brZKojMzUDfB6nvsc5PJ0p5B'
    access_token = '955766670135644160-CqYMwTNxsiDBIikR8lhfaZUb6wxUiU8'
    access_secret = 'CWAUOPLt81NktT9hZaoIcWAuMmy2XxVmB8WVXyzrlJ8hj'
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    print('Start gathering... to folder \'', args.data_dir, '\' with argument \'', args.query, '\'')
    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))

    # load the keywords and for the query phrases
    with open('Keywords\\keywords_' + lang + '_s.txt', 'r', encoding='utf-8') as file:    dictionary = file.read().splitlines()
    with open('Keywords\\keywords_' + lang + '_a.txt', 'r', encoding='utf-8') as file:    terms_a = file.read().splitlines()
    with open('Keywords\\keywords_' + lang + '_b.txt', 'r', encoding='utf-8') as file:    terms_b = file.read().splitlines()
    for term_a in terms_a:
         for term_b in terms_b:
            # ignore suffixes
            if term_a.find("/") > 0:    term_a = term_a[:term_a.find("/")]
            if term_b.find("/") > 0:    term_b = term_b[:term_b.find("/")]
            # if the suffix ends with a "-" join the words instead of making a phrase
            if term_a[-1] == '-':       dictionary.append(term_a[:-1] + term_b)
            else:                       dictionary.append(term_a + ' ' + term_b)
    dictionary = random.choices(dictionary, k=200)

    print(dictionary)
    twitter_stream.filter(track=dictionary)

def timeline(username):
    print('eimai thoes')

