from .Endpoint import Endpoint
from HTTPApi.Exceptions import ApiConnectionError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client import ClientSession


class ItemsEndpoint(Endpoint):
    def __init__(self, url: str, path: str):
        super().__init__(url, path)
        self._item_counter = 0
        self._total_requests_pending = 0
        self._total_completed = 0
        self._multiget_url = self.url + '/' + self.path + '?ids='
        self.urls = []

    def get(self, element_id: str, extra_args: str = None):
        self._total_requests_pending += 1
        return self.cr_get, element_id, extra_args

    async def cr_get(self, session: ClientSession, element_id: str = None, extra_args: str = None):
        self._multiget_url += "," + element_id
        self._item_counter += 1
        self._total_requests_pending -= 1

        if self._item_counter == 20 or self._total_requests_pending == 0:
            if extra_args:
                self._multiget_url += '&id,' + extra_args

            self.urls.append(self._multiget_url)
            cached_object = self.cache.get(element_id, None)

            local_multiget_url = self._multiget_url
            self._multiget_url = self.url + '/' + self.path + '?ids='
            self._item_counter = 0

            if cached_object is None:
                try:
                    resp = await session.get(local_multiget_url)
                except ClientConnectorError:
                    raise ApiConnectionError(self.url)
                items = await resp.json()

                for i in items:
                    element_id = i['body']['id']
                    self.cache[element_id] = i
