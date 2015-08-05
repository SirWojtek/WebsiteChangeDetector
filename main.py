#!/usr/bin/python3
from time import sleep
from datetime import datetime
from email.mime.text import MIMEText
from difflib import SequenceMatcher
import urllib.request
from sys import argv
from random import randrange
from argparse import ArgumentParser
from smtplib import SMTP_SSL

def wait(minSleepTime, maxSleepTime):
    sleep(randrange(minSleepTime, maxSleepTime))

def createMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return message

def sendNotification(arguments):
    rawMessage = createMessage('bot', arguments.receiver,
        'Change of site ' + arguments.website + ' detected',
        'Change of ' + arguments.website + ' was detected by script on ' + str(datetime.today()))
    smtp = SMTP_SSL('smtp.gmail.com')
    smtp.login(arguments.sender, arguments.password)

    smtp.sendmail('bot', [arguments.receiver], rawMessage.as_string())
    smtp.quit()

def areStringsDiffer(a, b):
    matcher = SequenceMatcher(None, a, b)
    return matcher.ratio() != 1.0

def getHtml(url):
    with urllib.request.urlopen(url) as response:
       return response.read()  

def setupArguments():
    parser = ArgumentParser(description = 'Watch for website change and send e-mail notification')
    parser.add_argument('website', help = 'Website to watch for changes')
    parser.add_argument('receiver', help = 'E-mail to send notification if website changes')
    parser.add_argument('sender', help = 'Gmail account for sending notification')
    parser.add_argument('password', help = 'Gmail account password')
    parser.add_argument('--min-wait-time', default = 60, type = int,
        help = 'Minimum time between site check (default = 60s)')
    parser.add_argument('--max-wait-time', default = 120, type = int,
        help = 'Maximum time between site check (default = 120s)')
    return parser

def getArguments():
    parser = setupArguments()
    return parser.parse_args(argv[1:])

def main():
    arguments = getArguments()
    site = arguments.website
    oldContent = getHtml(site)

    while True:
        newContent = getHtml(site)
        if areStringsDiffer(oldContent, newContent):
            print('Content differ! Sending email notification for ' + arguments.receiver)
            sendNotification(arguments)
        else:
            print('Same content!')
        oldContent = newContent
        wait(arguments.min_wait_time, arguments.max_wait_time)

if __name__ == '__main__':
    main()
