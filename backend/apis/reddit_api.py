import praw
import configparser
import statistics
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import config values
config = configparser.ConfigParser()
config.read("../config.ini")
print(f"\n{config['Reddit_creds']['client_id']}")

# Initialize sentiment analysis Instance 
analyzer = SentimentIntensityAnalyzer()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=f"{config['Reddit_creds']['client_id']}",
    client_secret=f"{config['Reddit_creds']['client_secret']}",
    user_agent=f"{config['Reddit_creds']['user_agent']}",
)


def character_scores(character_name):
  subreddit = "OnePiece"
  content = []
  score = []
  # search all posts of specified character and append the content of post to an array
  for submission in reddit.subreddit(subreddit).search(query=character_name, sort="hot",time_filter="day",syntax="plain"):
      print(f"**{submission.title}**\n")
      # contents of the post
      content.append(submission.selftext)
  # calculate sentiment score for every post
  for post in content:
      vs = analyzer.polarity_scores(post)
      score.append(vs["compound"])
  return score
  
def character_sentiment(sentiment_scores):
  average_score = statistics.mean(sentiment_scores)
  print(f'average score:{average_score}')
  if average_score > 0:
    return "positive"
  elif average_score < 0:
    return "negative"
  else:
    return "neutral"
      
def main():
  character = "luffy"
#  search subreddit for a specific character submission on the current day
  scores = character_scores(character)
  print(f"THIS ARE ALL THE POST SCORES{scores}")
  print(f"{character} Sentiment: {character_sentiment(scores)}")
      

  

  
        

if __name__ == '__main__':
    main()
