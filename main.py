#!/usr/bin/python3
from apiclient.discovery import build
from time import sleep
from email.mime.text import MIMEText
from difflib import SequenceMatcher
import urllib.request
import base64
from sys import argv
from apiclient import errors
from random import randrange
from argparse import ArgumentParser

minSleepTime = 60
maxSleepTime = 120

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
    return {'raw': base64.b64encode(bytes(message.as_string(), 'utf-8')).decode('utf-8')}

def sendNotification(service, email):
    rawMessage = createMessage('bot', email, 'test', 'test message')
    sendMessage(service, 'me', rawMessage)

def areStringsDiffer(a, b):
    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio() != 1.0

def getHtml(url):
    with urllib.request.urlopen(url) as response:
       return response.read()  

def setupArguments():
    parser = ArgumentParser(description = 'Watch for website change and send e-mail notification')
    parser.add_argument('website', help = 'Website to watch for changes')
    parser.add_argument('email', help = 'E-mail to send notification if website changes')
    parser.add_argument('key', help = 'Key for public google API access')
    parser.add_argument('--min-wait-time', default = minSleepTime, type = int,
        help = 'Minimum time between site check (default = 60s)')
    parser.add_argument('--max-wait-time', default = maxSleepTime, type = int,
        help = 'Maximum time between site check (default = 120s)')
    return parser

def getArguments():
    parser = setupArguments()
    return parser.parse_args(argv[1:])

def main():
    arguments = getArguments()
    site = arguments.website
    email = arguments.email
    service = build('gmail', 'v1', developerKey = arguments.key)
    oldContent = getHtml(site)

    # TODO: read optional min/max wait time

    sendNotification(service, email)

    # while True:
    #     newContent = getHtml(site)
    #     if areStringsDiffer(oldContent, newContent):
    #         print('Content differ!')
    #         sendNotification(service, email)
    #     else:
    #         print('Same content!')
    #     oldContent = newContent
    #     wait()

if __name__ == '__main__':
    main()
