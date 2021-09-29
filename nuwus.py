from bs4 import BeautifulSoup
import requests
import owo
import time
#from dotenv import dotenv_values
import tweepy
import os
 
headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
        }
 
class ReadRss:
 
    def __init__(self, rss_url, headers):
 
        self.url = rss_url
        self.headers = headers
        try:
            self.r = requests.get(rss_url, headers=self.headers)
            self.status_code = self.r.status_code
        except Exception as e:
            print('Error fetching the URL: ', rss_url)
            print(e)
        try:    
            self.soup = BeautifulSoup(self.r.text, 'lxml')
        except Exception as e:
            print('Could not parse the xml: ', self.url)
            print(e)
        self.articles = self.soup.findAll('item')
        self.articles_dicts = [{'title':a.find('title').text,'link':a.link.next_sibling.replace('\n','').replace('\t',''),'description':a.find('description').text,'pubdate':a.find('pubdate').text} for a in self.articles]
        self.urls = [d['link'] for d in self.articles_dicts if 'link' in d]
        self.titles = [d['title'] for d in self.articles_dicts if 'title' in d]
        self.descriptions = [d['description'] for d in self.articles_dicts if 'description' in d]
        self.pub_dates = [d['pubdate'] for d in self.articles_dicts if 'pubdate' in d]


if __name__ == "__main__":
    config = dotenv_values(".env")
    CONSUMER_KEY = os.getenv("CONSUMER_KEY")
    CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    feed = ''
    previous_url = ''
    while True:
        try:
            feed = ReadRss('https://www.abc.net.au/news/feed/51120/rss.xml', headers)
        except Exception as e:
            print(e)
        else:
            if(feed.urls):
                print(".") #Just to debug, doesn't do anything else
                if feed.urls[0].strip() != previous_url:
                    print(time.strftime("%H:%M:%S", time.localtime()))
                    text_to_tweet = owo.owo(feed.titles[0]) + " " + feed.urls[0].strip()
                    print(text_to_tweet)
                    api.update_status(text_to_tweet)
                    previous_url = feed.urls[0].strip()
            else:
                print("sumething iz wwong!")
        time.sleep(30)