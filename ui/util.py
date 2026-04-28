import re


# https://gist.github.com/dubpirate/fdea9a67500a46613ad637269320d272?permalink_comment_id=5118226#gistcomment-5118226
def to_snake_case(text: str) -> str:
    # Add an underscore before each uppercase letter that is followed by a lowercase letter
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    # Add an underscore before each lowercase letter that is preceded by an uppercase letter
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    # Convert the entire string to lowercase
    s = s.lower()
    return s
