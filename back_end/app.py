from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)

# Database setup
DATABASE_URL = 'postgresql://localhost:5432/op_pop'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    date_added = Column(Date)
    sentiment_score = Column(Float)
    picture_link = Column(String)

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/add_character', methods=['POST'])
def add_character():
    """
    Add character to DB
    """
    data = request.json
    new_character = Character(full_name=data['name'], date_added=datetime.now(), picture_link=data['picture_link'])
    session.add(new_character)
    session.commit()
    return jsonify({'message':'User added successfully'})

@app.route('/character/<int:id>', methods=['GET'])
def get_character_by_id(id):
    """
    Get character by their id
    """
    response = session.get(Character,id)
    if response:
        return jsonify({
            'id': response.id,
            'name': response.full_name,
            'date_added': response.date_added.strftime('%Y-%m-%d'),  # Convert date to string
            'picture_link': response.picture_link,
            'message': 'yay'
        })
    else:
        return jsonify({'message': 'Character not found'})
    
@app.route('/characters', methods=['GET'])
def get_all_characters():
    """
    Get all characters
    """
    responses = session.query(Character).all()
    for response in responses:
        print(response.full_name)
    print(f'---------\n{response}')
    return jsonify({
        'message': 'huh'
        })
    
@app.route('/top3', methods=['GET'])
def get_top3_characters():
    """
    Get 3 characters with the highest sentiment score
    """
    responses = session.query(Character).order_by(Character.sentiment_score.desc()).limit(3).all()
    for response in responses:
        print(response.id, response.full_name, response.sentiment_score)
    print(f'---------\n{response}')
    return jsonify({
        'message': 'wow'
        })

if __name__ == '__main__':
    app.run(debug=True)
