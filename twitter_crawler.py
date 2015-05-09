#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re
from bs4 import BeautifulSoup
import datetime
import csv
import os


class Sel(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        # kodadıkoz https://twitter.com/search?f=realtime&q=%23kodad%C4%B1koz%20since%3A2015-02-06%20until%3A2015-02-20&src=typd
        # kodadikoz https://twitter.com/search?f=realtime&q=%23kodadikoz%20since%3A2015-02-06%20until%3A2015-02-20&src=typd
        # kodadıkoz13şubattavizyonda https://twitter.com/search?f=realtime&q=%23kodad%C4%B1koz13%C5%9Fubattavizyonda%20since%3A2015-02-06%20until%3A2015-02-20&src=typd

        # banamasalanlatma https://twitter.com/search?f=realtime&q=%23banamasalanlatma%20since%3A2015-01-02%20until%3A2015-01-16&src=typd

        # icimdekises https://twitter.com/search?f=realtime&q=%23icimdekises%20since%3A2015-01-23%20until%3A2015-02-06&src=typd
        # içimdekises https://twitter.com/search?f=realtime&q=%23içimdekises%20since%3A2015-01-23%20until%3A2015-02-06&src=typd

        # selambaharayolculuk https://twitter.com/search?f=realtime&q=%23selambaharayolculuk%20since%3A2015-03-06%20until%3A2015-03-20&src=typd
        # baharayolculuk https://twitter.com/search?f=realtime&q=%23baharayolculuk%20since%3A2015-03-06%20until%3A2015-03-20&src=typd
        # selam2

        self.url = 'https://twitter.com/search?f=realtime&q=%23selam2%20since%3A2015-03-06%20until%3A2015-03-20&src=typd'
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_sel(self):
        driver = self.driver
        delay = 3
        driver.get(self.url)
        # driver.find_element_by_link_text("All").click()
        data=""
        f = csv.writer(open("selam2.csv", "w"))
        f.writerow(["Name", "Date", "Text", "Retweet", "Fav"])    # Write column headers as the first line
        for i in range(1, 20):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        soup = BeautifulSoup(data)
        # print(soup.prettify())
        # print data
        tweets = soup.find_all('li', 'js-stream-item')
        tweet_text = soup.find_all('p', {'class': 'js-tweet-text'})
        tweet_timestamps = soup.find_all('a', 'tweet-timestamp')
        names = soup.find_all('a', 'account-group js-account-group js-action-profile js-user-profile-link js-nav')
        retweets = soup.find_all('div', 'ProfileTweet-action ProfileTweet-action--retweet js-toggleState js-toggleRt')
        favs = soup.find_all('div', 'ProfileTweet-action ProfileTweet-action--favorite js-toggleState')
        print tweets
        for j in range(0, len(tweet_text)):
            name = names[j]['href']
            timestamp = datetime.datetime.strptime(tweet_timestamps[j]['title'], '%I:%M %p - %d %b %Y')
            text = tweet_text[j].get_text().encode('utf-8', 'ignore')
            new_text = text.replace('\n', '')
            retweet = retweets[j].get_text().encode('utf-8', 'ignore')
            new_rt = retweet.replace('\n', '')
            new_rt = new_rt[new_rt.index('Retweeted') + len('Retweeted'):]
            fav = favs[j].get_text().encode('utf-8', 'ignore')
            new_fav = fav.replace('\n', '')
            new_fav = new_fav[new_fav.index('Favorited') + len('Favorited'):]
            f.writerow([name, timestamp, new_text, new_rt, new_fav])
            # print name
            # print timestamp
            # print new_text

if __name__ == "__main__":
    unittest.main()
