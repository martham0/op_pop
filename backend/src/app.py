from flask import Flask, request, jsonify
from flask_cors import CORS
from database.postgres import add_character_to_db, get_character_by_id_from_db, get_all_characters_from_db


app = Flask(__name__)
CORS(app)




# Database setup
# engine = create_engine(db_url)
# Base = declarative_base()


# * Create the table in the database
# Base.metadata.create_all(engine)

# * Create a session to interact with the database
# TODO remove this and move to DB helper function
# Session = sessionmaker(bind=engine)
# session = Session()


@app.route("/add_character", methods=["POST"])
def add_character():
    """
    Add character to DB
    """
    data = request.json
    # TODO check if character exists
    try:
        add_character_to_db(data['name'], data['picture_link'])
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        # Handle any error
        return jsonify({'error': str(e)}), 500


@app.route("/character/<int:character_id>", methods=["GET"])
def get_character_by_id(character_id):
    """
    Get character by their id
    """
    response = get_character_by_id_from_db(character_id)
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
    characters = get_all_characters_from_db
    # print(f"----Characters\n{type(characters)}")
    # for character in characters:
    #     print("Character ID:", character.id)
    #     print("Character Name:", character.name)
    #     print("Character Age:", character.age)
    #     print()  # Empty line for clarity
    return jsonify(
        {"characters": "test"}
    )
#
#
# @app.route("/top3", methods=["GET"])
# def get_top3_characters():
#     """
#     Get 3 characters with the highest sentiment score
#     """
#     res = []
#     data = session.query(Character).order_by(Character.sentiment_score.desc()).limit(3).all()
#     character_list = [{
#         "id": character.id,
#         "full_name": character.full_name,
#         "date_added": character.date_added,
#         "sentiment_score": character.sentiment_score,
#         "picture_link": character.picture_link} for character in data]
#     return jsonify({"characters": character_list})
#
#
# @app.route("/add_attribute", methods=["PUT"])
# def update_character():
#     data = request.json
#     # Define the new column
#     new_column = Column(data["attribute"], data["type"])
#     # Add the new column to the table
#     Character.create_column(new_column)
#     return jsonify({"message": "Attribute added successfully"})


if __name__ == "__main__":
    # if __name__ == "__main__":
    app.run(debug=True)
