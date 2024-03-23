from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os
import json

AWS_DB_ENDPOINT = os.getenv("AWS_DB_ENDPOINT")
AWS_DB_USERNAME = os.getenv("AWS_DB_USERNAME")
AWS_DB_PASSWORD = os.getenv("AWS_DB_PASSWORD")
AWS_DB_NAME = os.getenv("AWS_DB_NAME")
AWS_DB_PORT = os.getenv("AWS_DB_PORT")

# * Create the table in the database
engine = create_engine(f"postgresql://{AWS_DB_USERNAME}:{AWS_DB_PASSWORD}@{AWS_DB_ENDPOINT}/{AWS_DB_NAME}")
Base = declarative_base()

# * Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# * SentimentScores table schema
class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    picture_link = Column(String)


class SentimentScores(Base):
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True)
    sentiment_score = Column(Float)
    sentiment = Column(String)
    date_added = Column(Date)
    character_id = Column(Integer, ForeignKey("characters.id"))


# * Create the tables in the database
Base.metadata.create_all(engine)


def add_sentiment_score_to_character(score, sentiment, id):
    """
    Add sentiment score to sentiment_scores table

    """
    new_sentiment_score = SentimentScores(sentiment_score=score, sentiment=sentiment,
                                          character_id=id, date_added=datetime.date.today())
    session.add(new_sentiment_score)
    session.commit()
    return session.query(SentimentScores).order_by(desc(SentimentScores.id)).first()


def handler(event, context):
    """
    Grab character name from json body and invoke add_character_to_db
    """
    body_str = event["body"]

    # Parse the JSON string into a dictionary
    body = json.loads(body_str)

    # Access specific fields from the body
    score = body.get("score")
    sentiment = body.get("sentiment")
    character_id = body.get("character_id")
    new_score = add_sentiment_score_to_character(score, sentiment, character_id)

    score_data = {
        "id": new_score.id,
        "sentiment_score": new_score.sentiment_score,
        "sentiment": new_score.sentiment,
        "date_added": new_score.date_added,
        "character_id": new_score.character_id
    }

    # json_character_data = json.dumps(character_data)
    response = {
        "statusCode": 200,
        "body": f"score input:{score_data}\n"
    }
    return response
