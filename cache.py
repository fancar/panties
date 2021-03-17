import asyncio
import json
import time

# main cache
# cache = []

# units managed by master
# master_units = set()
# cache_lock = asyncio.Lock()

class Cache:
    def __init__(self,logger,ttl=300):
        self._log = logger
        self.cnt = 0

        self._data = {} # {"id" : "xxx" {"ts" : "3434" data : {} }}
        self._ttl = ttl

        self._last_time = time.time()
        self._main_key = 'id'
        self._master_content = set()
        self._master_last_ts = time.time()


    # @property
    def item(self,item_id):
        print("item_id ",item_id)
        item = self._data.get(item_id.upper())
        print("item ",item)
        if item is None:
            return
        return item["data"]

    @property
    def data(self):
        self.check_ttl()
        return [self._data[d]["data"] for d in self._data]

    @data.setter
    def data(self, value):
        self._data = value

    def save_data(self,value, master=False):
        """ master contains the values that can not be overwriten by others """
        self.check_ttl()

        if type(value) is str:
            value = json.loads(value)

        if type(value) is dict:
            if "result" not in value:
                raise Exception(f'Can not cache data. Recieved data must be dumped as list of dicts or contain "result" key with list. Got {type(value)} ')
            value = value["result"]    

        if master:
            self._master_content = set()
            self._master_last_ts = time.time()

        result = {}
        for d in value:
            if type(d) is not dict:
                raise Exception(f'[cache] Can not cache data. Recieved text must be dumped as list of dicts. Got {type(value)}')

            if self._main_key not in d:
                raise Exception(f"[cache] every dict in list must contain key: {self._main_key}")

            gwid = d[self._main_key] = d[self._main_key].upper()
            if master:
                self._master_content.add(gwid)

            elif gwid in self._master_content:
                    self._log.debug(f'[cache] data for "{gwid}" skipped as it handles by master')
                    continue

            result[d[self._main_key]] = {
                "ts" : time.time(),
                "data" : d,
            }

        self._log.debug(f"[cache] recieved NEW data that contains ({len(result)} items): ")

        for k in self._data:
            if k not in result:
                if self._ttl + self._data[k]["ts"] < time.time():
                    self._log.debug(f"[cache] removed old data (id: {k})")
                else:
                    result[k] = self._data[k]

        print("self._master_content",self._master_content)
        self._last_time = time.time()
        self._log.info(f"[cache] saved ({len(result)} items)")
        self._data = result

    def check_ttl(self):
        if self._ttl*2 + self._last_time < time.time() and self._data:
            self._log.warning(f'[cache] Data in cache is too old (last ts: {self._last_time}). Cleaning up cache ...')
            self._data = []

        if self._ttl*2 + self._master_last_ts < time.time() and self._master_content:
            self._log.warning(f'[cache] Data in cache for master is too old (last ts: {self._master_last_ts}). Cleaning up cache ...')
            self._master_content = set()
            

    @data.deleter
    def data(self):
        del self._data        

    async def getCnt(self):
        return self.cnt


