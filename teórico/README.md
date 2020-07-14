# Desafío Teórico
## Consigna

### Procesos, hilos y corrutinas
- Un caso en el que usarías procesos para resolver un problema y por qué.

Cuando necesito aprovechar al máximo todos los CPUs y/o núcleos que tengo disponible, y el problema es divisible en partes que puedan correr en paralelo, por ejemplo un programa que corre un modelo matemático complejo.

- Un caso en el que usarías threads para resolver un problema y por qué.

En una aplicación que interactúa con el usuario y necesito lograr interactividad al efectuar varias tareas, por ejemplo en un carrito de compra, se podrían ejecutar en varios threads el proceso de pago, el guardado de la transaccion en la base de datos, el envío del email de compra, etc. Es entrada salida pero no tan masiva como en el caso de corrutinas.

- Un caso en el que usarías corrutinas para resolver un problema y por qué.

Cuando la mayor parte del tiempo de la ejecución de un programa se invierte en entrada/salida, por ejemplo, cuando necesitamos hacer muchas peticiones de red a un servidor. Tiene la ventaja que no se necesitan crear mas procesos o threads, ocupando mas recursos de hardware.


### Optimización de recursos del sistema operativo
Si tuvieras 1.000.000 de elementos y tuvieras que consultar para cada uno de ellos
información en una API HTTP. ¿Cómo lo harías? Explicar.

De la misma forma que se realizó en el trabajo, utilizando corrutinas que permitan eliminar el bloqueo al esperar la respuesta del servidor, siempre utilizando un semáforo contador para permitir acceder a los recursos de red a una cantidad determinada de llamadas, ya que de otra manera vamos a tener problemas por el lado de nuestro SO y/o del lado del servidor podría haber algún limite en cuanto a conexiones abiertas.