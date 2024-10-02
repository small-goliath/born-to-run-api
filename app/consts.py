from enum import Enum

class Bucket(str, Enum):
    PROFILE = "profile"
    FEED = "feed"