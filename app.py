#!/usr/bin/python3
""" main app """
import requests
import sys
import time
import json


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
        tweet = {
            "id": self.uid,
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


def get_all_tweets(user_id, guest_token, auth_token) -> object:
    """ 
        Given a username, return all tweets posted by that user.
        :param: username
        :return: A Json object of all the user's tweets
    """ 
    url = "https://twitter.com:443/i/api/2/timeline/profile/{}.json".format(user_id)
    headers = {
        "Authorization": "Bearer {}".format(auth_token),
        "x-guest-token": str(guest_token)
    }
    raw_posts = r.get(url, headers=headers)

    json_posts = json.loads(raw_posts.content)
    # json.dumps(json_posts, indent=4, sort_keys=True) 

    tweets_simplified = []

    for i in json_posts['globalObjects']['tweets']:
        new_tweet = Tweet(str(i),  
                        json_posts['globalObjects']['tweets'][i]['created_at'], 
                        json_posts['globalObjects']['tweets'][i]['text'] 
                    )
        tweets_simplified.append(new_tweet.serialize_post())

    return tweets_simplified


def main():
    """
        Main method
        :return: 
    """

    # Uncomment me whne done 
    if len(sys.argv) != 2:
        usage() 
        sys.exit(1)

    username = sys.argv[1]

    authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    guest_token = get_guest_token(authorization_token)
    user_rest_id = get_user_rest_id(username, authorization_token, guest_token)


    for i in get_all_tweets(user_rest_id, guest_token, authorization_token):
        print(i)




if __name__ == '__main__':
    main() 