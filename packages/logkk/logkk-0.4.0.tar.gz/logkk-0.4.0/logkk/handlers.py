import threading
from abc import ABC

file_lock = threading.Lock()
stream_lock = threading.Lock()


class Handler(ABC):

    def write(self, content):
        pass


class StreamHandler(Handler):

    def write(self, content):
        with stream_lock:
            print(content)


class FileHandler(Handler):

    def __init__(self, filepath, encoding="utf8"):
        self.filepath = filepath
        self.encoding = encoding
        self.file_obj = None

    def write(self, content):
        with file_lock:
            if not self.file_obj:
                self.file_obj = open(file=self.filepath,
                                     mode="a+",
                                     encoding=self.encoding)
            self.file_obj.write(content + "\n")
            self.file_obj.flush()

    def close(self):
        self.file_obj.close()
