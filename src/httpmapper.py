#!/usr/bin/python
# -*- coding utf-8 -*-

import argparse
import time
import os
import time, datetime
import urllib
import urllib.parse
from collections import deque
import socket
import urllib.request as urllib2

try:
    import requests
    from bs4 import BeautifulSoup
    import re
    import http.cookiejar
except ImportError:
    os.system("pip install -r requirements.txt")

# \033[31m

def banner():
    os.system("cls")
    print('''\033[1;36m
    ██╗  ██╗████████╗████████╗██████╗ ███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗ 
    ██║  ██║╚══██╔══╝╚══██╔══╝██╔══██╗████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ███████║   ██║      ██║   ██████╔╝██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
    ██╔══██║   ██║      ██║   ██╔═══╝ ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
    ██║  ██║   ██║      ██║   ██║     ██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
    ╚═╝  ╚═╝   ╚═╝      ╚═╝   ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
    by vLeeh
    \033[0m''')
    
#  Identify which browser is being used
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
}


def extract_websites():
    website = str(input('[*] Enter the URL of the website: ')).strip()
    if website.startswith('http'): 
        try: 
            source = requests.get(website).text
            soup = BeautifulSoup(source, 'lxml')
            print(soup.prettify())
            with open("extract_websites.html", "at+", encoding="utf8") as h:
                h.write(str(soup.prettify))

        except Exception as e: 
            print(f'[ERROR] {e}')

    else: 
        print()
        print('[-] Enter a valid URL.')


def extract_title(content):
    '''Get HTML title of an URL.'''
    soup = BeautifulSoup(content, "lxml")
    tag = soup.find("title", text=True)
    if not tag:
        return None

    return tag.string.strip()


def extract_links(content):
    '''Get links of URL's '''
    soup = BeautifulSoup(content, "lxml")
    links = set()  # Array but don't allow multiples elements

    for tag in soup.find_all("a", href=True):
        if tag["href"].startswith("http"):
            links.add(tag["href"])

    return links


def get_links():
    '''Create a log for links that are in the URL.'''
    ques = str(input('[*] Enter the URL of the website: ')).strip()
    page = requests.get(ques)
    links = extract_links(page.text)
    for link in links: 
        print(link)
        with open('links.txt', 'at+', encoding="utf8") as t: 
            t.write(str(links))


def crawler_links():
    '''Function that navigate websites just using one URL.'''
    start_url = str(input('[*] Enter the URL of the website: ')).strip()
    seen_urls = set([start_url])
    available_urls = set([start_url])
    while available_urls:
        url = available_urls.pop()
        try:
            content = requests.get(url, timeout=3).text

        except Exception:
            continue

        title = extract_title(content)

        if title:
            print(f"[+] Title: {title}")
            print(f"[+] URL: {url}")
            with open("links-titles.txt", "at+", encoding="utf8") as l:
                l.write(f"[+] Title: {title} \n\r [+] URL: {url}")

            time.sleep(1)
            print()

        for link in extract_links(content):
            if link not in seen_urls:
                seen_urls.add(link)
                available_urls.add(link)


def extract_emails():
    '''See URL's and emails.'''
    user_url = str(input('[*] Enter Target URL to Scan: ')).strip()

    if user_url.startswith('http'):
        try:
            urls = deque([user_url])
            count = 0
            scraped_urls = set()
            emails = set()
            while len(urls):
                count += 1
                if count == 50:
                    break
                url = urls.popleft()
                scraped_urls.add(url)

                parts = urllib.parse.urlsplit(url)
                base_url = "{0.scheme}://{0.netloc}".format(parts)

                path = url[: url.rfind("/") + 1] if "/" in parts.path else url

                print("[%d] Processing %s" % (count, url))
                try:
                    response = requests.get(url)
                except (
                    requests.exceptions.MissingSchema,
                    requests.exceptions.ConnectionError,
                ):
                    continue

                new_emails = set(
                    re.findall(
                        r"[a-z0-9\.\-+]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I
                    )
                )
                emails.update(new_emails)

                soup = BeautifulSoup(response.text, features="lxml")

                for anchor in soup.find_all("a"):
                    link = anchor.attrs["href"] if "href" in anchor.attrs else ""
                    if link.startswith("/"):
                        link = base_url + link

                    elif not link.startswith("http"):
                        link = path + link

                    if not link in urls and not link in scraped_urls:
                        urls.append(link)
                    
        except KeyboardInterrupt:
            print("[-] Closing")
            print()


        for mail in emails:
            print(emails)
            with open("emails.txt", "at+", encoding="utf8") as e: 
                e.write(f"{emails} \n\r")

    else: 
        print('[-] Enter a avaible URL.')
        print()


def extract_cookies():
    '''Get name and values of emails.'''
    URL = str(input('[*] Enter the URL of the website: ')).strip()
    if URL.startswith('https'):
        try: 
            cookie_jar = http.cookiejar.CookieJar()
            url_opner = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

            url_opner.open(URL)
            for cookie in cookie_jar: 
                print("[+] Cookie Name = %s - Cookie Value = %s" %(cookie.name, cookie.value))
                with open("cookie.txt", "at+", encoding="utf8") as c: 
                    c.write(
                        "[+] Cookie Name = %s - Cookie Value = %s \n\r" %(cookie.name, cookie.value))

        except Exception as e: 
            print()
            print(f'[ERROR] {e}')

    else: 
        print()
        print('[-] Enter an avaible URL.')


def extract_grabs(url, cookie):
    try: 
        esc = str(input("[*] GET or POST: ")).strip().lower() 
        if esc == 'post':
            req = requests.post(url, cookies={'Cookie':cookie}, headers=header)
        else:
            req = requests.get(url, cookies={'Cookie':cookie}, headers=header)

        code = req.status_code
        if code == 200:
            html = req.text
            print("\n[+] Request Succefully!\n")
            print(html.encode('utf-8'))
            with open("extract_grabs1.txt", "at+", encoding="utf8") as g: 
                g.write(
                    f"{html.encode('utf-8')}") 
        else:
            print("\n\033[31m[!] Request Failed, Exiting Program...\n\033[0m")
            exit(1)
    
    except Exception as e: 
        print(f'[ERROR]{e}')
