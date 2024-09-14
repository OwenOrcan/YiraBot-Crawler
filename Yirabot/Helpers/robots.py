import requests
import re
from urllib.parse import urlparse


class RobotsFileAnalyzer:

    def normalize_url(self, url):
        # Add https:// if the URL does not start with http or https
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed_url = urlparse(url)

        # Rebuild the URL to only include the scheme (https) and domain
        domain = parsed_url.netloc

        # Return the normalized URL in the form of https://domain
        return f'https://{domain}'

    def check_permissions(self, url):
        if not self.validate_url(url):
            return (1, [], [])  # Error code 1: Invalid URL

        allowed_urls = []
        disallowed_urls = []
        url = self.normalize_url(url)

        try:
            response = requests.get(f"{url}/robots.txt")
            response.raise_for_status()  # Handle HTTP errors

            # Parse robots.txt lines for Allow and Disallow rules
            current_user_agent = None
            for line in response.text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):  # Skip irrelevant lines
                    continue

                if line.lower().startswith('user-agent:'):
                    current_user_agent = line.split(':', 1)[1].strip()
                elif line.lower().startswith('allow:') and current_user_agent == '*':
                    allowed_urls.append(line.split(':', 1)[1].strip())
                elif line.lower().startswith('disallow:') and current_user_agent == '*':
                    path = line.split(':', 1)[1].strip()
                    if path:
                        disallowed_urls.append(path)

            return (0, allowed_urls, disallowed_urls)  # No errors, return lists

        except requests.RequestException:
            return (2, [], [])

    def validate_url(self, url):
        url_pattern = re.compile(
            r'^(https?):\/\/'  # Protocol (http or https)
            r'(\S+(:\S*)?@)?'  # Optional username:password@
            r'([A-Za-z0-9.-]+)'  # Domain name
            r'(\.[A-Za-z]{2,})'  # Top-level domain
            r'(:\d+)?'  # Optional port
            r'(\/[^\s]*)?$'  # Optional path
        )

        # Match the URL against the pattern
        return re.match(url_pattern, url) is not None


robot = RobotsFileAnalyzer()
print(robot.check_permissions("https://youtube.com"))
