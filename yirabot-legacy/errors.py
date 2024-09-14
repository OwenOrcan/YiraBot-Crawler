class HTTPError(Exception):
    """Exception raised for HTTP errors."""

    def __init__(self, code):
        """Initializes the exception with an HTTP status code.

        Args:
            code (int): The HTTP status code that caused the error.
        """
        self.code = code
        self.message = f"HTTP Error Occurred: {self.code}"
        super().__init__(self.message)


class ConnectionError(Exception):
    """Exception raised for errors in establishing a connection."""

    def __init__(self, url):
        """Initializes the exception with the URL that failed to connect.

        Args:
            url (str): The URL connection to which failed.
        """
        self.url = url
        self.message = f"Connection Error Occurred: {self.url}"
        super().__init__(self.message)


class TimeoutError(Exception):
    """Exception raised for timeout errors."""

    def __init__(self, url):
        """Initializes the exception with the URL that timed out.

        Args:
            url (str): The URL that experienced a timeout.
        """
        self.url = url
        self.message = f"Timeout Error Occurred: {self.url}"
        super().__init__(self.message)


class RequestError(Exception):
    """Exception raised for errors during a request."""

    def __init__(self, url):
        """Initializes the exception with the URL where the request error occurred.

        Args:
            url (str): The URL that experienced a request error.
        """
        self.url = url
        self.message = f"Request Error Occurred: {self.url}"
        super().__init__(self.message)


class RobotsError(Exception):
    """Exception raised for robots.txt blocking errors."""

    def __init__(self, url):
        """Initializes the exception with the URL blocked by robots.txt.

        Args:
            url (str): The URL that is blocked by robots.txt.
        """
        self.url = url
        self.message = f"{self.url} Does Not Allow Crawling (Blocked By robots.txt)"
        super().__init__(self.message)
