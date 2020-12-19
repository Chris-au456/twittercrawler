# Developer's Notes

Overall a tough, but very fun challenge! 

Basically, a request for twitter tweets returns as json objects.
Each tweet is essentially a json object containing an id, the date created, text and a bunch of other irrelevant points 
that I didnt need. This was solved by serializing the posts into another json object where the data structure was 
alot less complicated to work with. 


I tried to use a range of tactics such as web browser emulation, web scraping with beautiful soup but because of the dynamic website twitter.com is (javascript), it seems like it's clear that twitter just dont want us scraping for data across the site. 
Doing some investigation, research and boarderline reverse engineering the application It was found that pulling tweets in json format are actually authenticated (even if you're not logged in). 

## Steps which I essentially turned into code: 

### Step 1:
Collect the bearer's token in the Authorization header.
From my testing on other machines / web browsers this is consistently:
AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
This suggests that it's most likely hard coded for guest (anonymous) users.


### Step 2: 
Generate a guest token through a POST request with the Authorization header set to https://api.twitter.com/1.1/guest/activate.json.
I did get a bit of help from this github issue on this step and the next step! 
Source: https://github.com/Foo-Manroot/tweet-feed/issues/1 


### Step 3: 
We now have our key headers to access a users tweets. 
With the Authorization header and the x-guest-token header set, we need to request the target user's Rest ID via a
GET request. This occurs at ``` https://api.twitter.com/graphql/4S2ihIKfF3xhp-ENxvUAfQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22   <username>  %22%2C%22withHighlightedLabel%22%3Atrue%7D```

### Step 4:
I learned this when trying to find out how the web application worked through burp, assessing 
which requests were sent before we get the user's twitter posts.
Pull the user's tweets via ```GET /2/timeline/profile/[user rest ID].json```  with the user's user rest id with Authorization and x-guest-token

The below request is an example request which obtains the user's tweets after the previous steps are carried out. 

```
GET /i/api/2/timeline/profile/25073877.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&include_tweet_replies=false&count=20&userId=25073877&ext=mediaStats%2ChighlightedLabel HTTP/1.1
Host: twitter.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
x-twitter-auth-type: OAuth2Session
x-twitter-client-language: en
x-twitter-active-user: yes
x-csrf-token: 338a64655eecabf29976439b4834746d261e2ec3a68c9469ce3808c83dda902655bc0bb6403b4b464dc500a7f2b8a0b381e49087dee0e6bccb6e1367fa8f37f7dd8a38be97529cb5dc31a74ec036aa57
authorization: Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA
Referer: https://twitter.com/realDonaldTrump
Connection: close
Cookie: personalization_id="v1_Pt8mS7teXxdsjVy50azQJQ=="; guest_id=v1%3A160552780587694624; _ga=GA1.2.956912678.1605527808; _gid=GA1.2.409404576.1608105321; external_referer=8e8t2xd8A2w%3D|0|ziZgIoZIK4nlMKUVLq9KcnBFms0d9TqBqrE%2FyjvSFlFJR45yIlYF%2Bw%3D%3D; mbox=PC#cfa28451d86a4973aac2072bf7d8dab0.36_0#1671363095|session#6b9c5b5c900c4342ae4bca66daa6f7ec#1608119696; at_check=true; cd_user_id=1766ac3b8f5120-0236e1d2e9ebfd8-30634644-1fa400-1766ac3b8f6326; __utma=43838368.956912678.1605527808.1608114933.1608114933.1; __utmc=43838368; __utmz=43838368.1608114933.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ct0=338a64655eecabf29976439b4834746d261e2ec3a68c9469ce3808c83dda902655bc0bb6403b4b464dc500a7f2b8a0b381e49087dee0e6bccb6e1367fa8f37f7dd8a38be97529cb5dc31a74ec036aa57; _twitter_sess=BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCJOr4m92AToMY3NyZl9p%250AZCIlZjFlNTQyMTZhMjU5NWRjNDRmZWIyN2NiZGRmZWY4Y2Q6B2lkIiU5ODc1%250AM2M4OTEzMWYyMjBkYTA3MDZmMDE3ZmU2MzA0NDoJdXNlcmwrCQDA1B65TJgL--57599b72805862084b2cede96e1420490f0947d9; ads_prefs="HBERAAA="; kdt=qWYgddl7aOhoG3M0I0CtjisDotcs5lAvkkCYADPG; remember_checked_on=1; twid=u%3D835502088847147008; auth_token=725794f522f9183821d32bb0d14ba222faa0f9e1; lang=en
```

Sample Response:

```
HTTP/1.1 200 OK
cache-control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0
connection: close
content-disposition: attachment; filename=json.json
Content-Length: 149668
content-type: application/json;charset=utf-8
date: Fri, 18 Dec 2020 07:32:48 GMT
expires: Tue, 31 Mar 1981 05:00:00 GMT
last-modified: Fri, 18 Dec 2020 07:32:48 GMT
pragma: no-cache
server: tsa_l
status: 200 OK
strict-transport-security: max-age=631138519
x-access-level: read-write-directmessages
x-client-event-enabled: true
x-connection-hash: a2c7bbad01c692b558ab406060529874
x-content-type-options: nosniff
x-frame-options: SAMEORIGIN
x-rate-limit-limit: 180
x-rate-limit-remaining: 177
x-rate-limit-reset: 1608277623
x-response-time: 539
x-transaction: 00b4ba09004495b8
x-twitter-response-tags: BouncerCompliant
x-xss-protection: 0

{"globalObjects":{"tweets":{"1339594787133919239":{"created_at":"Thu Dec 17 15:34:20 +0000 2020","id_str":"1339594787133919239","full_text":"I will Veto the Defense Bill, which will make China very unhappy. They love it. Must have Section 230 termination, protect our National Monuments and allow for removal of military from far away, and very unappreciative, lands. Thank you!","display_text_range":[0,237],"entities":{},"source":"\u003ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003eTwitter for iPhone\u003c\/a\u003e","user_id_str":"25073877","is_quote_status":true,"quoted_status_id_str":"1339046341054521347","quoted_status_permalink":{"url":"https:\/\/t.co\/9rI08S5ofO","expanded":"https:\/\/twitter.com\/dailycaller\/status\/1339046341054521347","display":"twitter.com\/dailycaller\/st\u2026"},"retweet_count":39688,"favorite_count":165183,"reply_count":20621,"quote_count":3253,"conversation_id_str":"1339594787133919239","lang":"en"},
```
=========================================== SNIP ===========================================


I thought hashing was the best approach to take because I thought it was a flawless way of telling of any additional posts had
been added to the data structure. If the hash is the same, move on nothing has been changed and out put "No tweets to report". However, if the hashes of both old tweets and new tweets by current refresh are different - this essentially means that a post
has been changed somehow and we need to identify if a post was added or removed. 

If I had a bit more time, I'd try and figure out which posts were removed and return an output something like:
```
[Timestamp]
Posts Removed: 
time of post
text
username 
\n
```


## Timestamps
Basically, I took the date time and formatted it with the datetime library. I decided to use an integer because
I thought it would be much easier to sort later down the track when pulling the top five tweets. 

Datetime object: 
```
{'id': '1014548680077074432', 'date_created': datetime.datetime(2018, 7, 4, 16, 37, 9), 'text': 'CRYP70 just owned system on DevOops ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}
```


Actual timestamp it came from: 
```
{'id': '1014548680077074432', 'date_created': 'Wed Jul 04 16:37:09 2018', 'text': 'CRYP70 just owned system on DevOops ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}
```


Sample response of sorting by timestamp:
```
[{'id': '1140919895347093504', 'timestamp': 1560865874, 'date_created': 'Tue Jun 18 09:51:14 +0000 2019', 'text': 'Man.  A ton of my videos decided to go limited ads... again.  Really getting tired of having to submit videos for m… https://t.co/xktZUOFnkl'}, {'id': '1014539244184973312', 'timestamp': 1530734379, 'date_created': 'Wed Jul 04 15:59:39 +0000 2018', 'text': 'CRYP70 just owned system on Valentine ! https://t.co/0Tr9DSk7cz via @hackthebox_eu'}, {'id': '1135200093110333441', 'timestamp': 1559502167, 'date_created': 'Sun Jun 02 15:02:47 +0000 2019', 'text': 'RT @MalwareTechBlog: All the people posting fake/troll PoCs on github have basically made it impossible to find the real ones, unless you h…'}, {'id': '1087518797785849856', 'timestamp': 1548137661, 'date_created': 'Tue Jan 22 01:14:21 +0000 2019', 'text': 'Thank you so much @offsectraining for world class training..the definition of what personal achievement feels like.… https://t.co/9orUAcx0QM'}, {'id': '1049644658257739776', 'timestamp': 1539104162, 'date_created': 'Tue Oct 09 12:56:02 +0000 2018', 'text': 'RT @darrenpauli: Speaking with a few #CySCA2018 teams while snapping pics. Loads of players from non-sec fields: commerce, human resources,…'}, {'id': '1019836128617160704', 'timestamp': 1531997255, 'date_created': 'Thu Jul 19 06:47:35 +0000 2018', 'text': 'CRYP70 just owned system on Blue ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}, {'id': '1017025074019176449', 'timestamp': 1531327047, 'date_created': 'Wed Jul 11 12:37:27 +0000 2018', 'text': 'RT @OhExFortyOne: https://t.co/lQb4PJQTGw\n\nFinal #kioptrix series #boot2root write up done! This one is a walkthrough of the fifth and fina…'}, {'id': '1049502415056060416', 'timestamp': 1539070249, 'date_created': 'Tue Oct 09 03:30:49 +0000 2018', 'text': 'Speaking with a few #CySCA2018 teams while snapping pics. Loads of players from non-sec fields: commerce, human res… https://t.co/zxQWixdEgY'}, {'id': '1176174627757776896', 'timestamp': 1569271258, 'date_created': 'Mon Sep 23 16:40:58 +0000 2019', 'text': 'So just..so Noble keeping them ad free https://t.co/9TfFC0Qd5G'}, {'id': '1057151217304915968', 'timestamp': 1540893865, 'date_created': 'Tue Oct 30 06:04:25 +0000 2018', 'text': 'Michael Murphy discusses security operations with AI-guided comprehension. #MPOWER18 https://t.co/sIfUfrqQbT'}, {'id': '1019836089861791744', 'timestamp': 1531997246, 'date_created': 'Thu Jul 19 06:47:26 +0000 2018', 'text': 'CRYP70 just owned user on Blue ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}, {'id': '1019697211775508480', 'timestamp': 1531964135, 'date_created': 'Wed Jul 18 21:35:35 +0000 2018', 'text': 'CRYP70 just owned system on Sunday ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}, {'id': '954825558873001985', 'timestamp': 1516501127, 'date_created': 'Sat Jan 20 21:18:47 +0000 2018', 'text': 'https://t.co/lQb4PJQTGw\n\nFinal #kioptrix series #boot2root write up done! This one is a walkthrough of the fifth an… https://t.co/3eMIO3LnG6'}, {'id': '1090601326961016832', 'timestamp': 1548872593, 'date_created': 'Wed Jan 30 13:23:13 +0000 2019', 'text': 'Really love the marketing @offsectraining  does. Their certificates have always look immaculate. #oscp… https://t.co/oOcf8g1otH'}, {'id': '1057303685015920640', 'timestamp': 1540930216, 'date_created': 'Tue Oct 30 16:10:16 +0000 2018', 'text': 'RT @McAfee: Michael Murphy discusses security operations with AI-guided comprehension. #MPOWER18 https://t.co/sIfUfrqQbT'}, {'id': '1063824000709648384', 'timestamp': 1542488381, 'date_created': 'Sat Nov 17 15:59:41 +0000 2018', 'text': 'When my mom asks me what operating system I am using... again!\n\n@kalilinux #infosec https://t.co/YU4SMyEaYW'}, {'id': '1016992244455260160', 'timestamp': 1531319220, 'date_created': 'Wed Jul 11 10:27:00 +0000 2018', 'text': 'I don’t usually break boxes on vulnhub, I’m more of a @hackthebox_eu user but I wanna thank @loneferret for your… https://t.co/UEea9sNmlH'}, {'id': '1339502960192102401', 'timestamp': 1608215367, 'date_created': 'Thu Dec 17 09:29:27 +0000 2020', 'text': 'another test'}, {'id': '1339506731383078913', 'timestamp': 1608216266, 'date_created': 'Thu Dec 17 09:44:26 +0000 2020', 'text': 'test'}, {'id': '1134143172815142912', 'timestamp': 1559250178, 'date_created': 'Thu May 30 17:02:58 +0000 2019', 'text': 'All the people posting fake/troll PoCs on github have basically made it impossible to find the real ones, unless yo… https://t.co/fApBcPYUB3'}, {'id': '1339503080908279811', 'timestamp': 1608215395, 'date_created': 'Thu Dec 17 09:29:55 +0000 2020', 'text': 'just another test for a python application im writing, dont mind me!'}, {'id': '1019697169337470976', 'timestamp': 1531964124, 'date_created': 'Wed Jul 18 21:35:24 +0000 2018', 'text': 'CRYP70 just owned user on Sunday ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}, {'id': '1064079457483255808', 'timestamp': 1542549286, 'date_created': 'Sun Nov 18 08:54:46 +0000 2018', 'text': 'Just wanted to thank the @offsectraining  online staff who assisted me with my technical issues. Problem was quickl… https://t.co/thFQlGz3Kf'}, {'id': '1064192198185340929', 'timestamp': 1542576166, 'date_created': 'Sun Nov 18 16:22:46 +0000 2018', 'text': 'RT @joshjaycomedy: When my mom asks me what operating system I am using... again!\n\n@kalilinux #infosec https://t.co/YU4SMyEaYW'}, {'id': '1087954903039918086', 'timestamp': 1548241636, 'date_created': 'Wed Jan 23 06:07:16 +0000 2019', 'text': 'https://t.co/51C8oURGLS'}, {'id': '1014548680077074432', 'timestamp': 1530736629, 'date_created': 'Wed Jul 04 16:37:09 +0000 2018', 'text': 'CRYP70 just owned system on DevOops ! https://t.co/0Tr9DSBI47 via @hackthebox_eu'}]
```


## API 
API ticket was quite rushed and needs some cleaning but because of how time sensitive this project is, I was rushing the bonus content :/

Essentially, since I've done a bit of work with swagger - because of it's presentation and customizability I thought this was the best path to take. I set up the skeleton through flask and imported the functionality of obtaining the latest tweets for a user when a POST request is sent (Interacting with the server itself, as opposed to GET when you're just fetching a resource). 
Given a username, the latest tweets are returned for that user. 


## USAGE

### Monitor for user: 
```
python3 app.py [Twitter Username]
```
### API spin up: 
```
python3 api.py
```
The API should appear at http://127.0.0.1/


## API:

Once the api is started, a simple curl command can be used to obtain the latest tweets:

```
curl -X POST "http://localhost/twitcrawler?username=cryp70_" -H  "accept: application/json"
```



Sample output:
```
{
  "cryp70_": [
    {
      "id": "1339511587120410630",
      "timestamp": 1608217423,
      "date_created": "Thu Dec 17 10:03:43 +0000 2020",
      "text": "test"
    },
    {
      "id": "1339503080908279811",
      "timestamp": 1608215395,
      "date_created": "Thu Dec 17 09:29:55 +0000 2020",
      "text": "just another test for a python application im writing, dont mind me!"
    },
    {
      "id": "1339502960192102401",
      "timestamp": 1608215367,
      "date_created": "Thu Dec 17 09:29:27 +0000 2020",
      "text": "another test"
    },
    {
      "id": "1176174627757776896",
      "timestamp": 1569271258,
      "date_created": "Mon Sep 23 16:40:58 +0000 2019",
      "text": "So just..so Noble keeping them ad free https://t.co/9TfFC0Qd5G"
    },
=========================================== SNIP ===========================================
```


## DOCKER

Building the image:
```
docker build -t [Image tag] .
```

Running on commandline to obtain monitoring for specific user:
```
docker run -it [Image tag] realDonaldTrump
```



I had some trouble trying to get the api working simultaneously with my std output solution, that being said
I could only get either the API or the App itself to work through docker.

If I changed the entry point in the docker file to:
```
ENTRYPOINT ["python3", "api.py"]
```
This would allow me to run as an API. I tried multithreading in python and a separate bash script to start the flask server on another thread, but the output of swagger is still ran in the foreground. 

When the container is ran, the api webserver is up after running:
```
docker run -p 80:80 -it [Image tag]
```

Just before this submission I was thinking of using docker composer to run two simultaneous containers.
One for the API and one for the App itself.


## Bugs found:
Late in the night before the app was submitted, I was doing a bit of testing for abormalities and found that there is a bug 
where if a user adds a post - it appears in stdout just fine. However when the user deletes that post, one of the older posts 
(at least on my profile) is displayed. I added a ticket but never got the chance to fix it.

I tried a few solutions to try and fix the bug, like reversing the functionality where I left the comment, iterated throught the 
old tweets and the new tweets, and if in the new tweets (the tweets which are about to be returned as the latest tweets) are already
in the old tweets data structure, print the same as if there were no new tweets to report. But the bug was still present. Do let me know if there's a better solution! 









