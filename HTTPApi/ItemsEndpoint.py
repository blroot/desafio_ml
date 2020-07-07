from .Endpoint import Endpoint
from urllib.parse import urlencode


class ItemsEndpoint(Endpoint):
    async def cr_get(self, session, item_id=None, cache=False):
        url = self.url + '/' + self.path + '?ids=' + item_id

        if cache:
            cached_object = self.cache.get(url, None)
            if cached_object is None:
                resp = await session.get(url)
                self.cache[item_id] = await resp.json()

            return url, self.cache[item_id]

        resp = await session.get(url)
        out = await resp.json()

        return url, out
