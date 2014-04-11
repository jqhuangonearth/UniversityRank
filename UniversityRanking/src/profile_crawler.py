"""
@description: crawl the full profiles of given users
@author: Bolun Huang
"""

from linkedin import linkedin
import cjson
import json

API_KEY = "75erqo7zk5kx13"
API_SECRET = "Ujr0cUJzSLksRBAB"

USER_TOKEN = "161abd2a-1065-4817-80f3-c5fdcac58d8b"
USER_SECRET = "e5ec9937-9cd7-4d31-b93d-bb8bfab3406f"
RETURN_URL = 'http://localhost:8000'

authentication = linkedin.LinkedInDeveloperAuthentication(API_KEY, API_SECRET, 
                                                      USER_TOKEN, USER_SECRET, 
                                                      RETURN_URL)

application = linkedin.LinkedInApplication(authentication)

profile = application.get_profile(selectors = ['id', 'first-name', 'last-name', 'location',
                                                 'distance', 'skills', 'educations','industry', 'positions',
                                                 'num-connections','summary', 'specialties', 'connections',
                                                 'public-profile-url'])
print cjson.encode(profile)
exit(0)
f = open("../data/profiles_sample_2.json","w")

search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations','positions','connections']}], 
                                    params={'keywords' : 'Professor'})
print search

# 
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 0, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 10, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 20, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 30, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 40, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# search = application.search_profile(selectors=[{'people': ['first-name', 'last-name','public-profile-url','educations']}], 
#                                      params={'keywords': 'professor computer science University of Texas, Austin', 'start' : 50, 'count' : 10})
# print len(search['people']['values'])
# json.dump(search, f)
# f.write("\n")
# 
# f.close()