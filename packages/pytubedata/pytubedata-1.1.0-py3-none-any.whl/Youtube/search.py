# https://developers.google.com/youtube/v3/docs/search
from enum import Enum
from .api_mapper import API_MAPPER
from copy import deepcopy
class ChannelType(Enum):

    ANY = 'any'
    SHOW = 'show'

class EventType(Enum):

    COMPLETED = 'completed'
    LIVE = 'live'
    UPCOMING = 'upcoming'

class Sort(Enum):

    DATE = 'date'
    RATING = 'rating'
    RELEVANCE = 'relevance'
    TITLE = 'title'
    VIDEO_COUNT = 'videoCount'
    VIEW_COUNT = 'viewCount'

class SearchType(Enum):

    CHANNEL = 'channel'
    PLAYLIST = 'playlist'
    VIDEO = 'video'

class Search(ChannelType, EventType, Sort, SearchType):
    """
    The search class handles the methods to make search queries on Youtube using YouTube Data API
    """

    def __init__(self):
        pass


