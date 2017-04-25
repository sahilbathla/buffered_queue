import redis

class RedisQueue(object):
    """Simple Queue with Redis Backend"""
    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db= redis.Redis(**redis_kwargs)
        self.original_key = name
        self.key = '%s:%s' %(namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def get_all(self):
        """Return all elements of the queue."""
        return self.__db.lrange(self.key, 0, -1)

    def get_key(self):
        """Get the key of current queue."""
        return self.original_key

    def get_limit(self):
        """Get the limit of current queue."""
        return int(self.__db.get("%s:limit" % self.original_key) or 0)

    def get_topic(self):
        """Get the limit of current queue."""
        return self.__db.get("%s:topic" % self.original_key)

    def is_empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def empty(self):
        """Empty the queue."""
        self.__db.delete(self.key)

    def put(self, item):
        """Put item into the queue."""
        self.__db.lpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)