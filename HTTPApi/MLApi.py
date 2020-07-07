from HTTPApi.Endpoint import Endpoint
from HTTPApi.ItemsEndpoint import ItemsEndpoint


class MLApi:
    def __init__(self, url):
        self.url = url
        self.items = ItemsEndpoint(url, 'items')
        self.currencies = Endpoint(url, 'currencies')
        self.categories = Endpoint(url, 'categories')
        self.users = Endpoint(url, 'users')
