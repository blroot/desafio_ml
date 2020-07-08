from .Endpoint import Endpoint


class ItemsEndpoint(Endpoint):
    def __init__(self, url, path):
        self.item_counter = 0
        super().__init__(url, path)

    async def cr_get(self, session, item_id=None):
        url = self.url + '/' + self.path + '?ids=' + item_id

        cached_object = self.cache.get(url, None)
        if cached_object is None:
            resp = await session.get(url)
            self.cache[item_id] = await resp.json()
