#!/usr/bin/env python3
import os
import sys
from progress.bar import Bar
import subprocess
import signal
from bs4 import BeautifulSoup
import requests
import textwrap
import urllib.robotparser
import time

program_path = "/usr/local/bin/yirabot"

COMMANDS = {
    "setup": "Used to install YiraBot when first installed. Usage: python3 yirabot.py setup",
    "uninstall": "Used to uninstall YiraBot from the system. Usage: yirabot uninstall",
    "help": "Used to show all usable commands. Usage: yirabot help",
    "crawl": "Used to crawl webpages and get data. Usage: yirabot crawl <url>"
}

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
            case "setup":
                setup()
            case "uninstall":
                uninstall()
            case "help":
                help()
            case "crawl":
                try:
                    if ARGUMENT.startswith("https://") or ARGUMENT.startswith("http://"):
                        crawl(ARGUMENT)
                    else:
                        sys.exit("YiraBot: Please enter a valid url. https://<url> or http://<url>")
                except UnboundLocalError:
                    sys.exit("YiraBot: Enter a link to crawl.")
            case _:
                print("YiraBot: Unknown Command.")


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
        return


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
        print("YiraBot: YiraBot is not installed on your system.")

def help():
    global COMMANDS
    print("ALL USABLE COMMANDS")
    for command in COMMANDS:
        print(f"{command}: {COMMANDS[command]}")

def crawl(url):
    def divider():
        print("-" * 80)
        time.sleep(0.5)

    def is_allowed_by_robots_txt(url):
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(url + "/robots.txt")
        rp.read()
        return rp.can_fetch("*", url)

    def parse_sitemap(url):
        sitemap_url = url + "/sitemap.xml"
        try:
            response = requests.get(sitemap_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'xml')
                urls = [element.text for element in soup.find_all("loc")]
                return urls
        except requests.exceptions.RequestException:
            return []


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    if not is_allowed_by_robots_txt(url):
        print("Crawling forbidden by robots.txt")
        return

    try:
        # Send a request to the URL with custom headers
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(response.text, features="html5lib")

        # Find the <link> tag with rel="icon"
        favicon_tag = soup.find("link", {"rel": "icon"})
        # Find The Meta Description:
        meta_description_tag = soup.find("meta", {"name": "description"})
        # Find Title
        title_tag = soup.find("title")
        # Find Open Graph Tags
        og_tags = soup.find_all("meta", property=lambda x: x and x.startswith("og:"))
        # Find Twitter Tags
        twitter_tags = soup.find_all("meta", attrs={"name": lambda x: x and x.startswith("twitter:")})
        # Find Canonical URL
        canonical_tag = soup.find("link", {"rel": "canonical"})

        with Bar(f'Yirabot Crawling: {url}', max=40) as bar:
            for i in range(40):
                time.sleep(0.060)
                bar.next()

        if favicon_tag:
            favicon_link = favicon_tag.get("href")
            print("Favicon:", favicon_link)
            divider()
        else:
            print("This Page Has No Favicon.")

        if meta_description_tag:
            meta_description = meta_description_tag.get("content")
            wrapped_description = textwrap.fill(meta_description, width=80)
            print("Meta Description:", wrapped_description)
            divider()
        else:
            print("This Page Has No Current Description")
            divider()

        if title_tag:
            title = title_tag.get_text()
            print("Website Title:", title)
            divider()
        else:
            print("This Page Has No Title.")
            divider()

        if og_tags:
            print("Open Graph Tags:")
            for tag in og_tags:
                og_property = tag.get("property", tag.get("name"))
                og_content = tag.get("content")
                print(f"{og_property}: {og_content}")
            divider()
        else:
            print("This Page Has No Open Graph Tags.")
            divider()

        if twitter_tags:
            print("Twitter Card Tags:")
            for tag in twitter_tags:
                twitter_property = tag.get("name")
                twitter_content = tag.get("content")
                print(f"{twitter_property}: {twitter_content}")
            divider()
        else:
            print("This Page Has No Twitter Card Tags.")
            divider()

        if canonical_tag:
            canonical_url = canonical_tag.get("href")
            print("Canonical URL:", canonical_url)
            divider()
        else:
            print("This Page Has No Canonical URL.")
            divider()

        # Link Extraction
        links = soup.find_all('a', href=True)
        internal_links = [link['href'] for link in links if link['href'].startswith('/')]
        external_links = [link['href'] for link in links if link['href'].startswith('http')]
        print("Internal Links:", internal_links)
        divider()
        print("External Links:", external_links)
        divider()

        # Image Extraction
        images = soup.find_all('img', src=True)
        image_urls = [img['src'] for img in images]
        print("Image URLs:", image_urls)
        divider()

        # Content Extraction (Example for article content, adjust based on site structure)
        # For example, if the main content is inside a div with class 'article-body', you can use:
        # content = soup.find('div', class_='article-body').get_text(strip=True)
        # print("Content:", content)
        # divider()

        # Sitemap Parsing (Optional)
        sitemap_urls = parse_sitemap(url)
        if sitemap_urls:
            print("Sitemap URLs:", sitemap_urls)
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