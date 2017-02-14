#!/usr/bin/python3

""" TO-DO: Write the module's docstring. """
import sys
import workers
import helpers

VERBOSE_MODE = False

def main(argv):
    """Main entry point for the script."""

    # Create a list of sites to check
    sites_dict = helpers.read_sites_json('config/sites.json')
    emails = helpers.read_emails_json('config/emails.json')

    if sites_dict is not None:
        request_thread = workers.RequestsThread("Thread-1", sites_dict)
        request_thread.daemon = True
        request_thread.start()
        input_thread = workers.InputThread("Thread-2")
        input_thread.start()
        input_thread.join()

    print("Info: Goodbye!")
    sys.exit()

if __name__ == '__main__':
    main(sys.argv[1:])
