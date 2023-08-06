from dataclasses import dataclass


@dataclass
class Level(object):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
