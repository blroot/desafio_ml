from HTTPApi.Exceptions import ApiConnectionError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client import ClientSession


class Endpoint:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self.cache = {}

    def purge_cache(self):
        self.cache = {}

    def get(self, element_id: str, extra_args: str = None):
        return self.cr_get, element_id, extra_args

    async def cr_get(self, session: ClientSession, element_id: str = None, extra_args: str = None):
        url = self.url + '/' + self.path + '/' + str(element_id)

        if extra_args:
            url += '?' + extra_args

        cached_object = self.cache.get(url, None)
        if cached_object is None:
            try:
                resp = await session.get(url)
            except ClientConnectorError:
                raise ApiConnectionError(self.url)
            self.cache[element_id] = await resp.json()

    def get_from_cache(self, element_id: str = None):
        return self.cache.get(element_id, None)

