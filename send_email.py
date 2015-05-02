#! /usr/bin/python
# Written By Tom Paulus, @tompaulus, www.tompaulus.com

import os
import sys
import requests
from datetime import datetime
import pytz
import mandrill  # Comment this line if you don't plan to use Mandrill
import json


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

        json = sg_response.json

        if json['message'] == 'success':
            return True, None
        else:
            return False, json['errors']


class Mandrill(object):
    def __init__(self, key):
        self.client = mandrill.Mandrill(key)

    def send(self, to, to_name, error, date):
        try:
            message = {'auto_text': True,
                       'important': True,
                       'merge_language': 'mailchimp',
                       'global_merge_vars': [{'name': 'ERROR', 'content': error},
                                             {'name': 'DATE', 'content': date}],
                       'metadata': {'error': error},
                       'signing_domain': 'tompaulus.com',
                       'tags': ['Coverage'],
                       'from_email': 'python@tompaulus.com',
                       'to': [{'email': to,
                               'name': to_name,
                               'type': 'to'}],
                       'track_opens': True}

            result = self.client.messages.send_template(template_name='fatal-script-error', template_content=[],
                                                        message=message)

            if result[0]['status'] == 'sent':
                return True, None
            else:
                return False, result[0]['reject_reason']

        except mandrill.Error, e:
            # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
            # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
            raise


def read_api_keys(rel_file_path="./API.json"):
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
        msg = template.read().replace('*|Error Message|*', error).replace('*|Date|*', date)

    return msg


if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))

    d = datetime.now(tz=pytz.timezone('US/Pacific')).strftime('%A, %B %d, %Y')
    e = read_pipe()
#     e = """
# Traceback (most recent call last):
#   File "test.py", line 7, in <module>
#     l[3]  # List Index out of Range Error
# IndexError: list index out of range
#
#     """

    while e.startswith(' '):		# Remove Leading Spaces on e
            e = e[1:]
    while e.endswith(' '):			# Remove Trailing Spaces
            e = e[:-1]

    credentials_dict = json.loads(open('./API.json').read())
    # Uncomment the lines below if you want to bypass the external file.
    # username = ''
    # password = ''

    if e != '':
        # response, e = SendGrid(credentials_dict['SendGrid']['username'], credentials_dict['SendGrid']['password']).send(
        # 'tom@tompaulus.com', 'Fatal Script Error', make_email(e, d))
        response, e = Mandrill(credentials_dict['Mandrill']['key']).send('tom@tompaulus.com', 'Tom Paulus', e, d)

        if not response:
            print e
