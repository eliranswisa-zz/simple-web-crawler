from persistqueue import Queue
import os
from queue_interface import QueueInterface


class CrawlerQueue(QueueInterface):
    def __init__(self, id, depth):
        self.base = './db'
        self.queue = self.__retrieve_queue(id, depth)

    def put(self, url, depth):
        self.queue.put({'url': url, 'depth': depth})

    def get(self):
        item = self.queue.get()
        return item

    def is_empty(self):
        return self.queue.qsize() == 0

    def commit(self):
        self.queue.task_done()

    def __retrieve_queue(self, id, depth):
        return Queue(os.path.join(self.base, id + '-' + str(depth)))
