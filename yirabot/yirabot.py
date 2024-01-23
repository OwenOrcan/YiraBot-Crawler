#!/usr/bin/env python3
import os
import sys
from progress.bar import Bar
import subprocess
import signal
from bs4 import BeautifulSoup, Tag
import requests
import textwrap
import urllib.robotparser
import time
import csv
from datetime import datetime
from .crawl import crawl,crawl_content



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
                        else:
                            crawl(ARGUMENT)
                    else:
                        ARGUMENT = "https://" + ARGUMENT
                        if FLAG == "-file":
                            crawl(ARGUMENT, extract=True)
                        else:
                            crawl(ARGUMENT)
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
                        else:
                            crawl_content(ARGUMENT)
                    else:
                        ARGUMENT = "https://" + ARGUMENT
                        if FLAG == "-file":
                            crawl_content(ARGUMENT, extract=True)
                        else:
                            crawl_content(ARGUMENT)
                except UnboundLocalError:
                    sys.exit("YiraBot: Enter a link to crawl.")
            case _:
                print("YiraBot: Unknown Command.")

def help():
    HELP_MESSAGE = """
    YiraBot Web Crawler v1.0.5
    
    Crawl Commands:
    
    Basic Crawl: yirabot crawl example.com
    Extract Data to File: yirabot crawl example.com -file
    Content Crawl: yirabot crawl-content example.com
    Content Crawl to file: yirabot crawl-content example.com -file
    
    Documentation: https://github.com/OwenOrcan/YiraBot-Crawler
    """
    print(HELP_MESSAGE)

if __name__ == '__main__':
    main()