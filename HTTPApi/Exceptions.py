class ApiConnectionError(Exception):
    def __init__(self, url: str):
        self.url = url

    def __str__(self):
        return "Error while fetching API with URL: " + self.url
