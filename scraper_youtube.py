''' Setup '''
# a list of the required packages is listed here based on anaconda setup commands.

#  conda install -c conda-forge google-api-python-client
#  conda install -c conda-forge google-auth-oauthlib

import os, json, io, pickle
import google.oauth2.credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CLIENT_SECRETS_FILE = "Xtra/youtube_client_secret.json"
PICKLE_FILE = "Xtra/youtube_token.pickle"

SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_authenticated_service():
    # ylopoiisi_me_authentication
    # flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    # credentials = flow.run_console()
    # return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    # ylopoiisi xwris authentication
    credentials = None
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open(PICKLE_FILE, 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


service = get_authenticated_service()

# search videos with query and grab the comments
def search(query, nresults):

    query_results = service.search().list(
            part = 'snippet',
            q = query,
            order = 'relevance', # You can consider using viewCount
            maxResults = int(nresults/50),
            type = 'video', # Channels might appear in search results
            relevanceLanguage = 'en',
            safeSearch = 'moderate',
            ).execute()

    video_id = []
    channel = []
    video_title = []
    video_desc = []
    for item in query_results['items']:
        video_id.append(item['id']['videoId'])
        channel.append(item['snippet']['channelTitle'])
        video_title.append(item['snippet']['title'])
        video_desc.append(item['snippet']['description'])


    # =============================================================================
    # Get Comments of Top Videos
    # =============================================================================
    video_id_pop = []
    channel_pop = []
    video_title_pop = []
    video_desc_pop = []
    comments_pop = []
    comment_id_pop = []
    reply_count_pop = []
    like_count_pop = []

    from tqdm import tqdm

    results = []
    # datajson = {}
    # datajson['comments'] = []
    # dt1 = {}
    # dm1 = {}
    # dm1["id"] = "init"
    # dt1["meta"] = dm1
    # dt1 ["text"] = "init"
    # result1 = json.dumps(dt, ensure_ascii=False)
    # results = result

    print ("type tou results " +str(type (results)))
    for i, video in enumerate(tqdm(video_id, ncols=1000)):
        print(video_id)
        try:
            response = service.commentThreads().list(
                part='snippet',
                videoId=video,
                maxResults=50,  # Only take top 100 comments...
                order='relevance',  # ... ranked on relevance
                textFormat='plainText',
            ).execute()

            comments_temp = []
            comment_id_temp = []
            reply_count_temp = []
            like_count_temp = []
            for item in response['items']:
                dt = {}
                dm = {}
                dm["type"] = 'yt_comment'
                dm ["comment_id"] = item['snippet']['topLevelComment']['id']
                dm["reply_count"] = item['snippet']['totalReplyCount']
                dm["reply_count"] = item['snippet']['totalReplyCount']
                dm["like_count"] = item['snippet']['topLevelComment']['snippet']['likeCount']
                dm["video_id"] = video_id[i]
                dm["channel"] = channel[i]
                dm["video_title"] = video_title[i]
                dm["video_desc"] = video_desc[i]
                dm["author_id"] = (item['snippet']['topLevelComment']['snippet']['authorChannelId'])
                dm["author_name"] = (item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
                dm["rating"] = (item['snippet']['topLevelComment']['snippet']['viewerRating'])
                dm["date"] = (item['snippet']['topLevelComment']['snippet']['publishedAt'])
                dt["meta"] = dm
                dt["text"] = item['snippet']['topLevelComment']['snippet']['textDisplay']
                result = json.dumps(dt, ensure_ascii=False)

                # print (result)
                # print (type(result))
                results.append(result)
                comments_temp.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
                comment_id_temp.append(item['snippet']['topLevelComment']['id'])
                reply_count_temp.append(item['snippet']['totalReplyCount'])
                like_count_temp.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
            comments_pop.extend(comments_temp)
            comment_id_pop.extend(comment_id_temp)
            reply_count_pop.extend(reply_count_temp)
            like_count_pop.extend(like_count_temp)

            video_id_pop.extend([video_id[i]] * len(comments_temp))
            channel_pop.extend([channel[i]] * len(comments_temp))
            video_title_pop.extend([video_title[i]] * len(comments_temp))
            video_desc_pop.extend([video_desc[i]] * len(comments_temp))
        except:
            print('den exei comments')

    # with open('data2.txt', 'w') as outfile:
    #     json.dump(results, outfile, ensure_ascii=False)

    # with io.open('data2.json', 'w', encoding="utf-8") as outfile:
    #     json.dump(results, outfile, ensure_ascii=False)

    # with open('data.txt', 'w') as outfile:
    #     json.dump(datajson, outfile)

    print (type(results))
    f=open('Data\scraper_youtube_data.json','a', encoding='utf-8')
    s1='\n'.join(results)
    f.write(s1)
    f.close()

    # with io.open('test_youtube_io.json', "w", encoding="utf-8") as f:
    #     f.write(results)

    # f=open('test222.json','w')
    # s1='\n'.join(results)
    # f.write(s1)
    # f.close()