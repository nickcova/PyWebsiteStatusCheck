""" TO-DO: Write the module's docstring. """
import threading
import time
import urllib.request
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from helpers import read_html_file
from socket import gaierror

REQUEST_TIMEOUT = 10

class RequestsThread(threading.Thread):
    """TO-DO: Write the class' docstring."""
    def __init__(self, name, sites_dict, emails, email_auth_data):
        threading.Thread.__init__(self)
        self.name = name
        self.sites_dict = sites_dict
        self.emails = emails
        self.email_auth_data = email_auth_data
    def run(self):
        while True:
            for key in self.sites_dict:
                check_site_status(self.sites_dict[key], self.emails, self.email_auth_data)
            time.sleep(300)

class InputThread(threading.Thread):
    """TO-DO: Write the class' docstring."""
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    def run(self):
        while True:
            user_input = input(">>")
            if user_input == 'q':
                print("Info: Exiting input thread...")
                break

def check_site_status(site_url, emails, email_auth_data):
    """Checks a website's status by making a request"""
    try:
        print("Requesting : {0}".format(site_url))
        myrequest = urllib.request.urlopen(site_url, None, REQUEST_TIMEOUT)
        print("Codigo recibido: {0}".format(myrequest.getcode()))
    except urllib.error.HTTPError as ex1:
        if hasattr(ex1, "reason"):
            print("\x1b[0;37;41m" + " Warning " + "\x1b[0m" + " We failed to reach a server.")
            print("Reason: ", ex1.reason)
        if hasattr(ex1, "code"):
            print("\x1b[0;37;41m" + " Warning " + "\x1b[0m" + "The server couldn\'t fulfill the request.")
            print("Error code: ", ex1.code)
        if hasattr(ex1, "reason") and hasattr(ex1, "code"):
            send_email_notification(email_auth_data, emails, site_url, ex1.reason, ex1.code)
    except urllib.error.URLError as ex2:
        if hasattr(ex2, "reason"):
            exReason = ""
            print("\x1b[0;37;41m" + " Warning " + "\x1b[0m" + "We failed to reach a server.")
            if isinstance(ex2.reason, str):
                exReason = ex2.reason
                print("Reason: ", ex2.reason)
            elif isinstance(ex2.reason, gaierror):
                exReason = str(ex2.reason)
                print("Reason: ", str(ex2.reason))
            send_email_notification(email_auth_data, emails, site_url, exReason)

def send_email_notification(email_auth_data, emails, site, reason, code="N/A"):
    """Sends an email with the site, reason and request code"""
    if emails:
        print("Sending email...")
        sender = email_auth_data["Email"]
        recipients = ','.join(map(str, emails))

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Website Warning!"
        msg['From'] = sender
        msg['To'] = recipients

        text_msg = "Site = {0}\nReason = {1}\nCode = {2}".format(site, reason, code)
        #html_msg = read_html_file('html/alert.html').format(site, reason, code, "test date")
        html_msg = read_html_file('html/alert.html').replace("{0}", site).replace("{1}", reason)
        html_msg = html_msg.replace("{2}", str(code))
        html_msg = html_msg.replace("{3}", datetime.now().strftime("%d/%m/%Y %I:%M:%S %p %Z%z"))

        part1 = MIMEText(text_msg, 'plain')
        part2 = MIMEText(html_msg, 'html')

        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, email_auth_data["Password"])
        server.sendmail(sender, recipients, msg.as_string())
        server.quit()
        print("Email sent!")
