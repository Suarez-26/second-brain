---
fecha: "2026-01-22"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "A_YNPDhz-7Q"
canal: "Kevin Alejandro Tarazona"
duracion: "N/A"
vistas: 7
url: "https://www.youtube.com/watch?v=A_YNPDhz-7Q"
---

# Biblioteca campuslands

- **Canal:** Kevin Alejandro Tarazona
- **Fecha de subida:** 2026-01-22
- **Duración:** N/A
- **Vistas:** 7
- **URL:** https://www.youtube.com/watch?v=A_YNPDhz-7Q

## Descripción del Video
```text

```

## Transcripción de Audio / Subtítulos

[00:00] Este ejercicio consta de un sistema para
gestionar los recursos de la biblioteca
[00:03] aplicando los principios de programación
orientado a objetos. El objetivo es
[00:07] modelar libros y revistas, permitir su
préstamo búsqueda de administración
[00:11] utilizando conceptos básicos como
extracción, herencia, encapsulamiento,
[00:15] polimorfismo e interfaces.
Lo primero que se hace es definir la
[00:19] clase abstracta recurso que representa
cualquier elemento que pueda existir en
[00:22] la biblioteca. Esta clase encapsula los
atributos comunes a todos los recursos,
[00:27] los cuales son ID, título
y disponible.
[00:34] Los atributos son privados para aplicar
encapsulamiento y se acceden a ellos
[00:37] mediante los métodos get
ander.
[00:44] Al ser abstracta, recurso no se
instancia directamente, sino que sirve
[00:47] como base para tipos más específicos
como libros o revistas. Esto aplica bien
[00:53] el principio de abstracción, ya que ya
que modera el concepto general de lo que
[00:57] es un recurso bibliográfico.
[01:03] ¿Para qué se decidió de que recurso
fuera abstracta? Ya que hay dos clases
[01:09] que van a agregar de él, lo que es libro
y revista. Entonces, ¿esto qué hace?
[01:14] Esto evita de que una persona pueda
crear directamente un recurso, sino que
[01:18] tenga que crear o un libro o una revista
para poder ahí sí este ingresar a la
[01:23] biblioteca.
Entonces, seguimos con lo que es la
[01:27] clase,
las clases quean, lo que es libro y
[01:30] revista. Entonces, empezaremos eh con lo
que fue con lo que es libro. Entonces,
[01:37] libro, ¿qué hace libro? Primero que todo
hay que establecerlo de extensidad
[01:42] de recurso y él tiene su propio eh campo
adicional, campo propio, el cual es el
[01:49] autor. Entonces, hay que crear el
constructor llamando al sú y aplicando
[01:55] la nueva el nuevo campo que es autor y
se hace prácticamente lo mismo que que
[02:01] recursos los ge, además de un two string
para poder personalizar mejor la lo que
[02:07] es la la impresión del del objeto en sí.
En este caso pues sería el libro con su
[02:13] ID, subtítulo, su autor y su
disponibilidad.
[02:16] Lo mismo con revista. revista, el cual
tiene dos nuevos campos, su campo propio
[02:22] llamado número y su siguiente campo
llamado tipo. ¿Y tipo, ¿qué es tipo? Es
[02:27] un tipo revista. En este caso, tipo
revista va a ser una numeración. ¿Para
[02:31] qué? Para evitar este que hayan campos
que se escriban mal. Por ejemplo, no sé,
[02:38] investigación, unos escriben con i
minúscula, otros con i mayúscula, otros
[02:42] con títulos. con títulos, no, perdón,
con tildes. Entonces, en este caso se
[02:46] coloca enum poder para poder mantener lo
que es una consistencia en la
[02:50] información.
[02:54] Lo mismo, se crea el que el constructor
y se agrega los campos propios, bueno,
[03:01] además del súper que tiene lo que es ID,
título indisponible y también sus gear
[03:06] seter y el to stream.
Ahora vamos con lo que son los
[03:12] servicios. En este caso sería el
servicio de biblioteca que va a ser
[03:15] dividida en dos. La interfaz, la cual es
la que
[03:20] eh define los métodos que se va que va a
tener la biblioteca.
[03:24] En este caso va a ser agregar recurso,
prestar recurso y buscar recurso por
[03:27] título. Y esto se va a utilizar por
medio de la biblioteca, ya que la
[03:31] biblioteca lo que va a hacer es llamar a
la interfaz, decir, voy a realizar estos
[03:36] métodos y ahora sí proceder con la
lógica. En este caso
[03:42] está el método agregar recursos. lo que
lo que va a hacer es pedir la pedir la
[03:47] nueva el recurso nuevo y añadirlo.
[03:55] El siguiente método va a ser prestar el
recurso. Lo que va a hacer es buscar
[03:59] entre los recursos el que tenga su ID.
En caso de ser ID, pues directamente el
[04:04] recurso pasa a ser false. El recurso,
perdón, el valor
[04:10] disponible del recurso, pues va a pasar
a ser f. false y retorna true. Retorna
[04:16] true en caso de que primero se consiga
el
[04:20] recurso con el ID y su recurso sea
disponible.
[04:24] Entonces, hay dos casos en los cuales
puede retornar false, o sea, que no se
[04:28] puede prestar. El primero es en caso de
que el recurso y con el ID no que no no
[04:35] se encuentre o que se encuentre el
recurso con ese ID proporcionado, pero
[04:40] su disponibilidad, bueno, su valor
disponible sea false. Entonces por eso
[04:45] se realiza esta validación de que
recurso. Get id, o sea, que el ID sea
[04:49] igual al que se proporcionó y su
disponibilidad sea true. En caso de que
[04:53] alguno de los dos falle, pues
directamente pasa al siguiente recurso y
[04:58] en caso de que recorra todos los
elementos y no se consiga ningún ID con
[05:03] ningún recurso con ese ID y cuyo valor
de disponible sea true, pues
[05:07] directamente va a retornar false.
Y está el método buscar recurso por
[05:13] título. El método buscar recurso por
título, lo que va a hacer es
[05:17] eh recorrer, bueno, primero que todo se
declara una lista de recursos
[05:20] encontrados porque pueden haber varios
recursos con el mismo nombre. Entonces,
[05:25] lo que va a hacer es recorrer todos los
recursos y cada recurso le le obtiene el
[05:30] título y se compara con el título pasado
por parámetro. En caso de que
[05:35] correspondan, se va a agregar a esa
lista y al final del ciclo lo que va a
[05:40] hacer es imprimir la lista de recursos
encontrados.
[05:47] Y pues pasaríamos lo que es al main. La
clase main, ¿qué es lo que va a hacer?
[05:52] Primero va a crear la biblioteca,
segundo va a crear los libros, luego las
[05:58] revistas y esas libros y revistas como
son recursos,
[06:04] eh se agregan a la biblioteca que se
puede ver por medio de este método, que
[06:07] es biblioteca pun agregar recursos y se
agrega ahí los lo que son los libros y
[06:11] las revistas.
Después vamos a hacer el préstamo de los
[06:14] recursos 1, 2 y 5. Bueno, con su ID 1, 2
y 5. Ahora vamos a buscar por título.
[06:21] Entonces, eh va a guardar la lista de
recursos
[06:26] y después lo que va a hacer es
imprimirse,
[06:30] ya que el método lo que hace es devolver
una lista de recursos. Se tiene que
[06:32] imprimir por medio de un
system.outo.printline.
[06:36] Y por último, la idea es ver el estado
actual de los recursos. Siguiendo la
[06:41] lógica, pues vamos a tener lo siguiente,
los tres libros, las dos revistas en la
[06:47] biblioteca, pero como se prestaron el el
recurso con ID1, ID2 e ID5, entonces el
[06:55] libro Quijote de la Mancha, el libro 100
años de soledad y la revista Nature
[06:58] Communications va a tener el valor
disponible en false. Entonces, si
[07:03] ejecutamos el
aplicativo,
[07:09] entonces vamos a tener lo siguiente.
Primero,
[07:13] que ya están los dispositivos creados.
Segundo, se prestó el recurso con ID1.
[07:19] En este caso se prestó lo mismo con el
ID2 y lo mismo con el ID5. Ahora vamos a
[07:24] buscar los recursos con título 1984. En
este caso se encontraron dos. el libro
[07:29] que es ID3,
que es este, el título se llama 1984, la
[07:35] revista también 1984
y el el estado actual de los recursos.
[07:41] Anteriormente había comunicado de que se
prestaron los recursos 1, 2 y 5.
[07:45] Entonces, si miramos el libro con ID1,
vemos que el disponible está un false.
[07:50] Lo mismo con el libro de con el ID2 y lo
mismo con el recurso con ID5. Y eso
[07:56] sería
el qué el ejercicio. Ahora vamos a ver
[08:01] el diagrama de clases. Como había
mencionado anteriormente, recursos es la
[08:05] clase
que es la clase sú en la cual hereda el
[08:12] libro y revista.
Eh, se se había mencionado anteriormente
[08:16] también qué tipo revista es un enum, o
sea, que tipo revista era, qué tipo,
[08:22] perdón, era de de tipo revista y tipo
revista era un enum. En este caso, pues
[08:27] al crear una revista solo permite crear
de estos cinco tipos.
[08:31] Además de eso, se puede dar se puede ver
que biblioteca contiene recursos.
[08:37] Entonces por eso está por medio de este
cuadrado, por medio de este rombo
[08:43] e vacío
y biblioteca. Al usar la interfaz se
[08:49] puede ver el la flecha puenteada con el
triángulo blanco. Entonces, ¿esto qué
[08:55] significa? Que biblioteca usa esos
métodos. M.

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
