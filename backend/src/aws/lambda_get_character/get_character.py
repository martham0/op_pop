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


# * Character table schema
class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    picture_link = Column(String)
    # num_searches = Column(Integer)


def get_character_by_id_from_db(character_id):
    """
    Get character name from RDS using ID
    """
    character = session.get(Characters, character_id)
    return character


def handler(event, context):
    """
    Grab character id from path parameter and invoke get_character_by_id_from_db
    """
    # * Access character_id from the path parameter
    path_parameter = event["pathParameters"]
    character_id = int(path_parameter.get("character_id"))

    # * Get character info
    character = get_character_by_id_from_db(character_id)

    # * Convert character info into json
    character_data = {
        "id": character.id,
        "name": character.full_name,
    }
    json_character_data = json.dumps(character_data)
    response = {
        "statusCode": 200,
        "body": f"Character info:\n{json_character_data}"
    }
    return response
