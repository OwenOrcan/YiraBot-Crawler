import requests
import re
from urllib.parse import urlparse


class RobotsFileAnalyzer:

    def normalize_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        return f'https://{domain}'

    def check_permissions(self, url):
        if not self.validate_url(url):
            return (1,[],[])

        allowed_urls = []
        disallowed_urls = []

        try:
            response = requests.get(f"{url}/robots.txt")
            response.raise_for_status()

            current_user_agent = None
            for line in response.text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.lower().startswith('user-agent:'):
                    current_user_agent = line.split(':', 1)[1].strip()
                elif line.lower().startswith('allow:') and current_user_agent == '*':
                    allowed_urls.append(line.split(':', 1)[1].strip())
                elif line.lower().startswith('disallow:') and current_user_agent == '*':
                    path = line.split(':', 1)[1].strip()
                    if path:
                        disallowed_urls.append(path)

            return (0, allowed_urls, disallowed_urls)

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

        return re.match(url_pattern, url) is not None


robot = RobotsFileAnalyzer()
print(robot.check_permissions("https://youtube.com"))
