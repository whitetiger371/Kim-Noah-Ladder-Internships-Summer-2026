MAX_INPUT_LENGTH = 10000


def validate_input(text):

    if not text:
        return False, "Input cannot be empty."

    if len(text) > MAX_INPUT_LENGTH:
        return False, "Input too large."

    return True, None