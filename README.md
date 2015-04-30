# Coverage
For when things don't go as intended.

## Usage
send_email.py takes in its errors via pipes
    `python test.py | python send_email.py`

You can actually try it, test.py will generate a simple List Index out of Range Error which should send you an email if you have it setup right.

You have the option to save the API credentials outside of the script that is executed. To take advantage of this, rename `API_temp.txt` to `API.txt` and replace the placeholders with your credentials.

### Requirements

* You will need to upload `./Fatal Error Report.jpg` to a server and update the link in the email template (`./email_template.html`)
* You will also need a SendGrid account, but those are free!
* You will need to install the Requests Library and its security dependencies   `pip install requests[security]`
* pytz is used to set the timezone, which is necessary if your server is in a different timezone as you are, you should install that module and update the TZ accordingly in the script.
