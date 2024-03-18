import os
from dotenv import load_dotenv
import statistics
# wrapper for reddit API
import praw
# NLP library
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json

# Load environment variables from .env file
load_dotenv("./config.env")

# Access the environment variable
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')

# Initialize sentiment analysis Instance
analyzer = SentimentIntensityAnalyzer()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


# # TODO use character ID to
def get_yesterday_character_posts(character_name) -> list:
    """
    Queries OnePiece subreddit for all posts related to character_name in the last 24 hours using the reddit api
    Args:
      character_name (str): character name
    Returns:
      list: all reddit posts found in the last 24 hours
    """
    subreddit = "OnePiece"
    post_list = []
    # search all posts related to the specified character and append them to post_list
    for submission in reddit.subreddit(subreddit).search(query=character_name, sort="hot", time_filter="day",
                                                         syntax="plain"):
        print(f"**{submission.title}**\n")
        post_list.append(submission.selftext)
    return post_list


def calculate_sentiment_score(post_content) -> list:
    """
    Calculates sentiment score for every string item in the list [post_content]
    Args:
      post_content (list): list of strings/reddit posts
    Returns:
      list: all reddit posts found in the last 24 hours
    """
    scores = []
    # Calculate sentiment score for every post
    for post in post_content:
        vs = analyzer.polarity_scores(post)
        scores.append(vs["compound"])
    return scores


# get average character sentiment based on list of sentiment scores
def character_sentiment(sentiment_scores) -> dict:
    """
    Averages out a list of sentiment scores and assigns it one of 3 sentiment negative[<0], neutral[0], or positive[>0]
    Args:
      sentiment_scores (list): list of sentiment scores
    Returns:
      dictionary: the average sentiment score and one of the 3 sentiments:
            negative[<0], neutral[0], or positive[>0] based on average score
    """
    average_score = statistics.mean(sentiment_scores)
    print(f"average score:{average_score}")
    score = {"average_score": average_score, "sentiment": None}
    if average_score > 0:
        score["sentiment"] = "positive"
    elif average_score < 0:
        score["sentiment"] = "negative"
    else:
        score["sentiment"] = "neutral"
    return score


# get character sentiment score of today
def get_character_sentiment_score_today(character) -> dict:
    """
    Gets sentiment score and sentiment of specified character
    Args:
      character (string): character name
    Returns:
      list: the average sentiment score and one of the 3 sentiments:
            negative[<0], neutral[0], or positive[>0] based on average score
    """
    reddit_posts = get_yesterday_character_posts(character)
    print(f"-------\nTHESE ARE ALL THE REDDIT POSTS\n{reddit_posts}")
    sentiment_scores = calculate_sentiment_score(reddit_posts)
    print(f"-------\nTHESE ARE ALL THE POST SCORES\n{sentiment_scores}")
    sentiment = character_sentiment(sentiment_scores)
    return sentiment


def handler(event, context):
    body_str = event['body']

    # Parse the JSON body
    body = json.loads(body_str)

    # Access specific fields from the body
    character = body.get('character')
    #  Search subreddit for a specific character submission on the current day
    sentiment = get_character_sentiment_score_today(character)
    response = {
        "statusCode": 200,
        "body": f"{character}"
    }
