# Coverage
For when things don't go as intended.

## Usage
`send_email.py` takes in its errors via pipes
    `python test.py | python send_email.py`

You can actually try it, test.py will generate a simple List Index out of Range Error which should send you an email if you have it setup right.

You have the option to save the API credentials outside of the script that is executed. To take advantage of this, rename `API_temp.txt` to `API.txt` and replace the placeholders with your credentials.

### Requirements

* You will also need a SendGrid/Mandrill account, but those are free!
* You will need to install the Requests Library and its security dependencies   `pip install requests[security]`
If you plan to use Mandrill (which you should) you will need to install the SDK `pip install mandrill`
* pytz is used to set the timezone, which is necessary if your server is in a different timezone as you are, you should install that module and update the TZ accordingly in the script.


### Mandrill

Mandrill has the most setup initially, it's not hard, just long, but will be the most stable and have the lowest network traffic.

1. Get an API Key. Your key will need to be able to send emails and template emails, so be sure to allow both `Send` and `Send-Template` if you are restricting what class each API key can make.
2. Under Outbound, create a new template, the script is using the slug `fatal-script-error` so I would give it the same title for the highest likelihood of success.
3. Copy and Paste the contents of `email_template.html` into the content box on the Mandrill website.
4. Enter the default sender, From Name, and Subject; this will reduce the size of the message dict you will send in the API Request
5. Be sure to hit *Publish* on the template page!

_I also recommend that you go through and add your domain to the verified domains list on Mandrill and verify your domain, this will result in a lower likelihood of bing marked as spam_


