import re
from pathlib import Path


def find_file(filename: str) -> Path:
    path = Path(filename)
    if path.exists() and path.is_file():
        return path

    current_dir_path = Path.cwd()
    pattern = f"**/{filename}"
    if not pattern.endswith(".html"):
        pattern += ".html"
    html_files = list(current_dir_path.glob(pattern))
    if html_files:
        return html_files[0]

    raise FileNotFoundError(
        f"File '{filename}' not found in current directory or provided path."
    )


# https://gist.github.com/dubpirate/fdea9a67500a46613ad637269320d272?permalink_comment_id=5118226#gistcomment-5118226
def to_snake_case(text: str) -> str:
    # Add an underscore before each uppercase letter that is followed by a lowercase letter
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", text)
    # Add an underscore before each lowercase letter that is preceded by an uppercase letter
    s = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s)
    # Convert the entire string to lowercase
    s = s.lower()
    return s
