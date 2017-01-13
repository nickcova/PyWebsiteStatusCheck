"""Script description"""
import sys
import urllib.request
from pathlib import Path
import json

REQUEST_TIMEOUT = 10

def read_sites_json(file_path):
    """Checks if the site's JSON file exists and reads it. Returns
    a Dictionary with (Site Name, Site Url) pairs."""
    sites_file = Path(file_path)
    if sites_file.exists() and sites_file.is_file():
        with sites_file.open() as f:
            contents = f.read()
            decoded = json.loads(contents)
            return decoded
    return None


def check_site_status(site_url):
    """Checks a website's status by making a request"""
    try:
        print("Requesting : {0}".format(site_url))
        myrequest = urllib.request.urlopen(site_url, None, REQUEST_TIMEOUT)
        print("Codigo recibido: {0}".format(myrequest.getcode()))
    except urllib.error.HTTPError as ex1:
        if hasattr(ex1, "reason"):
            print("We failed to reach a server.")
            print("Reason: ", ex1.reason)
        if hasattr(ex1, "code"):
            print("The server couldn\'t fulfill the request.")
            print("Error code: ", ex1.code)
    except urllib.error.URLError as ex2:
        if hasattr(ex2, "reason"):
            print("We failed to reach a server.")
            print("Reason: ", ex2.reason)

def main(argv):
    """Main entry point for the script."""

    # Create a list of sites to check
    sites_dict = read_sites_json('sites.json')

    for key in sites_dict:
        check_site_status(sites_dict[key])

    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
