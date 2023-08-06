#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import snscrape.modules.twitter as sntwitter
import pandas as pd

class twitter():
  def __init__(self):
    pass
  def scrape(self,l1,n):
    self.l1=l1
    self.n=n
    df_list=[]
    for user in self.l1:
      tweets_list1 = []
      # Using TwitterSearchScraper to scrape data and append tweets to list
      for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"from:{user}").get_items()):  # declare a username
          if i > (self.n-1):  # number of tweets you want to scrape
              break
          tweets_list1.append(
              [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.likeCount, tweet.retweetCount, tweet.replyCount, tweet.quoteCount]
          )  # declare the attributes to be returned

      # Creating a dataframe from the tweets list above
      tweets_df1 = pd.DataFrame(
          tweets_list1, columns=["Datetime", "Tweet Id", "Text", "Username", "LikeCount", "RetweetCount", "ReplyCount", "QuoteCount"]
      )
      df_list.append(tweets_df1)
    return df_list

