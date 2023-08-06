import collections
from hashlib import md5
from typing import OrderedDict, Any, Dict


#######################################################
#  LRU
#######################################################
class LRU:
    __size: int = None
    __evict = None
    __lru_cache: OrderedDict[str, Any] = None

    # ------------------------------------------------------------------------
    def __init__(self, size, evict=None):
        self.__size = size
        self.__lru_cache = collections.OrderedDict()
        self.__evict = evict

    # ------------------------------------------------------------------------
    def get(self, key: str, default=None):
        try:
            value = self.__lru_cache.pop(key)
            self.__lru_cache[key] = value
            return value
        except KeyError:
            return default

    # ------------------------------------------------------------------------
    def put(self, key: str, value: Any):
        try:
            self.__lru_cache.pop(key)
        except KeyError:
            if len(self.__lru_cache) >= self.__size:
                _key, _val = self.__lru_cache.popitem(last=False)
                if self.__evict is not None:
                    self.__evict(_val)
        self.__lru_cache[key] = value

    # ------------------------------------------------------------------------
    def rem(self, key: str):
        if self.__lru_cache[key] is not None:
            del self.__lru_cache[key]


#######################################################
#  Change detector
#######################################################
class ChangeDetector:
    changes = LRU(500)

    @classmethod
    def is_changed(cls, name, content, serializer=None):
        if content is not None:
            content = serializer(content) if serializer is not None else content
        else:
            content = ''
        content_hash = cls.changes.get(name)
        new_content_hash = md5(str(content).encode('utf-8')).hexdigest()
        cls.changes.put(name, new_content_hash)
        return content_hash != new_content_hash


#######################################################
#  Change detector
#######################################################
class SchemaUtil:

    @staticmethod
    def create(instance: Any, data: Dict[Any, Any]):
        for key in data:
            instance.__setattr__(key, data[key])
        return instance
