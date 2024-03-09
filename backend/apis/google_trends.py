from pytrends.request import TrendReq
import pandas as pd

# stop empty values  from being changed to more specific dtype
pd.set_option('future.no_silent_downcasting', True)

# Interface to access Google Trends
pytrends = TrendReq(hl='en-US')

#  Search term list
kw_list = ['Luffy']

#  Query Google Trends
pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')

# Get related topics
character_related_topics = pytrends.related_topics()

# Print only the topic titles in order of rising popularity
print(character_related_topics["Luffy"]["rising"]["topic_title"])

