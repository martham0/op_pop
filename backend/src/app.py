from flask import Flask, request, jsonify
from flask_cors import CORS

from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import configparser
import sys
print(f"-----{sys.path}")
from backend.database.write_to_db import add_character_to_db
# import sys
# sys.path.append('backend/database')

# Import config values
config = configparser.ConfigParser()
config.read("config.ini")
db_url = config["Database"]["url"]

app = Flask(__name__)
CORS(app)

# Database setup
engine = create_engine(db_url)
Base = declarative_base()


# ? Might create tables manually instead?
# TODO: Need to move this to DB helper function
class Characters(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    sentiment_score = Column(Float)
    # ? Do I need the characters table to access the scores table?
    picture_link = Column(String)
    num_searches = Column(Integer)


class SentimentScores(Base):
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True)
    sentiment_score = Column(Float)
    sentiment = Column(String)
    date_added = Column(Date)
    character_id = Column(Integer, ForeignKey("characters.id"))
    character = relationship("Character", back_populates="sentiment_scores")
# ? Does this need to be bidirectional?

# * Create the table in the database
Base.metadata.create_all(engine)

# * Create a session to interact with the database
# TODO remove this and move to DB helper function
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/add_character", methods=["POST"])
def add_character():
    """
    Add character to DB
    """
    data = request.json
    add_character_to_db(data['name'],data['picture_link'])
    return jsonify({"message": "User added successfully"})


@app.route("/character/<int:id>", methods=["GET"])
def get_character_by_id(id):
    """
    Get character by their id
    """
    response = session.get(Character, id)
    if response:
        return jsonify({
            "id": response.id,
            "name": response.full_name,
            "date_added": response.date_added.strftime("%Y-%m-%d"),  # Convert date to string
            "picture_link": response.picture_link,
            "message": "yay"
        })
    else:
        return jsonify({"message": "Character not found"})


@app.route("/characters", methods=["GET"])
def get_all_characters():
    """
    Get all characters
    """
    data = session.query(Character).all()
    res = []
    # for row in data:
    #     res.append({row.id: }
    #     character_list = [{"id": character.id, "name": character.name, "age": character.age} for character in characters]
    character_list = [{
        "id": character.id,
        "full_name": character.full_name,
        "date_added": character.date_added,
        "sentiment_score": character.sentiment_score,
        "picture_link": character.picture_link} for character in data]
    return jsonify(
        {"characters": character_list}
    )


@app.route("/top3", methods=["GET"])
def get_top3_characters():
    """
    Get 3 characters with the highest sentiment score
    """
    res = []
    data = session.query(Character).order_by(Character.sentiment_score.desc()).limit(3).all()
    character_list = [{
        "id": character.id,
        "full_name": character.full_name,
        "date_added": character.date_added,
        "sentiment_score": character.sentiment_score,
        "picture_link": character.picture_link} for character in data]
    return jsonify({"characters": character_list})


@app.route("/add_attribute", methods=["PUT"])
def update_character():
    data = request.json
    # Define the new column
    new_column = Column(data["attribute"], data["type"])
    # Add the new column to the table
    Character.create_column(new_column)
    return jsonify({"message": "Attribute added successfully"})


if __name__ == "__main__":
    app.run(debug=True)
