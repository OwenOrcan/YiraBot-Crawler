class HTTPError(Exception):
    def __init__(self, url):
        self.url = url
        self.message = f"HTTP Error Occured: {self.url}"
        super().__init__(self.message)


class ConnectionError(Exception):
    def __init__(self, url):
        self.url = url
        self.message = f"Connection Error Occured: {self.url}"
        super().__init__(self.message)


class TimeoutError(Exception):
    def __init__(self, url):
        self.url = url
        self.message = f"Timeout Error Occured: {self.url}"
        super().__init__(self.message)


class RequestError(Exception):
    def __init__(self, url):
        self.url = url
        self.message = f"Request Error Occured: {self.url}"

        super().__init__(self.message)
