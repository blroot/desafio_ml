import aiohttp


class Endpoint:
    def __init__(self, url, path):
        self.url = url
        self.path = path
        self.cache = {}

    def get(self, item_id, cache=False):
        return self.cr_get, item_id, cache

    async def cr_get(self, session, item_id=None, cache=False):
        url = self.url + '/' + self.path + '/' + str(item_id)

        if cache:
            cached_object = self.cache.get(url, None)
            if cached_object is None:
                resp = await session.get(url)
                self.cache[item_id] = await resp.json()

            return url, self.cache[item_id]

        resp = await session.get(url)
        out = await resp.json()

        return url, out

    def get_from_cache(self, item_id=None):
        return self.cache.get(item_id, None)

