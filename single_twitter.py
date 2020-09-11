#This code creates the dataset from Corpus.csv which is downloadable from the
#internet well known dataset which is labeled manually by hand. But for the text
#of tweets you need to fetch them with their IDs.
import tweepy

# Twitter Developer keys here
consumer_key = 'bk7wn33YtsA2W2HTtP9o6yr26'
consumer_key_secret = 'YougqBSBRFpg9CdBbTBCDCJLD3brZKojMzUDfB6nvsc5PJ0p5B'
access_token = '955766670135644160-CqYMwTNxsiDBIikR8lhfaZUb6wxUiU8'
access_token_secret = 'CWAUOPLt81NktT9hZaoIcWAuMmy2XxVmB8WVXyzrlJ8hj'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# This method creates the training set
def createTrainingSet(corpusFile, targetResultFile):
    import csv
    import time

    counter = 0
    corpus = []

    with open(corpusFile, 'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")

        for row in lineReader:
            print(row[2])
            corpus.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})

    sleepTime = 2
    trainingDataSet = []

    for tweet in corpus:
        # try:
        tweetFetched = api.get_status(tweet["tweet_id"])
        print("Tweet fetched" + tweetFetched.text)
        tweet["text"] = tweetFetched.text
        trainingDataSet.append(tweet)
        time.sleep(sleepTime)

        # except:
        #     print("Inside the exception - no:2")
        #     continue

    with open(targetResultFile, 'w') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet

def scrape(url, hash, soup, results):
    # Code starts here
    # This is corpus dataset
    corpusFile = "corpus.csv"
    # This is my target file
    targetResultFile = "results.csv"
    # Call the method
    resultFile = createTrainingSet(corpusFile, targetResultFile)