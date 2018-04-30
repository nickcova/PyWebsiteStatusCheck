""" TO-DO: Write the module's docstring. """
import json
import re
import socket
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

def read_html_file(file_path):
    """Reads the contents of an HTML file."""
    html_file = Path(file_path)
    if html_file.exists() and html_file.is_file():
        with html_file.open() as temp_file:
            contents = temp_file.read()
            return contents
    return None

def read_email_auth_json(file_path):
    """Checks if the e-mail authorization's JSON file exists and reads it."""
    auth_file = Path(file_path)
    if auth_file.exists() and auth_file.is_file():
        with auth_file.open() as temp_file:
            contents = temp_file.read()
            decoded = json.loads(contents)
            return decoded
    return None

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex.message)
        
    return False
