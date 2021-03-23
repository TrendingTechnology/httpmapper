#!/usr/bin/python
# -- coding utf-8 --

from httpmapper import *
import time

banner()
alvo = str(input('[*] Enter the website URL: ')).lower().strip()

def start():
    time.sleep(0.50)
    ask = str(input('[*] What do you want to know?[Website/Links/Navigate/Emails/Cookies/Grabbing] ')).lower().strip()

    if ask == 'website': 
        extract_websites(alvo)
    elif ask == 'links': 
        get_links(alvo)
    elif ask == 'navigate':   
        navigate_links(alvo)
    elif ask == 'emails':
        extract_emails(alvo)
    elif ask == 'cookies':
        extract_cookies(alvo)
    elif ask == 'grabbing':
        extract_grabs(alvo)
    else: 
        print('[-] Enter a valid answer.')

    print()
    options = str(input('Do you want to make a consultation again?[Y/N] ')).upper().strip()
    if options == 'Y':
        banner()
        start()
    
    elif options == 'N': 
        banner()
        exit()

    else: 
        banner()
        print('Invalid option!')


if __name__=='__main__':
    start()
