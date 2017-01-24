""" TO-DO: Write the module's docstring. """
from pathlib import Path
import json

def read_sites_json(file_path):
    """Checks if the site's JSON file exists and reads it. Returns
    a Dictionary with (Site Name, Site Url) pairs."""
    sites_file = Path(file_path)
    if sites_file.exists() and sites_file.is_file():
        with sites_file.open() as temp_file:
            contents = temp_file.read()
            decoded = json.loads(contents)
            return decoded
    return None
    