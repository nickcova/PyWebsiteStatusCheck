""" TO-DO: Write the module's docstring. """
import json
import re
from pathlib import Path

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

def read_emails_json(file_path):
    """Checks if the e-mail's JSON file exists and reads it. Returns
    a list of strings representing e-mail addresses"""
    emails_file = Path(file_path)
    if emails_file.exists() and emails_file.is_file():
        with emails_file.open() as temp_file:
            contents = temp_file.read()
            decoded = json.loads(contents)
            if len(decoded) > 0:
                for email in decoded:
                    if not is_valid_email(email):
                        decoded.remove(email)
            return decoded
    return None

def is_valid_email(email_str):
    """Checks if a string represents a valid e-mail address. This function
    only checks the string's structure, it does not verify MX records."""
    if len(email_str) >= 3:
        if re.match("^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$", email_str) != None:
            return True
    return False
