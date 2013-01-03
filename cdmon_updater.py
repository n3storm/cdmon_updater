# -*- coding: utf-8 -*-

import logging
import urllib2
from hashlib import md5
from BeautifulSoup import BeautifulSoup

# CDMON Settings
## Change this with your settings
CDMON_USER = 'user'
CDMON_PASSWORD = md5('password').hexdigest()

## Do not change next settings
CDMON_GET_URL = 'https://dinamico.cdmon.org/onlineService.php?enctype=MD5&n=%s&p=%s'
CDMON_UPDATE_URL = CDMON_GET_URL + '&cip=%s'

# Logging options
LOG_FILENAME = '/var/log/cdmon_updater.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO, format=LOG_FORMAT)

# What is my ip services
SERVICE_URLS = [
            # ('http://url', (html_element, {"attr" : "attr_value"})),
            ('http://www.myglobalip.com/', ("span", { "class" : "ip" })),
            ('http://ipecho.net/plain/', None,),
        ]

def response_to_dict(value):
    mydict = dict()
    if value is not None:
        args = value.split('&')
        for arg in args:
            try:
                mydict[arg.split('=')[0]] = arg.split('=')[1]
            except:
                pass
    return mydict

def responsed(NEW_IP=None):
    response_dict = None

    if NEW_IP:
        URL = CDMON_UPDATE_URL % (CDMON_USER, CDMON_PASSWORD, NEW_IP)
    else:
        URL= CDMON_GET_URL % (CDMON_USER, CDMON_PASSWORD)

    try:
        request = urllib2.Request(URL)
        response = urllib2.urlopen(request)
        response_dict = response.read()
        return response_to_dict(response_dict)
    except:
        logging.info('Error making request %s' % URL)

    
    
def main():
    IP = None
    for url in SERVICE_URLS:
        try:
            page = urllib2.urlopen(url[0])
        except urllib2.URLError, e:
            # print e.reason
            logging.info('%s problem: %s' % (url[0], e.reason))
            
        try:
            soup = BeautifulSoup(page)
            if url[1] != False:
                IP = soup.find(url[1]).text
            else:
                IP = soup.text
            break
        except:
            logging.info('Error in HTML at %s.' % url[0])

    get = responsed()
    if get is not None and IP is not None:
        # print get
        if 'error' not in get['resultat']:
            if get['newip'] == IP:
                logging.info('Not updating. Everything OK.')
            else:
                update = responsed(NEW_IP = IP)
                logging.info('Updating %s' % IP)
        else:
            logging.info('User or password wrong')

if __name__ == "__main__":
    main()



