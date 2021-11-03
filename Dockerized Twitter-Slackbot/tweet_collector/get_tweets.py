import tweepy
import pymongo

API_KEY = "QPIjuozf4PmA1Tu6AlSAgv0i3"
API_SECRET = "3yCydaIvJh2Aju1sWjDMPud1QHBmItJMjK20tkTxlGvj9fydUi"


def get_auth_handler():
    """
    Function for handling Twitter Authentication. See course material for 
    instructions on getting your own Twitter credentials.
    """
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    return auth


def get_full_text(status):
    """Returns the full text of a (re)tweet"""
    try:
        return status.retweeted_status.full_text
    except AttributeError:  
        return status.full_text


if __name__ == '__main__':
    auth = get_auth_handler()
    api = tweepy.API(auth)

    cursor = tweepy.Cursor(
        api.user_timeline,
        id='khamenei_ir',
        tweet_mode='extended'
    )

    client = pymongo.MongoClient(host="mongodb", port=27017)
    db = client.twitter

    for status in cursor.items(50):
        tweet = {
            'text': get_full_text(status),
            'username': status.user.screen_name,
            'followers_count': status.user.followers_count
        }
        #print(tweet)
        db.tweets.insert_one(tweet)
