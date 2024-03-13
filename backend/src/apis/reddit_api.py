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
    config.read("config.ini")
    print("cur dir: ", os.getcwd())
    print(config["Reddit_creds"])
except Exception as e:
    print("exception : ", e)

# Initialize sentiment analysis Instance 
analyzer = SentimentIntensityAnalyzer()

# Create Reddit instance
reddit = praw.Reddit(
    client_id=f"{config['Reddit_creds']['client_id']}",
    client_secret=f"{config['Reddit_creds']['client_secret']}",
    user_agent=f"{config['Reddit_creds']['user_agent']}",
)


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
def character_sentiment(sentiment_scores) -> list:
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
    score = {"average_score": average_score, "sentiment": None, "character_id": None}
    if average_score > 0:
        score["sentiment"] = "positive"
    elif average_score < 0:
        score["sentiment"] ="negative"
    else:
        score["sentiment"] = "neutral"
    return score
#     ! Any benefit in changing this to an object


# get character sentiment score of today
def get_character_sentiment_score_today(character):
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


def main():
    character = "luffy"
    #  Search subreddit for a specific character submission on the current day
    print(character)
    sentiment = get_character_sentiment_score_today(character)
    print(f"TADA: {sentiment}")


if __name__ == "__main__":
    main()
