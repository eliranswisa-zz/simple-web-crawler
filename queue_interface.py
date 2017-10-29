from abc import ABC


class QueueInterface(ABC):
    """
        Interface for interacting with a queue.
    """
    def __init__(self):
        """
            Instantiate a queue object
        """
        raise NotImplementedError("__init__ should have been implemented.")

    def put(self, url, depth):
        """
            Inserts an item to the queue. Data as [url, depth]
        :param url: The URL
        :param depth: The depth in which the URL was found
        """
        raise NotImplementedError("put should have been implemented.")

    def get(self):
        """
            Gets the first item in the queue, while keeping it there.
        :return: Item as [url, depth] from the queue
        """
        raise NotImplementedError("get should have been implemented.")

    def is_empty(self):
        """
            Checks if the queue is empty
        :return: True if the queue is empty, False otherwise.
        """
        raise NotImplementedError("is_empty should have been implemented.")

    def commit(self):
        """
            Removes the item from the queue.
            Should be called once all the tasks were done for a specific item.
        """
        raise NotImplementedError("commit should have been implemented.")

