API_KEY = "75erqo7zk5kx13"
API_SECRET = "Ujr0cUJzSLksRBAB"

USER_TOKEN = "161abd2a-1065-4817-80f3-c5fdcac58d8b"
USER_SECRET = "e5ec9937-9cd7-4d31-b93d-bb8bfab3406f"

import oauth2 as oauth
from linkedin import linkedin
import cjson
import json

wait_seconds = 86400

class crawler:
    def __init__(self):
        
    def contruct_url(self):
        
    def crawl(self):
        """"""


url_profile = "http://api.linkedin.com/v1/people/~?format=json"
url_search = "http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,public-profile-url,positions),num-results)?keywords=professor%20MIT&start=0&count=710&format=json"
url_search_2 = "http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,public-profile-url,positions),num-results)?keywords=professor%20massachusetts%20institute%20technology&start=0&count=710&format=json"

consumer = oauth.Consumer(
     key=API_KEY,
     secret=API_SECRET)
     
token = oauth.Token(
     key=USER_TOKEN, 
     secret=USER_SECRET)


client = oauth.Client(consumer, token)
# resp, content = client.request(url_profile)
# 
# print cjson.decode(content)

resp, content = client.request(url_search_2)
print "header: ", resp
print "content: ", cjson.decode(content)
f = open("../test_data/search_sample_mit_2.json","w")
json.dump(cjson.decode(content), f)
f.close()
