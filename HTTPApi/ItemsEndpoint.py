from .Endpoint import Endpoint


class ItemsEndpoint(Endpoint):
    def __init__(self, url, path):
        super().__init__(url, path)
        self._item_counter = 0
        self._total_requests_pending = 0
        self._total_completed = 0
        self._multiget_url = self.url + '/' + self.path + '?ids='
        self.urls = []

    def get(self, item_id, extra_args=None):
        self._total_requests_pending += 1
        return self.cr_get, item_id, extra_args

    async def cr_get(self, session, item_id=None, extra_args=None):
        self._multiget_url += "," + item_id
        self._item_counter += 1
        self._total_requests_pending -= 1

        if self._item_counter == 20 or self._total_requests_pending == 0:
            if extra_args:
                self._multiget_url += '&id,' + extra_args

            self.urls.append(self._multiget_url)
            cached_object = self.cache.get(item_id, None)

            local_multiget_url = self._multiget_url
            self._multiget_url = self.url + '/' + self.path + '?ids='
            self._item_counter = 0

            if cached_object is None:
                resp = await session.get(local_multiget_url)
                items = await resp.json()

                for i in items:
                    item_id = i['body']['id']
                    self.cache[item_id] = i
