import aiohttp


class Endpoint:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        self.cache = {}

    def get(self, item_id):
        return self.cr_get, item_id

    async def cr_get(self, session, item_id=None):
        url = self.url + '/' + self.path + '/' + str(item_id)

        cached_object = self.cache.get(url, None)
        if cached_object is None:
            resp = await session.get(url)
            self.cache[item_id] = await resp.json()

    def get_from_cache(self, item_id=None):
        return self.cache.get(item_id, None)

