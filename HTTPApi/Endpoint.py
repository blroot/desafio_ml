class Endpoint:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        self.cache = {}

    def purge_cache(self):
        self.cache = {}

    def get(self, item_id, extra_args=None):
        return self.cr_get, item_id, extra_args

    async def cr_get(self, session, item_id=None, extra_args=None):
        url = self.url + '/' + self.path + '/' + str(item_id)

        if extra_args:
            url += '?' + extra_args

        cached_object = self.cache.get(url, None)
        if cached_object is None:
            resp = await session.get(url)
            self.cache[item_id] = await resp.json()

    def get_from_cache(self, item_id=None):
        return self.cache.get(item_id, None)

