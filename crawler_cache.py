import sqlite3
import filesystem

from cache_interface import CacheInterface


class CrawlerCache(CacheInterface):

    def __init__(self):
        filesystem.create_directory('./db/')
        self.conn = sqlite3.connect('./db/cache.db')
        self.init_cache()

    def init_cache(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS visited_urls
                        (url TEXT PRIMARY KEY, ratio TEXT, modified INTEGER)''')

    def cache_url(self, id, ratio, last_modified):
        self.conn.execute('INSERT OR REPLACE INTO visited_urls VALUES(?,?,?)', (id, str(ratio), last_modified,))
        self.conn.commit()

    def is_visited(self, id):
        results = self.conn.execute('SELECT COUNT(1) FROM visited_urls WHERE url = ?', (id,))
        count = results.fetchone()[0]
        return count

    def get_last_modified(self, id):
        results = self.conn.execute('SELECT modified FROM visited_urls WHERE url = ?', (id,))
        data = results.fetchone()[0]
        return data

    def get_ratio(self, id):
        results = self.conn.execute('SELECT ratio FROM visited_urls WHERE url = ?', (id,))
        data = results.fetchone()[0]
        return data
