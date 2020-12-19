#!/usr/bin/python3
import app as twitcrawler
from flask import Flask
from flask_restplus import Resource, Api, reqparse, inputs


app = Flask(__name__)
api = Api(app, title="Chris' API", version="0.1")


@api.route('/twitcrawler')
@api.param("username", type=str)
@api.response(200, 'Successfully fetched tweets')
@api.response(500, 'Internal server errror')
class TwitCrawler(Resource):

    def post(self):
        """
            API Post request (given a twitter username), returns 
            all the latest tweets by that user.
            :param: self
            :return: Sorted tweet objects 
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        args = parser.parse_args()

        authorization_token = 'AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
        guest_token = twitcrawler.get_guest_token(authorization_token)
        user_rest_id = twitcrawler.get_user_rest_id(args['username'], authorization_token, guest_token)

        all_tweets = twitcrawler.get_all_tweets(user_rest_id, guest_token, authorization_token)
        tweets_sorted = twitcrawler.sort_tweets(all_tweets)
        
        output = { args['username']: tweets_sorted }
        return output
        

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=80, use_reloader=False)
