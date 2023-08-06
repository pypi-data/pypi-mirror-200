import logging
import os
import traceback
from typing import Any, Dict

import pickledb

from openfabric_pysdk.utility import LRU


#######################################################
#  KeyValueDB
#######################################################
class KeyValueDB:
    __name: str = None
    __db_path: str = None
    __autodump: bool = None
    __db: pickledb.PickleDB = None

    # ------------------------------------------------------------------------
    def __init__(self, name: str, path: str = None, autodump: bool = False):

        if path is None:
            path = f"{os.getcwd()}"

        if not os.path.exists(path):
            os.makedirs(path)

        self.__name = name
        self.__autodump = autodump
        self.__db_path = f"{path}/{name}.json"
        try:
            self.__db = pickledb.load(self.__db_path, False, sig=False)
        except:
            logging.error(f"Openfabric - store {self.__db_path} is corrupted, recreate it")
            os.remove(self.__db_path)
            traceback.print_exc()
            self.__db = pickledb.load(self.__db_path, False, sig=False)

    # ------------------------------------------------------------------------
    def exists(self, key: str):
        return self.__db.exists(key)

    # ---------------------------`---------------------------------------------
    def rem(self, key: str):
        self.__db.rem(key)
        if self.__autodump:
            self.dump()

    # ---------------------------`---------------------------------------------
    def drop(self):
        self.__db.deldb()
        if os.path.isfile(self.__db_path):
            os.remove(self.__db_path)

    # ------------------------------------------------------------------------
    def get(self, key: str):
        return self.__db.get(key)

    # ------------------------------------------------------------------------
    def keys(self):
        return self.__db.getall()

    # ------------------------------------------------------------------------
    def set(self, key: str, val: Any):
        self.__db.set(key, val)
        if self.__autodump:
            self.dump()

    # ------------------------------------------------------------------------
    def dump(self):
        self.__db.dump()

    # ------------------------------------------------------------------------
    def all(self) -> Dict[str, Any]:
        return self.__db.db


#######################################################
#  Store
#######################################################
class Store:
    __path: str = None
    __kvdbs: LRU = None
    __autodump: bool = None

    # ------------------------------------------------------------------------
    def __init__(self, path: str = None, autodump: bool = False):
        self.__path = path
        self.__autodump = autodump
        self.__kvdbs = LRU(10, self.dump)

    # ------------------------------------------------------------------------
    def dump(self, kvdb: KeyValueDB):
        logging.debug(f"Openfabric - evicting {kvdb}")
        kvdb.dump()

    # ------------------------------------------------------------------------
    def get(self, name, key, default=None) -> Any:
        kvdb = self.__instance(name)
        value = kvdb.get(key)
        if value:
            return value
        else:
            return default

    # ------------------------------------------------------------------------
    def set(self, name: str, key: str, val: Any):
        kvdb = self.__instance(name)
        kvdb.set(key, val)

    # ------------------------------------------------------------------------
    def rem(self, name: str, key: str):
        kvdb = self.__instance(name)
        kvdb.rem(key)

    # ------------------------------------------------------------------------
    def drop(self, name: str):
        kvdb = self.__instance(name)
        self.__kvdbs.rem(name)
        kvdb.drop()

    # ------------------------------------------------------------------------
    def all(self, name: str) -> Dict[str, Any]:
        kvdb = self.__instance(name)
        return kvdb.all()

    # ------------------------------------------------------------------------
    def __instance(self, name: str) -> KeyValueDB:
        kvdb = self.__kvdbs.get(name, None)
        if kvdb is None:
            kvdb = KeyValueDB(f"{name}", path=self.__path, autodump=self.__autodump)
            self.__kvdbs.put(name, kvdb)
        return kvdb
