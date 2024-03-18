import req
def handle(event, context):
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