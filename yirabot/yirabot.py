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


program_path = "/usr/local/bin/yirabot"

COMMANDS = {
    "help": "Used to show all usable commands. Usage: yirabot help",
    "crawl": "Used to crawl webpages and get data. Usage: yirabot crawl <url>. Optionally use the '-file' flag to extract the data to a file"
}

WRITE_TO_FILE = False

def main():
    if len(sys.argv) < 2:
        sys.exit("YiraBot: No Command Specified")
    else:
        COMMAND = sys.argv[1]
        try:
            ARGUMENT = sys.argv[2]
        except IndexError:
            pass
        match COMMAND.lower():
            case "help":
                help()
            case "crawl":
                try:
                    FLAG = sys.argv[3]
                    if FLAG == "-file":
                        global WRITE_TO_FILE
                        WRITE_TO_FILE = True
                    else:
                        sys.exit(f"YiraBot: Unrecognized flag: {FLAG}")
                except IndexError:
                    pass
                try:
                    if ARGUMENT.startswith("https://") or ARGUMENT.startswith("http://"):
                        crawl(ARGUMENT)
                    else:
                        sys.exit("YiraBot: Please enter a valid url. https://<url> or http://<url>")
                except UnboundLocalError:
                    sys.exit("YiraBot: Enter a link to crawl.")
            case _:
                print("YiraBot: Unknown Command.")
# Old Setup Function
''' 
def setup():
    global program_path
    if os.path.exists(program_path):
        sys.exit("YiraBot: YiraBot is already installed.")

    print("Initializing YiraBot Setup.\n*You could be prompted to enter your sudo password.")
    try:
        os.system("chmod +x yirabot.py")
        # Using subprocess to run the command
        process = subprocess.Popen(['sudo', 'cp', 'yirabot.py', '/usr/local/bin/yirabot'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)

        # Wait for the subprocess to complete
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            # Handle error if sudo command fails
            print(f"Error: {stderr.decode().strip()}")
            return

        # If the above command is successful, start the progress bar
        with Bar('Setting Up YiraBot', max=20) as bar:
            for i in range(20):
                time.sleep(0.1)
                bar.next()
        print("YiraBot: YiraBot successfully installed!\n*Use 'yirabot help' to see all commands ")

    except KeyboardInterrupt:
        # Handle what happens when Ctrl+C is pressed
        print("\nSetup was interrupted by the user. Exiting...")
        try:
            # Check if the process is still running and send SIGINT if it is
            os.kill(process.pid, signal.SIGINT)
        except ProcessLookupError:
            # If the process is no longer running, just pass
            pass
        return'''

# Old uninstall function
'''
def uninstall():
    global program_path
    if os.path.exists(program_path):
        user_choice = input("YiraBot: Do you wish to delete YiraBot from your system? (Y/n) ").lower()
        if user_choice in ["y", "yes"]:
            try:
                os.remove(program_path)
                with Bar('Deleting YiraBot', max=20) as bar:
                    for i in range(20):
                        time.sleep(0.1)
                        bar.next()
                print("YiraBot has been successfully removed.")
            except PermissionError:
                print("Error: Permission denied. Try running with elevated permissions. (sudo yirabot uninstall)")
            except Exception as e:
                print(f"Error: {e}")
        elif user_choice in ["n", "no"]:
            print("YiraBot: Cancelled Uninstall Process")
        else:
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
    else:
        print("YiraBot: YiraBot is not installed on your system.")'''



def write_to_file(data, filename):
    with open(filename, 'w') as file:
        for key, value in data.items():
            if isinstance(value, list):
                # Convert each element to string if it's a BeautifulSoup Tag
                str_values = [str(item) if isinstance(item, Tag) else item for item in value]
                value = ', '.join(str_values)
            file.write(f"{key.capitalize()}: {value}\n")
            file.write("-" * 50 + "\n")  # Divider



def divider():
    print("-" * 80)
    time.sleep(0.5)

def help():
    global COMMANDS
    print("ALL AVAILABLE COMMANDS")
    divider()
    for command in COMMANDS:
        print(f"{command}: {COMMANDS[command]}")
        divider()

def crawl(url):
    def is_allowed_by_robots_txt(url):
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url + "/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)

    def parse_sitemap(url):
        sitemap_url = url + "/sitemap.xml"
        secondary_url = url + "/static/sitemap.xml"
        try:
            response = requests.get(sitemap_url)
        except Exception:
            response = requests.get(secondary_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                urls = [element.text for element in soup.find_all("loc")]
                return urls
        except requests.exceptions.RequestException:
            return []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    if not is_allowed_by_robots_txt(url):
        print("YiraBot: Crawling forbidden by robots.txt")
        return

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, features="html5lib")

        favicon_tag = soup.find("link", {"rel": "icon"})
        meta_description_tag = soup.find("meta", {"name": "description"})
        title_tag = soup.find("title")
        og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
        twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
        canonical_tag = soup.find("link", {"rel": "canonical"})

        links = soup.find_all('a', href=True)
        internal_links = [link['href'] for link in links if link['href'].startswith('/')]
        external_links = [link['href'] for link in links if link['href'].startswith('http')]
        images = soup.find_all('img', src=True)
        image_urls = [img['src'] for img in images]
        sitemap_urls = parse_sitemap(url)

        with Bar(f'Yirabot Crawling: {url}', max=40) as bar:
            for i in range(40):
                time.sleep(0.060)
                bar.next()

        data = {
            'favicon': favicon_tag.get("href") if favicon_tag else None,
            'meta_description': meta_description_tag.get("content") if meta_description_tag else None,
            'title': title_tag.get_text() if title_tag else None,
            'open_graph_tags': og_tags,
            'twitter_card_tags': twitter_tags,
            'canonical_url': canonical_tag.get("href") if canonical_tag else None,
            'internal_links': internal_links,
            'external_links': external_links,
            'image_urls': image_urls,
            'sitemap_urls': sitemap_urls
        }

        if WRITE_TO_FILE:
            if WRITE_TO_FILE:
                # Replace problematic characters in the URL
                safe_url = url.replace("https://", "").replace("http://", "").replace("/", "_")

                # Format the current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                # Generate a safe filename
                filename = f"{safe_url}.{timestamp}.txt"

                write_to_file(data, filename)
                divider()
                sys.exit("YiraBot: file created.")

        # Print statements
        divider()
        print("Favicon:", data['favicon'])
        divider()
        print("Meta Description:", textwrap.fill(data['meta_description'], width=80) if data['meta_description'] else "This Page Has No Current Description")
        divider()
        print("Website Title:", data['title'] if data['title'] else "This Page Has No Title.")
        divider()
        print("Open Graph Tags:")
        for tag in data['open_graph_tags']:
            og_property = tag.get("property", tag.get("name"))
            og_content = tag.get("content")
            print(f"{og_property}: {og_content}")
        divider()
        print("Twitter Card Tags:")
        for tag in data['twitter_card_tags']:
            twitter_property = tag.get("name")
            twitter_content = tag.get("content")
            print(f"{twitter_property}: {twitter_content}")
        divider()
        print("Canonical URL:", data['canonical_url'])
        divider()
        print("Internal Links:", data['internal_links'])
        divider()
        print("External Links:", data['external_links'])
        divider()
        print("Image URLs:", data['image_urls'])
        divider()
        print("Sitemap URLs:", data['sitemap_urls'])
        divider()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    except Exception as e:
        print(f"An error occurred while parsing the page: {e}")



if __name__ == '__main__':
    main()