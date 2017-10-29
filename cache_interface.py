from abc import ABC


class CacheInterface(ABC):
    """
        Interface for interacting with a cache.
    """
    def __init__(self):
        """
            Instantiate a cache object
        """
        raise NotImplementedError("__init__ should have been implemented.")

    def init_cache(self):
        """
            Create the cache metadata if needed.
        """
        raise NotImplementedError("init_cache should have been implemented.")

    def cache_url(self, id, ratio, last_modified):
        """
            Caches the URL and its data.
        :param id: The URL
        :param ratio: Same domain ratio
        :param last_modified: Last time the URL was accessed as EPOCH.
        """
        raise NotImplementedError("cache_url should have been implemented.")

    def is_visited(self, id):
        """
            Checks if the URL was visited.
        :param id: The URL
        :return: True if the URL was visited, False otherwise.
        """
        raise NotImplementedError("is_visited should have been implemented.")

    def get_last_modified(self, id):
        """
            Returns the last modified for a specific URL
        :param id: The URL
        :return: Last modified date as EPOCH.
        """
        raise NotImplementedError("get_last_modified should have been implemented.")

    def get_ratio(self, id):
        """
            Returns the same domain ratio of a specific URL
        :param id: The URL
        :return: Same domain ratio in the page.
        """
        raise NotImplementedError("get_ratio should have been implemented.")