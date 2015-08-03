#!/usr/bin/python3
import urllib.request

def getHtml(url):
    with urllib.request.urlopen(url) as response:
       return response.read()  

def main():
       print(getHtml('http://www.onet.pl'))

if __name__ == '__main__':
    main()
