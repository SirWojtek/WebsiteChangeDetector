#!/usr/bin/python3
from apiclient.discovery import build
from time import sleep
from email.mime.text import MIMEText
from difflib import SequenceMatcher
import urllib.request
from apiclient import errors
from random import randrange

minSleepTime = 60
maxSleepTime = 120
# service = build('Gmail API', 'v1')

def wait():
    sleep(randrange(minSleepTime, maxSleepTime))

def sendMessage(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('An error occurred: %s' % error)

def createMessage(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64 encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.b64encode(message.as_string())}

def sendNotification(email):
    pass

def areStringsDiffer(a, b):
    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio() == 1.0

def getHtml(url):

    with urllib.request.urlopen(url) as response:
       return response.read()  

def main():
    site = 'http://www.davidgilmour.com'
    email = 'foo@bar.com'
    oldContent = getHtml(site)

    while True:
        newContent = getHtml(site)
        if areStringsDiffer(oldContent, newContent):
            print('Content differ!')
            sendNotification(email)
            continue
        print('Same content!')
        oldContent = newContent
        wait()

if __name__ == '__main__':
    main()
