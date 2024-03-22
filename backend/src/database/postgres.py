from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import datetime
import configparser

# * Import configs
config = configparser.ConfigParser()
config.read("config.ini")
db_url = config["Database"]["url"]

# * Create the table in the database
engine = create_engine(db_url)
Base = declarative_base()

# * Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    picture_link = Column(String)
    # num_searches = Column(Integer)


class SentimentScores(Base):
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True)
    sentiment_score = Column(Float)
    sentiment = Column(String)
    date_added = Column(Date)
    character_id = Column(Integer, ForeignKey("characters.id"))


# * Create the tables in the database
Base.metadata.create_all(engine)


def add_character_to_db(character_name, picture_link=""):
    """
    Add character to postgress characters table
    """
    new_character = Characters(full_name=character_name, date_added=datetime.date.today(),
                               picture_link=picture_link)
    session.add(new_character)
    session.commit()


def add_sentiment_score_to_character(score, sentiment, character_id):
    """
    Add sentiment score to sentiment_scores table

    """
    new_sentiment_score = SentimentScores(sentiment_score=score, sentiment=sentiment,
                                          character_id=character_id, date_added=datetime.date.today())
    session.add(new_sentiment_score)
    session.commit()


def get_character_by_id_from_db(character_id):
    character = session.get(Characters, character_id)
    return character


def get_top_sentiment_score_today():
    data = session.query(Characters).order_by(Characters.sentiment_score.desc()).limit(3).all()
    data = session.query(SentimentScores).order_by(SentimentScores.sentiment_score.desc()).limit(3).all()
    return data


def get_all_characters_from_db():
    data = session.query(Characters).all()
    return data
