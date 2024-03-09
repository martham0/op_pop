import configparser
import statistics
import os
# wrapper for reddit API
import praw
# NLP library 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Import config values
config = configparser.ConfigParser()
db_url = os.environ.get("DB_URL_LOCAL")
print(f"____{db_url}_______")

# getting path to config

try:
    config.read("../config.ini")
    print("cur dir: ", os.getcwd())
    print(config['Reddit_creds'])
except Exception as e:
    print('exception : ', e)

# Initialize sentiment analysis Instance 
analyzer = SentimentIntensityAnalyzer()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=f"{config['Reddit_creds']['client_id']}",
    client_secret=f"{config['Reddit_creds']['client_secret']}",
    user_agent=f"{config['Reddit_creds']['user_agent']}",
)
def get_yesterdays_character_posts(character_name) -> list:
    """
  queries reddit api given character_name 

  Args:
      character_name (str): character name
  Returns:
      array: an array of reddit posts
  """
    subreddit = "OnePiece"
    post_list = []
    # search all posts related to the specified character and append thm to post_list
    for submission in reddit.subreddit(subreddit).search(query=character_name, sort="hot", time_filter="day",
                                                         syntax="plain"):
        print(f"**{submission.title}**\n")
        # add post to the list
        post_list.append(submission.selftext)
    return post_list


def character_scores(post_content):
    score = []
    # calculate sentiment score for every post
    for post in post_content:
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
    print(character)
    scores = character_scores(character)
    print(f"THIS ARE ALL THE POST SCORES{scores}")
    print(f"{character} Sentiment: {character_sentiment(scores)}")


if __name__ == '__main__':
    main()
