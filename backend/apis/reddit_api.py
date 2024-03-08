import praw
import configparser
import statistics
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import config values
config = configparser.ConfigParser()
config.read("../config.ini")


reddit = praw.Reddit(
    # username=f"${config['Reddit_creds']['username']}",
    # password=f"${config['Reddit_creds']['password']}",
    client_id=f"{config['Reddit_creds']['client_id']}",
    client_secret=f"{config['Reddit_creds']['client_secret']}",
    user_agent=f"{config['Reddit_creds']['user_agent']}",
)
analyzer = SentimentIntensityAnalyzer()
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
  subreddit = "OnePiece"
  character = "luffy"
  content = []
  score = []
#  search subreddit for a specific character submission on the current day
  for submission in reddit.subreddit(subreddit).search(query=character, sort="hot",time_filter="day",syntax="plain"):
        print(f"**{submission.title}**\n")
        # contents of the post
        content.append(submission.selftext)
        

  for post in content:
      vs = analyzer.polarity_scores(post)
      score.append(vs["compound"])
  print(f"Number of posts:{len(score)}")
  print(f"THIS ARE THE OG SCORES{(score)}")
  print(f"{character} Sentiment: {character_sentiment(score)}")
      

  

  
        

if __name__ == '__main__':
    main()
