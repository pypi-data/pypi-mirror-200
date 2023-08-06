import requests


class HttpHandlerError(Exception):
    def __init__(self, r: requests.Response):
        super().__init__(f"post log error, url={r.url}, status_code={r.status_code}, text={r.text}")
