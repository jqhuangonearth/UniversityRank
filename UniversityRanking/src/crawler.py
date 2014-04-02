"""
@author: Bolun
"""


API_KEY = "75erqo7zk5kx13"
API_SECRET = "Ujr0cUJzSLksRBAB"

USER_TOKEN = "161abd2a-1065-4817-80f3-c5fdcac58d8b"
USER_SECRET = "e5ec9937-9cd7-4d31-b93d-bb8bfab3406f"

import oauth2 as oauth
import cjson
import json
import time
import logging
import sys


wait_seconds = 86400

class crawler:
    def __init__(self):
        self.univ_list = self.read_file("../data/universities.txt")
        self.features = ["id","first-name","last-name","headline","location",
                         "industry","num-connections","summary","specialties", 
                         "relation-to-viewer"]
        
        self.consumer = oauth.Consumer(
                                 key=API_KEY,
                                 secret=API_SECRET)     
        self.token = oauth.Token(
                             key=USER_TOKEN, 
                             secret=USER_SECRET)
        self.client = oauth.Client(self.consumer, self.token)
        
    def read_file(self, filename):
        """
        @description: read file
        
        @param filename: file path and name
        @type filename: string
        """
        univ_list = []
        f = open(filename, "r")
        for line in f:
            univ_list.append(line.lower().strip("\r\n"))
        f.close()
        return univ_list
    
    def crawl(self):
        """
        @description: crawl the public profile of search results
        
        @return: the result dictionary {id:{profile}}
        """
        t_res = {}
        for val in self.univ_list:
            keywords = self.construct_keywords(title = "professor", companies_name = val)
            print keywords
            start = 0
            count = 25
            f_res = {} # final result for this request
            while True:
                res, total, count, start = self.search(self.features, keywords, start, count)
                if total == count + start:
                    f_res.update(res)
                    break
                else:
                    f_res.update(res)
                    start += count # update the start index of search result
            print str(len(f_res))+"\n"
            t_res.update(f_res)
        print "\n"+"total num of users: "+str(len(t_res))+"\n"
        return t_res
        
    def search(self, features = [], keywords = [], start = 0, count = 25):
        """
        @description: send search profile url request
        
        @param features: set of selectors to be returned
        @type features: list
        
        @param keywords: set of keywords for search
        @type keywords: list
        
        @param start: start index of result set
        @type start: integer
        
        @param count: number of results returned; default as 25
        @type count: integer
        """
        url = self.construct_search_url(self.features, keywords, start, count)
        result = {}
        newstart = start
        newcount = count
        total = start+count
        resp, content = self.client.request(url) # fetch!!
        if resp["status"] == '200':
            result, total, newcount, newstart = self.get_results(content)
        elif resp["status"] == '403':
            print "sleeping for 86400 seconds..."
            time.sleep(wait_seconds)
            resp, content = self.client.request(url) # fetch again
            result, total, newcount, newstart = self.get_results(content)
        return result, total, newcount, newstart
    
            
    def construct_search_url(self, features = ["id", "first-name", "last-name", "public-profile-url"], keywords = [], start = 0, count = 25):
        """
        @description: construct the http request url
        
        @param features: set of selectors to be returned
        @type features: list
        
        @param keywords: set of keywords for search
        @type keywords: list
        
        @param start: start index of result set
        @type start: integer
        
        @param count: number of results returned; default as 25
        @type count: integer
        """
        
        url1 = "http://api.linkedin.com/v1/people-search:(people:("
        url2 = ""
        for i in range(len(features)):
            if i == 0:
                url2 += features[i]
            else:
                url2 += ","+features[i]
        url3 = "),num-results)?keywords="
        url4 = ""
        for i in range(len(keywords)):
            if i == 0:
                url4 += keywords[i]
            else:
                url4 += "%20"+keywords[i]
        url5 = "&format=json"
        url6 = "&start=%d&count=%d" %(start, count)
        return url1+url2+url3+url4+url5+url6
    
    def get_results(self, content = ""):
        """
        @description: parse the result
        
        @return: r_res: result set
        @return: total number of results
        @return: number of results in this request
        @return: starting index of this request
        """
        r_res = {}
        res = cjson.decode(content)
        persons = res["people"]["values"]
        for person in persons:
            r_res.update({person["id"] : person})
        print res["people"]["_total"], res["people"]["_count"], res["people"]["_start"]
        return r_res, res["people"]["_total"], res["people"]["_count"], res["people"]["_start"]
        
        
    def construct_keywords(self, title = "", companies_name = ""):
        """
        @description: generate a list of keywords combining <title> and <company_name>
        
        @return: set of keywords
        """
        keywords = []
        titles = title.split(" ")
        for title in titles:
            if not title == "":
                keywords.append(title)
        companies_names = companies_name.split(" ")
        for company in companies_names:
            if not company == "":
                keywords.append(company)
        return keywords

def main():
#     logging.basicConfig(filename="crawler_log")
#     root = logging.getLogger()
# 
#     ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     ch.setFormatter(formatter)
#     root.addHandler(ch)
    sys.stdout = open('out', 'w')
    c = crawler()
    result = c.crawl()
    fp = open("../data/crawled_data.json","w")
    json.dump(result, fp)
    fp.close()
      
if __name__ == "__main__":
    main()