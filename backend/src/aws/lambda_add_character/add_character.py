from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, query
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

# Create table schema if not already added
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

def handler(event, context):
    """
    Grab character to add from json body and invoke add_character_to_db.
    """
    body_str = event["body"]

    # Parse the JSON body
    body = json.loads(body_str)
    # Access specific fields from the body
    character = body.get("character")
    response = {
        "statusCode": 200,
        "body": f" {character}"
    }
    return response