#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import sys
import requests
from datetime import datetime
import pytz


class SendGrid(object):
    def __init__(self, username, password):
        self.sendgrid_username = username
        self.sendgrid_password = password

    def send(self, to, subject, message_html):
        data = dict()
        data['api_user'] = self.sendgrid_username
        data['api_key'] = self.sendgrid_password
        data['to'] = to
        data['from'] = 'Python<python@tompaulus.com>'  # Replace this with your from address
        data['subject'] = subject
        data['html'] = message_html
        sg_response = requests.post('https://api.sendgrid.com/api/mail.send.json', data)

        if sg_response.json()['message'] == 'success':
            return True, None
        else:
            return False, sg_response.json()['errors']


def read_api_keys(rel_file_path="./API.txt"):
    """
    :param rel_file_path: Location of the API Key File relative to the file being executed.
    :return sendgrid_user: FancyHands API Key
    :return sendgrid_pass: FancyHands API Secret
    :rtype : tuple

    """
    sendgrid_user = ''
    sendgrid_pass = ''

    try:
        with open(rel_file_path) as license_file:
            line = license_file.readline()

            while line != '':
                if line.count('User:') == 1:
                    # Key Line
                    sendgrid_user = line[6: -1]

                elif line.count('Pass:') == 1:
                    # Secret Line
                    sendgrid_pass = line[6: -1]

                line = license_file.readline()  # Advance to the next line in the file.

    except IOError:
        print 'The API Key file does not exist. Not Fatal.'
        return None, None

    return sendgrid_user, sendgrid_pass


def read_pipe():
    data_in = sys.stdin.read()
    return data_in


def make_email(error, date):
    with open('./email_template.html') as template:
        msg = template.read().replace('{{ Error Message }}', error).replace('{{ Date }}', date)

        return msg


if __name__ == "__main__":
    d = datetime.now(tz=pytz.timezone('US/Pacific')).strftime('%A, %B %d, %Y')
    # e = read_pipe()
    e = """
Traceback (most recent call last):
  File "test.py", line 7, in <module>
    l[3]  # List Index out of Range Error
IndexError: list index out of range

    """

    username, password = read_api_keys()
    # Uncomment the lines below if you want to bypass the external file.
    # username = ''
    # password = ''

    response, e = SendGrid(username, password).send('tom@tompaulus.com', 'Fatal Script Error', make_email(e, d))

    if not response:
        print e






