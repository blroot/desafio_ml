# BI ML Technical Challenge

## Quick Start

Los contenedores exponen los puertos 5000 para flask y 5432 para la base de datos postgres

Para levantar el proyecto con docker-compose, en la raíz del proyecto:

```
docker-compose up -d
```

Abrir [upload.html](upload.html) y subir el csv, si todo va bien el servidor nos va a responder con el id del upload, con ese id, por ejemplo 1, podemos ir a [http://localhost:5000/uploadstatus/1](http://localhost:5000/uploadstatus/1)
 nos va a mostrar el estado del proceso.
 
## Decisiones de diseño

El proyecto está hecho con varios contenedores docker:

- app flask
- postgres
- rabbitmq
- celery worker

### Dependencias

- flask
- flask-sqlalchemy
- python-dotenv
- psycopg2
- aiohttp
- celery

Se decidió utilizar celery y rabbitmq para correr la tarea en background y no dejar abierto el request del usuario que sube el archivo.

### Abstracción de la API de ML

En el módulo HTTPApi, se diseñó una abstracción para poder consultar al backend de Meli, se pensó en una clase Endpoint en donde cada uno tiene su propio caché, donde se guardan los resultados de las consultas.
Para el endpoint de items se aprovechó el multiget de 20 items simultaneos para optimizar las consultas.
Se utiliza un semáforo configurable para evitar sobrecargar los recursos de red del sistema operativo y/o ser limitados por el backend.

### Módulo filereader

Se diseñaron los parsers para diferentes tipos de archivos (CSV, JsonLines, txt) se cargan en runtime mediante el patrón factory

```
parser_factory = StreamParserFactory(delimiter=Config.DELIMITER)
parser_factory.register_parser('csv', CsvParser)
parser_factory.register_parser('jsonl', JsonLinesParser)
parser_factory.register_parser('txt', TxtParser)
```

La clase FileReader se construye con un objeto StreamParserFactory, una subclase Record y un nombre de archivo, se definen métodos para leer el archivo indicado linea a linea y para borrarlo.
Utiliza los parsers para parsear y construír un Record con cada una.

Cada parser implementa dos métodos por herencia:

- reader(file_object): se encarga de parsear una linea del archivo, retorna un generador, para csv, adapta csv.reader
- build_record(values, record_class): devuelve un Record con los valores y la clase que hereda de Record que le pasamos

### Flask app

En el módulo fileupload se encuentra la app de flask, 

### Módulo record

El proceso se pensó como un pipeline por etapas, en cada etapa se pueden hacer consultas a la API de mercadolibre mediante las abstracciones diseñadas para tal fin, es importante remarcar que el resultado de la consulta siempre va a estar disponible una etapa mas tarde en la caché del endpoint, esto permite agrupar las consultas del mismo tipo para todos los records para poder hacer los pedidos a la api de manera asincrónica, logrando una aceleración importante.

#### Record 

Es la clase base para un record, es lo que usamos para modelar nuestro pipeline, se construye con los datos que nos entrega el Parser

Por ejemplo, para el ejercicio, en la clase SiteIdPriceStartTimeNameDescriptionNicknameRecord creamos dos métodos que representan dos etapas:
 
 - retrieve_item 
 - retrieve_all_details 
 
estos métodos deben retornar una lista con todos los resultados de MLApi.Endpoint.get():
 
 ```
     def retrieve_item(self, ml_api: MLApi) -> Iterable[Tuple] or None:
        if not self._id_valid() or not self._site_valid():
            self.cancel_pipeline()
            return

        item_async = ml_api.items.get(item_id=self._item_id(),
                                      extra_args='attributes=price,start_time,currency_id,category_id,seller_id')
        return [item_async]
 ```
Dicha lista va a ser utilizada por el RecordPool para unificar todas las consultas.

Si se necesita interrumpir la ejecución en alguna etapa, se llama a cancel_pipeline() y se retorna.

En la etapa siguiente, se puede leer el resultado de dicha consulta con get_from_cache():
 
```
    def retrieve_all_details(self, ml_api: MLApi) -> Iterable or None:
        item = ml_api.items.get_from_cache(item_id=self._item_id())
        ....
```

Para cargar los métodos que creamos como etapas, lo indicamos mediante load_stages():

```
    def load_stages(self) -> None:
        self.tasks_pipeline = self.retrieve_item, self.retrieve_all_details
```

Luego, como siempre tenemos end_pipeline y save donde se guardan los datos en BD.

#### RecordPool 

Es una clase que agrupa los records y desde aquí se corre todo el pipeline y se guardan todos los resultados en BD.
 
En el método run_all_pipelines() 

![](recordpool.jpg)
