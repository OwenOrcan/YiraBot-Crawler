#!/usr/bin/env python3
import os
import sys
from bs4 import BeautifulSoup, Tag
import requests
import textwrap
import urllib.robotparser
import time
from datetime import datetime
from .crawl import crawl,crawl_content
from colorama import Fore



def main():
    if len(sys.argv) < 2:
        help()
    else:
        COMMAND = sys.argv[1]
        try:
            ARGUMENT = sys.argv[2]
        except IndexError:
            pass
        match COMMAND.lower():
            case "crawl":
                try:
                    FLAG = sys.argv[3]
                except IndexError:
                    FLAG = None
                try:
                    if ARGUMENT.startswith("https://") or ARGUMENT.startswith("http://"):
                        if FLAG == "-file":
                            crawl(ARGUMENT, extract=True)
                        elif FLAG == None:
                            crawl(ARGUMENT)
                        else:
                            sys.exit(f"YiraBot: Unrecognized Flag: {FLAG}")
                    else:
                        ARGUMENT = "https://" + ARGUMENT
                        if FLAG == "-file":
                            crawl(ARGUMENT, extract=True)
                        elif FLAG == None:
                            crawl(ARGUMENT)
                        else:
                            sys.exit(f"YiraBot: Unrecognized Flag: {FLAG}")
                except UnboundLocalError:
                    sys.exit("YiraBot: Enter a link to crawl.")

            case "crawl-content":
                try:
                    FLAG = sys.argv[3]
                except IndexError:
                    FLAG = None
                try:
                    if ARGUMENT.startswith("https://") or ARGUMENT.startswith("http://"):
                        if FLAG == "-file":
                            crawl_content(ARGUMENT, extract=True)
                        elif FLAG == None:
                            crawl_content(ARGUMENT)
                        else:
                            sys.exit(f"YiraBot: Unrecognized Flag: {FLAG}")
                    else:
                        ARGUMENT = "https://" + ARGUMENT
                        if FLAG == "-file":
                            crawl_content(ARGUMENT, extract=True)
                        elif FLAG == None:
                            crawl_content(ARGUMENT)
                        else:
                            sys.exit(f"YiraBot: Unrecognized Flag: {FLAG}")
                except UnboundLocalError:
                    sys.exit("YiraBot: Enter a link to crawl.")
            case _:
                print("YiraBot: Unknown Command.")

def help():
    HELP_MESSAGE = Fore.RED+"""
YiraBot Web Crawler v1.0.6.3""" + Fore.CYAN + """

Crawl Commands:""" + Fore.RESET + """

-Basic Crawl: yirabot crawl example.com

-Extract Data to File: yirabot crawl example.com -file

-Content Crawl: yirabot crawl-content example.com

-Content Crawl to file: yirabot crawl-content example.com -file
""" + Fore.LIGHTBLUE_EX + """

Documentation: https://github.com/OwenOrcan/YiraBot-Crawler
    """
    print(HELP_MESSAGE)

if __name__ == '__main__':
    main()