import re
from typing import List
from datetime import datetime

from logkk.level import Level
from logkk.handlers import Handler, StreamHandler


class Logger(object):
    """
    记录日志的实际操作者，可以理解为worker
    """

    def __init__(self, name, level=Level.INFO, fmt=None, handlers=None):
        self.name = name
        self.level = level
        self.fmt = fmt
        self.handlers: List[Handler] = handlers if handlers else []
        self._datetime_fmt = "%Y-%m-%d %H:%M:%S"
        self._default_handler = StreamHandler()

    def _get_content(self, level, *args, **kwargs):
        """组装日志内容"""
        keys = re.findall(r"{(\w+)}", self.fmt)
        data = dict()
        for key in keys:
            if key == "message":
                data[key] = self._get_message(*args, **kwargs)
                continue
            if key == "level":
                data[key] = level.upper()
                continue
            data[key] = getattr(self, f"_get_{key}")()
        content = self.fmt.format(**data)
        return content

    def _get_name(self):
        return self.name

    def _get_datetime(self):
        return datetime.now().strftime(self._datetime_fmt)

    @staticmethod
    def _get_message(*args, **kwargs):
        message = " ".join([str(arg) for arg in args])
        for key, val in kwargs.items():
            message += f" {key}={val}"
        return message

    def _write(self, level, *args, **kwargs):
        content = self._get_content(level, *args, **kwargs)
        if self.handlers:
            for handler in self.handlers:
                handler.write(content)
        else:
            self._default_handler.write(content)

    def debug(self, *args, **kwargs):
        if self.level > Level.DEBUG:
            return
        self._write("debug", *args, **kwargs)

    def info(self, *args, **kwargs):
        if self.level > Level.INFO:
            return
        self._write("info", *args, **kwargs)

    def warn(self, *args, **kwargs):
        if self.level > Level.WARNING:
            return
        self._write("warn", *args, **kwargs)

    def error(self, *args, **kwargs):
        if self.level > Level.ERROR:
            return
        self._write("error", *args, **kwargs)
