from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query
import datetime
import os
import json

# * Import env variables
AWS_DB_ENDPOINT = os.getenv("AWS_DB_ENDPOINT")
AWS_DB_USERNAME = os.getenv("AWS_DB_USERNAME")
AWS_DB_PASSWORD = os.getenv("AWS_DB_PASSWORD")
AWS_DB_NAME = os.getenv("AWS_DB_NAME")
AWS_DB_PORT = os.getenv("AWS_DB_PORT")

# * Connect to database
engine = create_engine(f"postgresql://{AWS_DB_USERNAME}:{AWS_DB_PASSWORD}@{AWS_DB_ENDPOINT}/{AWS_DB_NAME}")
Base = declarative_base()

# * Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


# *  Table schema
class SentimentScores(Base):
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True)
    sentiment_score = Column(Float)
    sentiment = Column(String)
    date_added = Column(Date)
    character_id = Column(Integer, ForeignKey("characters.id"))


def get_score_by_character_id_from_db(character_id):
    """
    Get all character_id scores from RDS using character ID
    """
    sentiment_scores = session.query(SentimentScores).filter(SentimentScores.character_id == character_id).all()
    return sentiment_scores


def handler(event, context):
    """
    Grab character id from path parameter and invoke get_score_by_character_id_from_db
    """
    # * Access character_id from the path parameter
    path_parameter = event["pathParameters"]
    character_id = int(path_parameter.get("character_id"))

    # * Get character scores
    character_scores = get_score_by_character_id_from_db(character_id)

    # * Create dict to show all scores associated with character id
    character_data = {}
    for score in character_scores:
        character_data[f"{score.id}"] = {"date":  score.date_added.strftime("%Y-%m-%d"), "sentiment": score.sentiment, "score":score.sentiment_score}

    # * Convert character info into json
    json_character_data = json.dumps(character_data)
    response = {
        "statusCode": 200,
        "body": f"{json_character_data}"
    }
    return response
