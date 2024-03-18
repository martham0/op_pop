from flask import Flask, request, jsonify
from flask_cors import CORS
from database.postgres import add_character_to_db, get_character_by_id_from_db, get_all_characters_from_db, \
    add_sentiment_score_to_character

app = Flask(__name__)
CORS(app)


@app.route("/add_character", methods=["POST"])
def add_character():
    """
    Add character to DB
    """
    data = request.json
    # TODO check if character exists
    try:
        # add_character_to_db(data["name"], data["picture_link"])
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        # Handle any error
        return jsonify({"error": str(e)}), 500


@app.route("/add_sentiment_score", methods=["POST"])
def add_character_sentiment_score():
    data = request.json
    # TODO check if character exists
    try:
        add_sentiment_score_to_character(data["sentiment_score"], data["public_sentiment"], data["character_id"])
        return jsonify({"message": "Score added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
    data = get_all_characters_from_db()
    character_list = [{
        "id": character.id,
        "full_name": character.full_name,
        "date_added": character.date_added,
        "picture_link": character.picture_link} for character in data]
    return jsonify(
        {"characters": character_list}
    )


#
#
# @app.route("/top_three", methods=["GET"])
# def get_top_three_characters():
#     """
#     Get top 3 characters with the highest sentiment score
#     """
#     data = get_top_three_characters_from_db()
#     character_list = [{
#         "id": character.id,
#         "full_name": character.full_name,
#         "date_added": character.date_added,
#         "picture_link": character.picture_link} for character in data]
#     return jsonify({"characters": character_list})


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
