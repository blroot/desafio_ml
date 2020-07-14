from HTTPApi.Exceptions import ApiConnectionError
from aiohttp.client_exceptions import ClientConnectorError
from aiohttp.client import ClientSession


class Endpoint:
    def __init__(self, url: str, path: str):
        self.url = url
        self.path = path
        self.cache = {}

    def purge_cache(self):
        """
        Vacía la caché del Endpoint
        """
        self.cache = {}

    def get(self, element_id: str, extra_args: str = None):
        """
        Se utiliza para pedir una consulta al backend, pero no devuelve la respuesta del servidor sinó lo necesario para ejecutar la función asincrónica que lo hace

        :param element_id: Identificador del elemento que vamos a pedir al endpoint de la API
        :param extra_args: Para pasarle argumentos extra a la url
        :return: Tupla con función asincrónica y sus argumentos
        """
        return self.cr_get, element_id, extra_args

    async def cr_get(self, session: ClientSession, element_id: str = None, extra_args: str = None):
        """
        Función asíncrónica para hacer una consulta al backend o traerlo de caché si se encuentra

        :rtype: None
        :param session: Una sesión abierta de aiohttp
        :param element_id: Identificador del elemento que vamos a pedir al endpoint de la API
        :param extra_args: Para pasarle argumentos extra a la url
        :raises ApiConnectionError: Si ocurre un error al conectar al backend
        """
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
        """
        Para consultar a la caché por un elemento

        :param element_id: Identificador del elemento que pedimos con anterioridad a la API
        :return: Diccionario con respuesta del backend
        """
        return self.cache.get(element_id, None)

