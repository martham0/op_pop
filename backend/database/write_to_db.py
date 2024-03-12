from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime
import configparser

# import configs
config = configparser.ConfigParser()
config.read("config.ini")
db_url = ["Database"]["url"]

# connect to DB
engine = create_engine(db_url)
Base = declarative_base()

# * Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


def add_character_to_db(character_name, picture_link=""):
    """
    Add character to postgress characters table
    """
    new_character = Characters(full_name=character_name, date_added=datetime.date.today(),
                               picture_link=picture_link)
    session.add(new_character)
    session.commit()


def add_sentiment_score_to_character(score):
    """
    Add sentiment score to sentiment_scores table

    """
    new_sentiment_score = SentimentScores(sentiment_score=score["average_score"], sentiment=score["sentiment"], character_Id=score['character_id'], date_added=datetime.date.today())
    session.add(new_sentiment_score)
    session.commit()
