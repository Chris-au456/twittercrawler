#!/usr/bin/python3
""" main twitcrawler app """
import requests
import sys
import time
import json
import datetime
import hashlib
from operator import itemgetter


r = requests.session()


class Tweet: 
    """ Class for Single Twitter Post """ 

    def __init__(self, uid, created_at, text): 
        
        self.uid = uid
        self.created_at = created_at
        self.text = text

    def serialize_post(self) -> object:
        """
            Extract post attributes and condense into simple object
            :return: Simple tweet object
        """

        new_created_at = self.created_at.replace('+0000 ', '')
        new_datetime = datetime.datetime.strptime(new_created_at, '%a %b %d %H:%M:%S %Y')

        tweet = {
            "id": self.uid,
            "timestamp": int(new_datetime.timestamp()),
            "date_created": self.created_at,
            "text": self.text
        }
        return tweet


def usage() -> None:
    """
        Returns the usage of the app
        :return: 
    """
    print("Usage:")
    print("{} [ Twitter Username ]".format(sys.argv[0]))
    sys.exit(1)


def get_guest_token(auth_token) -> int:
    """
        Returns a guest token for anonymous authentication
        :return: Returns an integer guest token
    """
    
    url = "https://api.twitter.com/1.1/guest/activate.json"
    headers = {
        "Authorization": "Bearer {}".format(auth_token)
    }

    result = r.post(url, headers=headers)
    raw_data = json.loads(result.text)

    guest_token = int(raw_data['guest_token'])

    return guest_token


def get_user_rest_id(username, auth_token, guest_token) -> int:
    """
        Given a username, returns the targeted user's API ID to pull their latest tweets
        :return: An integer that is their REST ID
    """
    url = 'https://api.twitter.com/graphql/4S2ihIKfF3xhp-ENxvUAfQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{}%22%2C%22withHighlightedLabel%22%3Atrue%7D'.format(username)
    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "x-guest-token": str(guest_token)
    }

    raw_data = r.get(url, headers=headers)
    raw_data = json.loads(raw_data.text)
    user_id = int(raw_data['data']['user']['rest_id'])

    return user_id


def get_all_tweets(user_id, guest_token, auth_token) -> list:
    """ 
        Given a username, return all tweets posted by that user.
        :param: username
        :return: A list of json objects containing all the user's tweets
    """ 
    url = "https://twitter.com:443/i/api/2/timeline/profile/{}.json".format(user_id)
    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "x-guest-token": str(guest_token)
    }
    raw_posts = r.get(url, headers=headers)

    json_posts = json.loads(raw_posts.content)

    tweets_simplified = []

    for i in json_posts['globalObjects']['tweets']:
        new_tweet = Tweet(str(i),  
                        json_posts['globalObjects']['tweets'][i]['created_at'], 
                        json_posts['globalObjects']['tweets'][i]['text'] 
                    )
        tweets_simplified.append(new_tweet.serialize_post())

    return tweets_simplified


def sort_tweets(tweets) -> list:
    """
        Supplying a list of json objects, this will sort by timestamp
        :return: A list of tweets sorted
    """
    sorted_tweets = sorted(tweets, key=lambda s: s['timestamp'], reverse=True)
    return sorted_tweets

def get_recent_tweets(tweets) -> object:
    """
        Gets the top 5 most recent tweets
        :return: Returns an object of 5 tweets
    """

    top_five = []
    count = 0
    sorted_tweets = sort_tweets(tweets)
    for i in sorted_tweets:
        top_five.append(i)
        count += 1
        if count == 5:
            break
    return top_five


def main():
    """
        Main method
        :return: 
    """

    if len(sys.argv) != 2:
        usage() 
        sys.exit(1)

    username = sys.argv[1]

    authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    guest_token = get_guest_token(authorization_token)
    user_rest_id = get_user_rest_id(username, authorization_token, guest_token)


    all_tweets_old = get_all_tweets(user_rest_id, guest_token, authorization_token)
    top_five_tweets = get_recent_tweets(all_tweets_old)

    for i in range(0, len(top_five_tweets)):
        print(top_five_tweets[i]['date_created'])
        print(top_five_tweets[i]['text'])
        print(username)
        print("\n")
    

    try:
        while True:
            time.sleep(600) # 600 seconds in 10 minutes

            guest_token = get_guest_token(authorization_token)
            user_rest_id = get_user_rest_id(username, authorization_token, guest_token)

            all_tweets_refreshed = get_all_tweets(user_rest_id, guest_token, authorization_token)
            
            print("\n")
            print(datetime.datetime.now())
            print("Latest Tweets:")
            
            hash_of_new_tweets = hashlib.md5()
            hash_of_old_tweets = hashlib.md5()

            hash_of_new_tweets.update(str(all_tweets_refreshed).strip().encode())
            hash_of_old_tweets.update(str(all_tweets_old).strip().encode())


            if hash_of_new_tweets.hexdigest() != hash_of_old_tweets.hexdigest():
                new_tweets = [x for x in all_tweets_refreshed if x not in all_tweets_old]
                # BUG: When the user deletes a post, one of the older tweets
                for i in new_tweets:
                    print(i['date_created'])
                    print(i['text'])
                    print(username)
                    print("\n")
            else:
                print("No new tweets to report!")

            all_tweets_old = all_tweets_refreshed

    except KeyboardInterrupt:
        print("\n\nGoodbye!")

if __name__ == '__main__':
    main() 