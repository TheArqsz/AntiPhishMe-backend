import json

invalid_post_error_msg_verifier = {
    "error": "Invalid request"
}


def error_message_helper(msg):
    return json.dumps(
        { 
            "error": str(msg)
        }
    )


class ErrorMessages:
    pass
