#!/usr/bin/python
# -*- coding utf-8 -*-

from httpmapper import *

def httpmapper_main():
    banner()
    question = str(input('What do you want to know of the URL?[Website/Links/Navigate/Emails/Cookies/Grabbing] ')).lower().strip()

    if question == 'website': 
        extract_websites()
    elif question == 'links': 
        get_links()
    elif question == 'navigate':
        crawler_links()
    elif question == 'emails': 
        extract_emails()
    elif question == 'cookies': 
        extract_cookies()
    elif question == 'grabbing': 
        extract_grabs()
    else: 
        print('Enter a valid answer!')

    print()
    options = str(input('Do you want to make a consultation again?[Y/N] ')).upper().strip()
    if options == 'Y':
        banner()
        main()
    
    elif options == 'N': 
        banner()
        exit()

    else: 
        banner()
        print('Invalid option!')

if __name__ == '__main__': 
    httpmapper_main()

