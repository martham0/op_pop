# from ../.
def handler(event, context):
    response = {
        "statusCode": 200,
        "body": f"luffy ---, {event}, {context}"
    }
    return response
