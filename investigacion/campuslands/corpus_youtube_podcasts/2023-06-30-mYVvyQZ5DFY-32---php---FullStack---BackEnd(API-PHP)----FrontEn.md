---
fecha: "2023-06-30"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "mYVvyQZ5DFY"
canal: "Campuslands Bucaramanga"
duracion: "1:58:32"
vistas: 406
url: "https://www.youtube.com/watch?v=mYVvyQZ5DFY"
---

# 32 - php - FullStack - BackEnd(API-PHP) -  FrontEnd (JS) - Alquilartemis - By Camper Maicol Estrada

- **Canal:** Campuslands Bucaramanga
- **Fecha de subida:** 2023-06-30
- **Duración:** 1:58:32
- **Vistas:** 406
- **URL:** https://www.youtube.com/watch?v=mYVvyQZ5DFY

## Descripción del Video
```text

```

## Transcripción de Audio / Subtítulos

[00:00] listo Muy buenos días a todos
listo Hoy vamos a empezar con una
[00:06] pequeña prueba para consumir apis la
base de datos que vamos a usar es la
[00:11] base de datos que el profesor les la
última base de datos que el profesor le
[00:14] mandó entonces vamos a crear una nueva
vamos a crear una base de datos entonces
[00:20] venimos acá base de datos
le voy a poner Esto
[00:25] [Música]
[00:30] sí vamos a crear otra para esta clase
[00:37] dos yo voy a poner dos porque hay como
10
[00:41] Comenten así aquí le pongo lo de que
para lo de mayúscula creo que era utc
[00:53] listo creo que era este y le doy crear
perdón
[00:58] y ya está por acá Aquí está entonces le
doy aquí en importar Y ustedes
[01:05] seleccionan el último archivo que el
profesor les mando para para hacer esa
[01:10] base de datos
en mi caso yo la tengo por acá guardada
[01:14] en el en el Sam
[01:20] en la carpeta que de las plantillas que
yo le mandé que se llama clase 2
[01:41] listo ahí está
[01:47] es como quieran ponerle la cosa es que
la que sepan Cómo se llama para ahorita
[01:51] referenciarla
entonces Open folder
[01:57] tendría Abrir mi documento que tengo en
el local Host
[02:07] en este caso se llama clase dos Así es
que le puse listo aquí está la plantilla
[02:13] Este es el el
donde están las páginas Y en este caso
[02:20] vamos a
creo vamos a abrirlo primero y ya ya
[02:27] admiroquesa ya les digo qué vamos a
hacer entonces aquí el local
[02:32] local
[02:36] se llama
[02:39] clase
[02:42] entonces aquí le dan al fan y listo aquí
lo manda la página de factura Entonces
[02:47] en este caso para hacer un CURP rápido y
para que aprendan como a consumir eso
[02:53] Entonces vamos a hacer unos sencillito
este es más complicado si tenemos tiempo
[02:57] lo intentamos hacer pero vamos a hacer
uno más fácil que es aquí en clientes
[03:05] entonces La idea es consumir aquí en la
base de datos aquí la una de las tablas
[03:12] que se cargaron que se llaman
constructoras que en este caso me
[03:16] vendrían a ser quienes nuestros clientes
Entonces La idea es cargar todos esos
[03:21] datos aquí poder Añadir nuevos clientes
poder borrarlos Y si alcanzamos a poder
[03:27] actualizarlas listo Entonces
vamos a ir aquí a nuestro archivo y aquí
[03:34] en el H en el en el html clientes y esta
es la que nosotros vamos a modificar
[03:40] listo entonces aquí está la nuestra
tablita entonces para poder hacer la
[03:47] conexión con la base de datos nosotros
necesitamos tres archivos claves que es
[03:51] el conector el controlador y
el y el modelo donde van a correr las
[03:58] funciones entonces aquí donde dice Back
Ahí vamos a crear esos tres archivos
[04:02] listo entonces aquí creamos un nuevo
archivo Le vamos a dar el primero que va
[04:07] a ser conectar
[04:10] que va a ser php
listo vamos a crear de una vez el otro
[04:18] con conectar punto
allá me quedó el primero
[04:25] el otro se va a llamar
con control
[04:32] punto php
y el otro más
[04:42] y el otro se va a llamar model
[04:52] listo entonces aquí tengo mis tres
carpetas estas tres carpeticas son las
[04:57] que me van a conectar con la base de
datos Y es la que me va a crear la Api
[05:01] la cual yo la que es la que yo voy a
consumir con javascript listo Entonces
[05:06] vamos a empezar con la de conectar
Entonces ya sabemos como un archivo es
[05:11] un archivo php Entonces vamos a abrir
nuestra
[05:15] nuestro nuestro nuestra etiqueta de php
sino que se me partieron allá se me
[05:21] perdieron las cestas aquí php de acá lo
cerramos
[05:28] Sí una pregunta listo entonces
para conectar para empezar a conectarla
[05:37] Entonces nosotros vamos a creer que una
clase Entonces le damos aquí una clase y
[05:43] le vamos a poner conectar Recuerden que
con mayúscula para las clases conectar
[05:49] entonces conectar abrimos nuestras
llaves y ahí es donde nosotros vamos a
[05:55] crear esto nuestra función de de la del
pedido y de la base de datos Entonces
[06:01] vamos a darle un
protect
[06:09] y le vamos a decir que va a hacer con la
variable deben
[06:16] debe punto y coma que siempre se me
olvida
[06:20] y listo en protect vamos a hacer otra
con protect
[06:27] que es una función
una función y hasta le vamos a llamar
[06:32] conexión conexión
[06:36] conexión que es una función abrimos
nuestras llaves y listo en esta conexión
[06:41] vamos a crear un tricast
esa que va a ser nuestra promesa
[06:46] entonces aquí en el code es donde vamos
a poner el
[06:51] el código Entonces vamos a abrir vamos a
crear una una nueva variable llamada
[06:57] conectar
[07:00] eso ya lo sabe Pero vamos a hacerlo
conectar va a ser igual A quién a
[07:06] tis
[07:09] a disque Y le vamos a pasar al parámetro
de cuál era este
[07:17] el dv va a ser igual A quién a un
pdo listo vamos a hacer un pedo sencillo
[07:25] que es
abrimos las llaves de
[07:29] las comillas le decimos que es igual
Perdón en minúscula
[07:38] le damos dos puntos le decimos que el
local
[07:42] y le vamos a pasar el que es que en
nuestro caso es localhost local
[07:58] Sí es que este pedo se pasa es de muchas
formas en este caso vamos a hacer unos
[08:04] súper sencillo
[08:06] para conectarlo listo entonces ponemos
igual dos puntos local localhost
[08:14] lo cajón dos puntos y aquí le vamos a
pasar el debe
[08:18] el base de datos el nombre o sea el
nombre de la base de datos señor
[08:26] en dónde
[08:30] señor
[08:41] Sí hay punto y coma Sí claro
Ah no aquí en dos puntos local igual al
[08:49] localhost punto y coma
y le paso y le va a pasar ahora que el
[08:54] nombre de nuestra base de datos entonces
este debe name va a ser igual a quién Ah
[08:59] pues al nombre de la base de datos que
en este caso nosotros vamos a usar en
[09:02] este caso la base de datos que le
pusimos
[09:05] [Música]
a alquilar temis Entonces yo vengo acá
[09:10] con base de datos aquí están todas y
esta es la que yo Acabo de crear
[09:14] entonces esa es la que yo le puse
quería ponerle con mayúscula presencia
[09:19] Entonces es ahí aquí es donde Nosotros
le vamos a pasar el nombre la base de
[09:25] datos que vamos a usar
Entonces después de eso le damos
[09:30] cerramos ahí las comidas Entonces le
damos coma y qué sigue ponerle esto a
[09:36] nuestro
a nuestro usuario que en su caso es
[09:41] Campos en mi caso que estoy en Windows
es Root entonces coma abro
[09:47] comillas le doy digo que Ruth
[09:51] Y le doy coma y que sigue la contraseña
que en mi caso no tengo Entonces yo la
[09:57] dejo así listo entonces esperaré
Este es el de conectar Ese es el pedido
[10:04] con el que vamos a conectar a la base de
datos listo
[10:07] Entonces ya después de eso Simplemente
como es una función Entonces le damos a
[10:13] quien nos retorne recto
nos returne a quién Pues a este
[10:20] a esta variable listo conectar y
cerramos con punto y coma creo que aquí
[10:25] también va punto y coma que siempre se
me olvida
[10:28] punto y coma en el hasta allá en el cas
ya saben aquí le damos una variable
[10:34] llamada e y aquí le decimos que es
section
[10:45] y aquí le pasamos un retum
[10:54] y donde retornamos esta variable
[11:00] que va a ser
[11:10] así
[11:13] en Windows esto no suele afectar mucho
pero en Linux un montón
[11:24] listo entonces aquí completamos el
parámetro
[11:28] y le mandamos un get mensaje
[11:35] y listo Le cerramos la función
y punto
[11:41] y listo
[11:47] y Para nuestras para nuestros nombres
que tengan
[11:52] ño tilde Entonces vamos a ponerle la
función de texto que nos valía todas
[11:57] esas cosas entonces
señor
[12:08] bueno Igualmente bueno en cuenta no
importa el linus no sé el Lino sí me ha
[12:14] dado problema
[12:19] al final
[12:22] listo listo vamos a crearla nuestra
variable pública
[12:32] que vaya igual al set
es señal
[12:44] una función Pública para la validación
de las señas y de las tildes a esa
[12:51] función a veces no sé por qué
listo abrimos nuestras llaves entonces
[12:55] aquí retornamos
[12:58] retornamos a nuestro
[13:02] Dish que va a ser le asignamos a la debe
y a este le asignamos
[13:13] al cuello
[13:18] y le mandamos el mensaje
que
[13:24] set Names
abrimos nuestras comillas simples dos
[13:30] veces y Aquí vamos a poner esa extensión
que nos valida
[13:34] las las tildes usted utf8
[13:40] y listo cerramos aquí listo creo que ya
verifico que todos tengan estas que
[13:46] siempre se me voy a ponerle y listo esta
sería entonces nuestro pedido la función
[13:51] de nuestro pedido listo
[13:58] continuamos entonces recordamos lo que
tenemos que hacer que es llenar estos
[14:04] datos Entonces en ese caso entonces en
nuestro modelo aquí es donde nosotros
[14:09] vamos a empezar a construir las
funciones que nos van a llamar que nos
[14:14] van a llamar esos datos listo entonces
aquí Entonces vamos a crear una clase
[14:19] pero esa clase
[14:22] Ah Sí perdón hay que abrir las etiquetas
de php
[14:27] aquí
[14:38] entonces aquí vamos a instanciar una de
las clases por qué Porque necesitamos a
[14:45] este conectar o sea a este conectar la
volvimos una función para poder usarlo
[14:49] muchas veces entonces necesitamos
esenciarla para poder usarla entonces
[14:55] aquí en nuestro en nuestro models es
donde lo vamos a hacer entonces le vamos
[15:00] a decir que en una clase y le vamos a
poner por ejemplo alquiler
[15:06] y aquí extendemos
[15:12] es con stents A quién a nuestra clase de
conectar entonces la venimos la copiamos
[15:19] acá
[15:21] extendemos y la pegamos acá entonces
aquí ya cogemos y la abrimos entonces
[15:28] aquí es donde vamos a crear las
funciones para llamar a esos datos listo
[15:32] Entonces como necesitamos el de cliente
Entonces vamos a crear una función
[15:35] Pública para llamar a estos datos
entonces public
[15:40] función
[15:43] llamada get porque es vida URL
clientes listo
[15:50] venga de clientes una función entonces
ponemos nuestras
[15:57] paréntesis y abrimos las llaves
[16:03] entonces
aquí vamos a crear nuestro caso
[16:09] que es la promesa entonces
[16:14] le vamos a decir una variable llamada
conectar
[16:22] que va a ser igual al pared
[16:27] con dos dos puntos seguidos los dos
puntos le vamos a decir conexión
[16:35] [Música]
[16:42] conexión y ahora volvemos a llamar a
parent
[16:46] con los dos puntos le vamos a dar set
[16:51] name que esta me está llamando a la
función de la que nos valían las las
[16:57] tildes Y eso está llamando a la función
de la conexión listo que eso está por
[17:02] acá
a esta función y esta función
[17:11] entonces aquí en models
entonces recuerde aquí me acabo de dar
[17:18] cuenta de algo que es que aquí está en
mayúscula Entonces allá como estamos
[17:21] Llamando a la misma función debe estar
aquí también en mayúscula
[17:24] entonces conexión aquí ya vamos a la
función conexión y a la función signate
[17:28] listo y la se la agregamos a la variable
conectar
[17:33] entonces con otra variable llamada
stm vamos a decirle que es igual
[17:41] a la variable conectar
y la asignamos
[17:51] prepare
[17:56] abrimos paréntesis y aquí es donde le
vamos a dar esto el código que se le
[18:01] suele dar en el my para llamar las
tablas entonces aquí se le llama Select
[18:11] y aquí le vamos a dar el nombre de la
tabla que vamos a llamar entonces vamos
[18:15] a la base de datos y dijimos que íbamos
a llamar entonces vamos aquí al tenis y
[18:21] dijimos que íbamos a cargar a quienes a
los a los clientes que en este caso
[18:24] serían las las constructoras entonces a
esta tablita era la que nosotros vamos a
[18:29] llamar para que nos muestre esos datos
entonces venimos acá y se le añadimos
[18:33] aquí entonces se le seleccione todos los
datos de la tabla constructora listo
[18:40] conectar listo creo que ahí está todo
bien
[18:47] punto y comas eso es un error grande
punto y coma punto y coma
[18:53] sí creo que ya todos
[18:57] y listo Entonces ya teniendo esto hay
que ejecutarla entonces aquí
[19:03] stm
[19:07] y le decimos que
que ejecute
[19:19] Aquí ya está
entonces aquí Esta es la función que nos
[19:24] va a llevar todos los datos de esa tabla
listo
[19:28] Entonces ya una vez ejecutada entonces
necesitamos que retornarle entonces la
[19:33] retornamos stm
[19:41] y le decimos que nos muestre A quién al
fecha
[19:53] fecha O sea que nos muestra a todos
switch alt y le pasamos a nuestro pedido
[20:00] pdo estos dos puntos seguidos a nuestra
fecha
[20:15] listo Ese es el código con el que
nosotros la función que nos va a mostrar
[20:19] a quienes a los datos de la constructora
que estamos conectando con el pedido y
[20:23] el pdo se está conectando a la base de
datos que le pusimos que le pasamos aquí
[20:29] entonces este es el código
Mientras voy haciendo también el Cash
[20:34] que es lo mismo el anterior le llamamos
[20:39] una variable
[20:43] e le decimos que
[20:49] Perdón perdón
[20:58] y aquí volvemos retornamos
[21:05] a la variable
[21:10] y lo mismo legamos un
get mensaje
[21:17] cerramos y listo este sería el código o
la función que nos va a llamar
[21:22] a a esa tabla listo
[21:30] listo vamos a continuar y ahora sí vamos
a usar a nuestro controlador entonces
[21:35] abrimos nuestras
nuestras etiquetas de php
[21:41] que
HP
[21:50] y listo como bien sabemos esto
javascript y php no se entienden Pero
[21:55] hay un intermediario que se entiende
entre los dos que es esto el Jason
[21:59] Entonces vamos a crear ahí un header
[22:06] donde le vamos a decir que Su contenido
o content abrimos nuestras nuestras
[22:13] comillas simples y le vamos a decir
[22:19] content
está escrito igual a qué al tipo
[22:30] y le decimos de la aplicación
[22:38] que sea Jason
Listo ya estamos creando nuestro gel con
[22:44] un con un Jason
y ahora Necesitamos aquí Llamar tanto a
[22:50] esta función como Llamar a quien a
nuestro conector entonces aquí en
[22:55] controladores aquí es donde vamos a
llamar altos y es donde los vamos a
[22:59] fusionar para que él nos quede la URL
donde se va a generar la Api listo
[23:03] entonces ahí lo vamos a hacer con un
recuerdo
[23:09] y vamos a llamar
a nuestro
[23:15] conectar entonces aquí para asegurarnos
de que esté escrito tal cual y se lo
[23:22] pasamos aquí con comillas conectar
y lo mismo vamos a hacer con el
[23:27] siguiente
que es nuestro nuestros modelos entonces
[23:31] remake
control c aquí y se los damos acá
[23:38] listo ahí ya estamos ya estamos
llamándolo a los dos porque los vamos a
[23:42] necesitar
[23:45] y después de eso
vamos a instanciar vamos a crear una
[23:51] variable donde vamos a guardar a nuestra
función cita que creo que estaba aquí a
[23:57] este donde vamos a guardar a esta clase
listo entonces aquí vamos a crear una
[24:02] variable llamada Por ejemplo alquilar
alquilar
[24:08] va a ser igual aquí a una Estancia New
de quién de
[24:12] el término
de alquiler entonces venimos acá la
[24:17] copiamos y la pegamos acá
[24:22] callamos sus Ay perdón Ay hermoso y
abrimos
[24:29] y le abrimos los paréntesis punto y coma
que a mí ya se me olvidó ponerlos acá
[24:41] listo creo que no me olvido la otra
[24:45] listo entonces ahí ya tenemos a esa
clase
[24:50] Entonces vamos a crear la otra clase
otra variable llamada Body donde vamos a
[24:56] cargar los datos entonces Body es igual
a quien a Jason
[25:00] de code
[25:04] decimos que es
file con get
[25:11] y decimos
[25:15] contentos o sea el contenido
[25:19] y aquí abrimos paréntesis y abrimos
comillas y le decimos php
[25:27] dos puntos enlaces y le decimos que
input
[25:33] y le decimos que es un truco
[25:41] Sí gracias
[25:46] true php me cierro de una vez antes que
se me olvide Fire
[25:52] contains de Jason decode y listo
entonces aquí Entonces vamos a quedar
[25:58] nuestra serie de casos que nos van a
crear las urls listo Entonces vamos con
[26:02] un switch nos vamos a hacer entonces al
switch le vamos a decir como parámetro
[26:07] que sea get
que es la Perdón
[26:13] Aquí está Qué hacer con la URL Entonces
le vamos a decir con con nuestras llaves
[26:20] que va a ser la ope de opciones
y
[26:26] abrimos y aquí es donde vamos a empezar
a asignar los casos de esas urls
[26:31] entonces
para el caso 1 que es donde vamos a
[26:35] mostrar a mostrar necesitamos la URL que
nos muestre a los clientes de la empresa
[26:41] Entonces le vamos a decir ahí que sea
con un get
[26:47] un get en este caso que son todos
[26:53] al cuando tengan que manejar muchas de
estas urls es bueno especificar cada uno
[26:58] cada cada una está sobre las más
específicamente pero por este momento le
[27:02] vamos a dejar así listo entonces venimos
aquí creamos una llamada de datos
[27:09] que va a ser igual A quién a la variable
alquiler que es la que nos está
[27:15] estanciando al a la clase de alquiler
entonces aquí se la añadimos entonces
[27:21] dato va a ser aquí
se la pasamos le pasamos también la
[27:27] con flecha le hicimos que es
get clientes
[27:34] este get cliente es de dónde sale es de
la función que nosotros quedamos aquí
[27:39] entonces es esta la que nosotros estamos
llamando aquí en el controlador para que
[27:44] se nos ejecute aquí Entonces le damos
que es clientes que nos ejecute con la
[27:48] URL entonces get clientes Entonces como
es una función le abrimos los paréntesis
[27:53] punto y coma que no
punto y coma y después vamos a
[27:58] imprimirlo entonces con un hecho le
vamos a decir que es un Jason
[28:04] en code
Y de quién de datos que es el que está
[28:10] almacenando esa información entonces
aquí le estamos que es datos
[28:15] entonces aquí ya estamos creando esa URL
y nos falta que cerrarlo
[28:23] Break y pero lo acomodo Aquí bien
entonces listo esta sería prácticamente
[28:28] ya o sea por el momento ya deberían ya
debería estar creando una URL con es con
[28:35] la opción y con este método para que nos
muestre a quien a esos datos con Jason
[28:40] en este caso que es esto nuestra Api
Entonces vamos a probarla entonces
[28:46] venimos acá
abrimos nuestro local Host donde están
[28:52] guardando esos datos le damos que sea
la clase 2 que es como le puse a la
[28:59] carpeta y esta esta ese controlador está
en la carpeta llamada
[29:06] baking entonces aquí ponemos baki
[29:12] creo que sí lo tengo así pero me
verifico
[29:16] Back
[29:19] entonces en esta carpetita y Sí aquí
está entonces vamos a abrir el
[29:23] controller vemos que no nos dé un error
no hasta ahorita no da un error y ya
[29:28] aquí ya no está diciendo que falta la
opción y de ciertos parámetros Entonces
[29:31] eso es lo que le vamos a Añadir entonces
con signo de pregunta que es con lo que
[29:36] lo enlazamos Entonces le pasamos la
opción recordemos que fue el que le
[29:40] pusimos acá la opción y le vamos a pasar
a este método entonces
[29:44] opción que es igual a quién al get
Entonces le damos enter y listo
[29:55] [Aplausos]
[30:00] entonces aquí ya estamos creando la Api
que vamos a empezar a consumir con
[30:05] javascript listo entonces
listo
[30:11] Juan continuamos Entonces ya que tenemos
la Api Entonces vamos a empezar a
[30:16] consumirla de una vez entonces aquí en
páginas vamos a crear una carpeta
[30:21] donde vamos a decirle que clientes
y vamos a llevar este html vaya clientes
[30:30] y porque ahí donde vamos a crearlo los
javascript internamente en esta carpeta
[30:37] listo entonces en esa carpeta vamos a
crear
[30:45] un un javascript que es el que nos va a
consumir
[30:50] la Api le vamos a poner Api y le podemos
juntar js y el otro que es
[30:58] se me va a romper Entonces ya saben Api
mayúscula js
[31:05] punto js y listo y vamos a crear otro
archivo que es el que nos va a gestionar
[31:12] todas las funciones el que va ya es el
que va a consumirla la piel la que nos
[31:17] va a llamar nos va a hacer la conexión
con la Api y ya que con el otro la vamos
[31:21] a consumir Entonces le vamos a poner
clientes
[31:23] punto js listo Entonces ya tenemos los
archivos Entonces vamos a clientes y
[31:29] recordemos como estos dos se van a unir
Entonces vamos a venir aquí a de aquí ya
[31:35] lo tenía no lo borré entonces Script
clientes js
[31:41] pero igual vamos a comprobarlo aquí
control espacio es cliente js que es
[31:47] tipo módulo tipo de modulación porque él
va a llamar a otro javascript listo
[31:53] entonces
[31:56] para empezar vamos a crear la la
URL que nos va a cargar esos datos y lo
[32:03] vamos a guardar una variable Y esa
variable la que vamos a usar para perdón
[32:07] a crear una función que es la que vamos
a usar para para gestionar esos esa
[32:13] información listo entonces quedamos una
constante esto ya creamos una constante
[32:19] llamada URL en este caso le vamos a
poner clientes
[32:23] entonces clientes va a ser igual A quién
a la URL a la Perdón aquí a la hora l
[32:29] Entonces vamos
al aquí y vamos a copiar esta URL que es
[32:33] la que tiene la
la copiamos la venimos y la pegamos aquí
[32:37] Entonces esta constante clientes es la
que ahora tiene esa entonces venimos acá
[32:42] y vamos a crear una constante
[32:48] que va a ser una función entonces una
constante le vamos a llamar get que es
[32:52] por el método URL le vamos a poner
clientes qué clientes va a ser igual a
[32:59] una a una creo que es esta la Arrow
[33:05] entonces aquí abrimos Entonces
vamos a darle una constante
[33:14] una
constante llamada clientes sí que es
[33:20] donde vamos a tener los datos Entonces
esta constante Cliente va a tener el
[33:23] fecha y ese fecha es el que va a tener A
quién a esta URL entonces venimos acá
[33:29] URL y vamos a crear otra constante
otra constante y le vamos a poner datos
[33:38] datos clientes
[33:48] y este cliente es a quién va a ser igual
datos clientes pues va a ser igual a
[33:54] clientes pero ya en formato punto Jason
[34:07] aquí no necesario los punto y coma pero
por buena práctica y retornamos
[34:16] a quién Pues a tus clientes Ahora qué
sucede Ay perdón
[34:26] lo que pasa es que si este código llega
a fallar O sea si no llega a recibir
[34:31] ninguna señal hasta hice para el código
Entonces tenemos que decirle que
[34:36] decirle que sean que sea conforme a
nuestro tricash y también conforme a
[34:42] quién conforme la sinaway para que el
código se pueda ejecutar y no se atasque
[34:47] entonces este código lo ponemos aquí
dentro del Tri
[34:53] aquí y imprimimos aquí en el cast de una
vez el error en low Y imprimimos a quién
[35:00] a error Entonces
le decimos aquí que es así
[35:07] así y el away le decimos que es aquí
detrás del pecho entonces aquí
[35:17] ahí lo volvemos así no güey listo
Entonces esta función cita es la que nos
[35:23] va a retornar esos datos la que nos va a
retornar los datos del cliente listo ese
[35:27] array entonces vamos a venir aquí a
clientes Ah perdón a clientes js y aquí
[35:33] es donde vamos a hacer el llamado de
quién del clientes html o sea esta tabla
[35:40] esta tabla la que nosotros vamos a
llamar para insertarle esos datos
[35:44] entonces venimos aquí a clientes y
creamos nuestro
[35:54] un vamos a crear Unas benellisten que
nos Llame al dom para que cuando cargue
[36:00] el dom Entonces nos cargue la función
que va que va a llamar a esos datos
[36:03] listo Entonces le decimos al Don content
lower y vamos a decirle que sea un arroz
[36:10] funcho entonces decimos acá que se
ejecuta de una vez sin necesidad de
[36:14] nombrarla abrimos y listo entonces aquí
[36:21] es donde vamos a poner esos datos
entonces a esta función que nos va a
[36:26] cargar estos datos Vamos a ponerle
cargar cargar clientes
[36:31] Ah Sí perdón aquí faltó la comida
recargar clientes es una función con la
[36:37] que vamos a llamar a esos datos
obviamente todavía no está creada
[36:40] entonces la vamos a crear
entonces la vamos a crear acá
[36:45] una función que se va a llamar cargar
clientes abrimos y cerramos listo esa
[36:51] función que se va a cargar con el
logo entonces necesitamos aquí a los
[36:56] datos que nos está generando la Api O
sea a este dato cliente entonces
[37:00] necesitamos a esta función como está en
otro entonces simplemente que la
[37:04] importamos entonces aquí la importamos
importar A quién a get cliente se me
[37:11] olvidó como le puse
Así que clientes venimos acá importar
[37:16] que
clientes
[37:25] importar
[37:33] tan raro
[37:46] Ah perdón perdón es que cuando como es
no es por defaul toca darle así
[37:58] cierto no la estoy despertando
le damos aquí es
[38:05] ahora sí tenemos aquí ahora sí la
importamos Con qué clientes Ahora sí ya
[38:10] nos aparece ya saben aquí que no nos
pone la la extensión js
[38:16] Perdón
listo entonces aquí
[38:21] en cargar clientes
vamos a decirle a una constante
[38:29] que nos guarde esos datos le vamos a
poner clientes y va a ser igual A quién
[38:36] a este que es clientes que recordemos
que la función cita Entonces le damos
[38:40] acá entonces para comprobarlo vamos a
imprimir a esa a esa constante para
[38:45] mirar si los datos están guardando en
ella
[38:50] listo entonces venimos aquí ya acá vamos
a nuestro
[38:55] nuestra factura clientes
[38:59] Ah okay cambio como cambió la la página
[39:05] ahora está aquí en clientes cliente html
Ay no está conectando con el css
[39:11] Espéreme
el ccs está
[39:16] en la carpeta llamada css Entonces
espere vengo aquí aquí aquí clientes
[39:23] entonces aquí Busco el css
[39:27] fronte css index
cargamos
[40:17] tan raro
[40:21] esto Ahora sí Listo Ya apareció
listo Entonces vamos aquí en
[40:28] inspeccionar recordemos que en Java es
la consola la que nos muestra esos datos
[40:32] entonces damos aquí a control le damos a
recargar y no nos está mostrando nada
[40:37] entonces creo que también él es el
javascript está mal llamado venimos acá
[40:46] si se está ahí clientes
[40:51] pero vengo acá a la clientes aquí le doy
un Love con sol
[40:59] llamamos
[41:12] importando
[41:23] estamos usando la sinaway entonces toca
decirle aquí en el cliente
[41:31] aquí le decimos que es así
y aquí le decimos que es
[41:37] entonces venimos acá
[41:43] venimos acá y ya nos está imprimiendo
los
[41:54] se pausa pausa Bueno continuamos
entonces ya
[42:00] ya miramos que los datos estuvieran aquí
cargándose la raya y la promesa
[42:06] entonces lo que procedemos es a usar
ahora esos datos entonces lo que vamos a
[42:12] hacer es primero Llamar al lugar donde
vamos a insertar esos datos que está
[42:18] aquí en clientes que vendría a ser
nuestra tablita o sea sería esta
[42:22] Entonces vamos a llamarla con estos
datos con esta idea para ahí asignarle
[42:28] los datos entonces con una constante
[42:33] una constante
[42:37] que le vamos a poner esto tabla
tabla clientes
[42:44] por ejemplo el que quiere Entonces está
la 500 hicimos al documento
[42:52] selector y vamos a seleccionar A quién
al ID Perdón comillas simples y
[42:58] seleccionamos al ID que en este caso se
llama dato clientes Entonces control c
[43:03] venimos acá lo pegamos y ahí ya
estaríamos ubicando ese lugar entonces
[43:08] lo que procede es con un Forest recorrer
todos estos datos para inyectarse los a
[43:15] esta tabla Entonces vamos a a
nuestro foris
[43:20] y nos está pidiendo la raíz que ya
sabemos que es que clientes Entonces
[43:24] aquí
clientes en Force Eleven y listo
[43:29] Entonces vamos a decirle a tabla
clientes que es el lugar
[43:34] punto Inner html para inyectarle código
html entonces cogemos nuestros
[43:42] y ahí es donde vamos a escribir nuestro
código de la tabla listo Entonces ya
[43:48] sabemos
por tiempos que vamos a voy a ir a
[43:53] postra para traerme esa tablita
entonces
[44:03] tablet entonces necesito el tema
[44:09] entonces me vengo para aquí datos
clientes la pego acá Entonces qué datos
[44:14] necesito necesito Necesito el ID el
número entonces aquí va a ir el aire el
[44:20] ID Necesito la constructora
Necesito el número del nit de la
[44:27] constructora
Necesito el nombre del representante
[44:32] Y qué más necesito el el correo
electrónico entonces quedamos aquí dos
[44:37] más
[44:41] Entonces sí el teléfono
control c y ponemos aquí el teléfono
[44:46] entonces esta tablita la que vamos a
inyectar entonces control x vamos aquí a
[44:52] nuestro cliente y la ponemos acá
Entonces ahora Necesitamos cargar esos
[44:57] datos Entonces ya sabemos que entonces
clientes Entonces Element está
[45:03] recorriendo todos esos datos que tiene
clientes Entonces vamos aquí a abrirlo
[45:08] con nuestras llaves de
nuestro signo peso abrimos nuestras
[45:13] llaves y le damos Element
Element Y tenemos
[45:22] y tenemos que ir por el nombre Exacto
que tiene la tablet de todos estos
[45:27] elementos entonces aquí le damos a
estructura y Necesitamos este nombre y
[45:31] de constructora que le vamos a poner
aquí recordemos que si nosotros
[45:36] destructuramos a l m No necesitamos
escribirlo así Si quiere hagamos lo
[45:43] hagámoslo esta vez porque para que no se
nos olvide Entonces ya sabemos para
[45:49] estructurar creamos una constante y
donde nosotros le añadimos A quién a
[45:55] todos estos valores que es el que
Element está recorriendo entonces leemos
[45:58] y constructora
coma
[46:04] a quién más a nombre de la constructora
[46:12] el nit de la constructora
[46:17] al nombre del representante control C
control B
[46:24] al correo electrónico
coma control
[46:30] Y por último al teléfono de contacto y
lo pegamos aquí Entonces ya teniendolos
[46:37] aquí le vamos a decir que esto es igual
a quién
[46:42] a Element
entonces venimos acá y le decimos que
[46:48] eso es igual a L entonces ahí ya crea
todas como una que como una constante
[46:53] que ya podemos usar Entonces a ella no
es necesario decirle que esto sea
[46:57] Element punto ID constructora
Simplemente ya la llamamos porque ya es
[47:02] una constante y como verán ahí ya se se
alumbra como diciendo ya la estamos
[47:06] usando Entonces ahora sí así con todas
entonces cogemos Este ejemplo
[47:13] pongamos acá y aquí necesitamos a quién
Pues al nombre de la constructora
[47:17] entonces la ponemos aquí
[47:22] necesitamos
pero lo hago acá
[47:28] signo pesos abrimos cerramos
control c y todo también para acá yo
[47:36] también para acá y le termina esto para
acá
[47:39] entonces necesitamos el ni constructora
que lo vamos a poner acá necesitamos el
[47:44] nombre del representante que lo vamos a
poner acá
[47:47] necesitamos el correo electrónico que le
vamos a poner aquí y el teléfono
[47:54] entonces
en teoría en teoría ya debe estar
[47:58] funcionando Entonces vamos a verificar
nos vamos a nuestra página de facturas
[48:03] le damos recargar y
hay cargo un dato y eso es porque aquí
[48:09] en el antes de las es igual hay que
darle un más recargamos y Listo ya
[48:15] cargaron todos los datos
a la base
[48:22] listo Entonces ya terminamos el primer
crud que era Mostrar Ahora nos falta el
[48:27] siguiente que es insertar Entonces vamos
a crear un botón para insertar a nuevos
[48:33] clientes listo Entonces vamos a
venir aquí en nuestro clientes
[48:41] html y por aquí ya tengo por acá
aquí le vamos a decir a que sea un botón
[48:51] que sea
un un cliente
[48:58] nuevo
cliente nuevo entonces ya debe aparecer
[49:03] a cargar acá listo
está muy lejos
[49:08] [Música]
Pero podemos abajito
[49:14] Ahí está mejor Entonces le damos una
clase que ya tenemos aquí a gusto
[49:20] Entonces hicimos btn btn le vamos a
decir ah pero
[49:25] que se vea bonito
venimos aquí y venimos aquí a botones
[49:31] botones botones botones
[49:35] por aquí yo he visto una que me gusta
todo este esta clase btner
[49:43] entonces venimos acá
[49:47] y se lo damos
Entonces si venimos acá
[49:58] entonces démosle
démosle un margen creo que dos Sí está
[50:04] bien
[50:09] porque no se para
[50:15] estoy dando el que no es
acá
[50:22] une a tres
ya sí entonces aquí tenemos el botón
[50:27] tenemos la clase y un margen de tres
entonces La idea es que cuando le demos
[50:34] clic nos descargue el formulario para
ingresar un nuevo un nuevo cliente
[50:39] entonces significa que tenemos que ir
por un formulario por un modal entonces
[50:44] podemos dar que sea el formulario
Entonces vamos a mirar acá
[50:48] yo ya visto
[50:53] no
había uno que ya tenía
[50:57] [Música]
[51:07] es que había uno que ya tenía un
[51:15] venimos para acá y lo ponemos abajo el
todo No necesita estar ya que es un no
[51:21] necesita estar anclado porque es un
modal aquí clic derecho a formar
[51:24] documento
[51:31] Bueno entonces este es nuestro modal el
botón que necesitamos es el primero
[51:37] entonces este lo borramos
entonces necesitamos de esto Solo
[51:44] necesitamos estas dos cositas entonces
control x borramos lo demás
[51:51] y venimos al botón
el botón venimos al botón este y se las
[51:59] añadimos listo Entonces ese es el botón
que nos va a llamar al modo alto y
[52:03] venimos aquí a probarlo cargamos y no
nos funciona
[52:09] [Música]
sí nos faltó el link de vuestra de los
[52:16] Script femeninos acá
[52:20] copiamos el Script
[52:25] y venimos al otra vez a la página
recargamos y ahí está listo Entonces ese
[52:33] es el modal que nos va a registrar a los
nuevos clientes listo Entonces vamos a
[52:37] editarlo
[52:44] formulario Entonces como este vamos a
hacerlo de antes que se nos olviden como
[52:49] este formulario es el que vamos a llamar
entonces le vamos a dar un ID
[52:55] que puede ser registro le podemos poner
registro
[52:59] y le vamos a agregar de una vez el
método qué
[53:03] pues el que se nos olvide entonces listo
entonces miramos venimos a la base de
[53:09] datos para saber qué es lo que
necesitamos la base de datos que se me
[53:12] hizo esto necesitamos un ID necesitamos
entonces venimos acá
[53:19] esto es un mensaje esto no nos sirve
Entonces lo podemos borrar
[53:24] entonces necesitamos a este lo ubicamos
entonces necesitamos A quién a un ID
[53:30] aquí le vamos a dar el ID manualmente
pero se puede hacer automáticamente por
[53:36] cuestión de tiempo lo vamos a hacer así
manualmente ya después lo hacemos si nos
[53:40] queda tiempo lo hacemos automáticamente
que cuando que le hace ID Le vamos
[53:45] sumando uno y que simplemente lo imprima
en pantalla solo para visualizarlo
[53:48] entonces este ID le decimos que es tipo
number
[53:53] venimos aquí al modal
descargamos
[54:01] Ok necesitamos también venimos a la base
de datos que necesitamos el nombre la
[54:06] constructora entonces este Está bien
entonces aquí le ponemos
[54:11] una
constructora
[54:15] entonces Para aprovechar le ponemos aquí
[54:21] que sea ID
también se lo ponemos aquí en el Ford ID
[54:37] también se lo ponemos como ID
Este sí pongámoslo con minúscula
[54:48] también se lo ponemos en el Ford
[54:52] listo necesitamos también el nit de la
constructora Entonces qué significa eso
[54:57] que eso es otro number otro número
perdón sí otro número
[55:02] y necesitamos
nombre el representante Entonces es otro
[55:07] texto
también necesitamos el correo entonces
[55:14] venimos acá copiamos y pegamos y deber
de decirle decimos que es tipo de
[55:20] mai también necesitamos el teléfono
entonces copiamos y pegamos y le decimos
[55:25] que es tipo teléfono entonces entonces
aquí pedimos el celular
[55:32] celular
[55:35] creamos el ID con minúscula
[55:42] le ponemos la constructora la
constructora Este es el imán aquí lo
[55:47] pedimos en
[56:00] Este es el constructora
[56:06] email nombre el representante entonces
aquí es representante
[56:11] y
[Música]
[56:18] el nit de la constructora el número
[56:24] representante
[56:34] hacemos en minúscula porque más
recomendable
[56:38] Imagine representante el nit nit número
nit consultora ID creo que ya están
[56:45] todos los datos entonces venimos a
nuestra página recargamos y le damos
[56:53] aquí clientes y Listo Ya está nuestro
formulario de pronto vamos a arreglar un
[56:57] poquito porque eso está muy grande creo
que eso se arregla con columnas Entonces
[57:01] el ID
le vamos a decir que sea con una
[57:08] col de col de tres creo que era así
[57:15] si a ella se reduce pero no me aplica el
otro entonces
[57:21] constructora clase como es el nombre
entonces pongámosle un call de una
[57:27] columna de 6
al nit también pongámosle una columna de
[57:32] tres
al representante como es un nombre
[57:37] póngame una columna de 6
[57:41] alimail Pues
también la columna de 6
[57:47] al celular una columna de
[57:52] una columna de cuatro
y listo Tenemos aquí recargamos y le
[57:58] damos acá
igual nos quedan para abajo de abajo
[58:14] gracias
[58:19] creo que era creo que se le añades acá
Class le decimos que es un dislex
[58:29] El flex si creo que ya se corrige vamos
a ver
[58:33] Bueno creo que también tengo que decirle
que sarro si no me equivoco
[58:39] sea ya ahí se ve más ordenadito
celular
[58:45] 1 2 3 Listo ya se ve más ordenado listo
entonces lo que vamos a hacer es Llamar
[58:52] a todos estos datos para insertarlos
entonces como bien sabemos necesitamos
[58:58] esto la URL para insertar esos datos
entonces
[59:04] vamos a crearla Entonces nos vamos
primero a nuestras funciones
[59:11] Entonces vamos a usar la función de
insertar datos entonces declaramos
[59:18] una función pública función
[59:25] ya se le vamos a poner insertar insertar
en este caso estamos insertando a un
[59:32] cliente entonces
para insertar un nuevo cliente vamos a
[59:36] quedar las variables que nos van a
almacenar todos esos datos Entonces para
[59:40] no confundirnos vamos a llamar esas
variables tal cual como se llaman en la
[59:45] base de datos listo entonces venimos acá
y cogemos el ID constructora
[59:54] y le pasamos
y le decimos que la variable se va a
[60:00] llamar y de constructora entonces coma y
así con todos estos datos entonces
[60:05] nombre
[60:13] ahora cogemos el
[60:25] coma aquí nombre de representante
[60:40] el contacto
y el teléfono
[60:57] y algo raro que veo aquí
[61:07] sí
[61:27] listo Ahí está nuestra función cita con
los datos que le vamos a mandar los
[61:32] parámetros y ahora le vamos a decir
a nuestro conectar
[61:41] que va a ser igual a quien a parent
de quién de la conexión
[61:50] con el tiempo que no está que es la
función de que está en el otro lado
[61:56] entonces la conexión aquí cuenta y coma
que no ya punto y coma
[62:03] listo entonces conectar conexión le
pasamos ahora pasamos también la otra
[62:09] función
que es la del set name
[62:19] y también está en el otro lado y ahora
sí Aquí vamos a crear la variable
[62:27] stm que va a ser igual
a abrimos nuestras comillas aquí lo del
[62:36] Maíz igual Entonces le ponemos que
[62:41] quinto para insertar
[62:47] los datos en donde los vamos a insertar
Entonces vamos por el nombre de quién de
[62:53] la tabla a la que se los vamos a asignar
en este caso constructora entonces
[62:57] venimos acá se los inyectamos
le decimos la tabla que se lo va a
[63:03] inyectar y ahora sí le vamos a pasar los
nombres de de esas variables
[63:09] entonces que son los mismos de acá
entonces y de constructora
[63:18] coma nombre constructora
[63:25] coma nombre
[Música]
[63:32] coma nit constructora
[63:38] nombre el representante
[63:43] le pasamos también
el contacto Y por último
[63:51] le pasamos el teléfono
listo entonces después de eso le decimos
[63:58] que los evalúe con el valor entonces va
[64:05] con values y tenemos que pasarle los
[64:12] los datos que en este caso no los
tenemos entonces él se queda esperando
[64:17] se queda esperando los Entonces lo
mandamos con
[64:20] con el signo de pregunta en este caso
Son seis datos y venimos acá la base de
[64:24] datos nos dice que en estructura nos
dice que son seis entonces hay que
[64:30] ponerle aceite de esto entonces ahí va
uno dos tres cuatro cinco falta
[64:37] uno y lo separamos con comas
[64:45] y listo entonces aquí ya
cerramos y listo Entonces ahora le vamos
[64:52] a pasar esos parámetros a las variables
a las variables Entonces le decimos a la
[64:58] variable stm que fue como la nombramos
stm va a ser igual
[65:06] a la función de conectar
con conectar
[65:15] sigue una flecha
prepare
[65:21] a stm
listo así se inicia entonces
[65:28] y volvemos
stm va a ser igual a
[65:37] Bin vale
[65:40] abrimos paréntesis le damos uno y le
vamos a pasar
[65:45] al a la primera
a la primera variable que es esta
[65:54] y así con todas
[65:59] gracias
[66:03] listo entonces
pegamos Y empezamos a mandar a todas las
[66:09] variables
[66:12] esa sería quién la segunda
esta sería la tercera esta sería la
[66:18] cuarta esta sería la quinta
esta sería la sexta
[66:24] Entonces el nombre constructora después
sigue el nit de la constructora
[66:31] después sigue el nombre del
representante
[66:38] después sigue el correo electrónico
[66:44] Y por último sigue el teléfono
y
[66:58] después del teléfono Entonces le decimos
[67:03] a ese tema que se ejecute decimos acá
[67:15] y listo Entonces ahí retornamos los
datos
[67:21] con un retum
retornamos a esa variable stm
[67:28] y que nos muestre a todos Entonces le
damos aquí con el
[67:35] Mejor dicho es el mismo barrio
este mismo
[67:42] Igual vamos a escribir
[67:51] al el pdo
[67:57] que sea el
[68:10] y listo entonces ahí ya estamos creando
nuestra función cita creo que falta algo
[68:15] No creo que ya es todo
[68:21] No se les olvide no después de error
me faltan los punto y coma
[68:30] entonces en esta en esta función
Entonces ya estamos
[68:33] insertándole a la a la base de datos los
datos que le vamos a mandar entonces
[68:39] aquí creo que ya punto y coma punto y
coma listo esta esta función se llama
[68:44] inser cliente Entonces nos falta hacer
que el controlador o sea el caso
[68:49] entonces para
para ese caso Entonces le vamos a decir
[68:54] que sea
[68:59] un caso que sea con la
la insert te van a decir que es inser
[69:07] y le vamos a decir
[69:11] que el Data la
que la variable Data
[69:18] sea igual a quién
[69:21] a exactamente alquilar entonces podemos
la variable y se la pasamos a alquilar
[69:27] y
le mandamos
[69:33] A quién a la función que acabamos de
hacer cuál es esa función inser clientes
[69:39] Tenemos aquí a controladores
inser clientes y a ese inser clientes
[69:45] Entonces
le vamos a Añadir al Body que todo esos
[69:51] datos los datos de la de la de la de la
tabla entonces venimos aquí con nuestras
[69:59] llaves Entonces vamos a ir por quienes
por todos estos nombres de nuevo
[70:03] entonces aquí va
y de Entonces le damos
[70:09] una coma y volvemos a pasarle todo este
mismo parámetro entonces
[70:15] Pero ahora con el siguiente dato que
sería el nombre de la constructora
[70:24] señal
[70:28] hacia los ya los
Aquí estos datos van con comillas
[70:37] simple
[70:41] entonces venimos acá
[70:49] nombre de la constructora el nit de la
constructora
[71:00] representante entonces
[71:27] correo
[71:39] Y por último el teléfono
[71:48] y listo cerramos aquí y listo
simplemente le damos a un eco le decimos
[71:55] que es Jason raya pista en code
en code y le mandamos un anuncio que
[72:03] diga que los datos
[72:09] ingresaron correctamente
[72:14] y listo Entonces en ese caso sería ya
cerrar el caso que es con un break
[72:20] punto y coma y listo entonces aquí ya
creamos que la URL donde vamos que vamos
[72:27] a consumir para insertar los datos
Entonces vamos a probarla
[72:31] entonces venimos aquí a nuestro
[72:51] en dónde
[72:55] dice entonces aquí deber de decirle get
Ah le decimos que
[73:02] No
[73:05] creo que sí
[73:10] no le estoy pasando el parámetros pero
voy a estar preguntándolos
[73:16] modelos en la línea 39
[73:28] sí
[73:45] y listo entonces aquí me está pidiendo
que los datos Entonces ya podemos decir
[73:50] que está funcionando Entonces vamos a
ver si funciona realmente entonces para
[73:54] eso Entonces vamos a crear aquí en
clientes esto la el código para
[74:01] insertarla para insertar para insertar
esto estos datos Entonces vamos a la Api
[74:08] a construir primero Esa
esa función entonces en Api le vamos a
[74:15] decir
[74:18] que exportemos de una vez la la función
con una constante
[74:26] la constante pongámosle nuevo nuevo
cliente
[74:31] le decimos de una vez que es así
[74:35] y le vamos a pasar un parámetro
de donde vamos a cargar los datos le
[74:42] vamos a pasar un objeto Entonces ese
objeto le vamos a poner registrar
[74:47] registrar todavía no está creado pero lo
vamos a crear eventualmente entonces
[74:51] registrar
le vamos a decir que es una función
[74:56] abrimos
y listo entonces aquí le vamos a pasar
[75:02] con método
[75:07] vamos a poner de una vez que es away
y el agua que es un
[75:15] Fest de quién de la URL esta URL todavía
no la tenemos Entonces vamos a ponerla
[75:20] aquí una constante
y le vamos a poner
[75:25] URL esto nuevo nuevo cliente
[75:32] que va a ser igual a
a esta
[75:36] URL venimos acá la ponemos y está La
cogemos y la llamamos aquí en dentro del
[75:43] fecho
[75:46] entonces dentro del Fest con una gomita
dentro abrimos nuestras llaves
[75:53] y ahí le vamos a decir que el método que
es
[76:04] coma le vamos a pasar
al body
[76:10] que eso Jason punto
[76:16] y le pasamos al que va a cargar al que
tiene esos datos que en este caso
[76:22] registro que todavía no está creada pero
ya eventualmente la crearemos entonces
[76:26] registrar o pongámosle mejor registro
registro
[76:33] pero nos puedes confundirnos
porque este ya es el registro cargado
[76:38] entonces registro
[76:42] coma y le decimos
al que sea un headers
[76:49] dos puntos abrimos llaves y le decimos
que es esto con comillas simples el
[76:59] content
[77:03] content
[77:08] me salgo dos puntos vuelvo y abro y le
digo application
[77:20] y listo ahí ya debería estar cargándome
haciéndome el post para inyectar en la
[77:27] base de datos a esos a esos usuarios
nuevos Entonces ahora sí vamos a ir a
[77:33] clientes
[77:35] y vamos a agarrar a ese registro al
registro que hicimos ahorita en clientes
[77:45] a este registro que ya sabemos que le
pusimos una una idea que es registro
[77:49] entonces aquí pongámosle que sea
registrar para no confundirnos registrar
[77:54] Entonces vamos a venir aquí a clientes y
vamos a crear una función
[78:01] que va a ser nuevo
[Música]
[78:08] sí puede ser un nuevo cliente
nuevo cliente y le vamos a agregar una e
[78:15] ya una un evento entonces aquí
ya quedamos la función pero esta función
[78:23] necesitamos
que la tenga el formulario cuando él
[78:28] haga un submit entonces aquí es donde
vamos a llamar a quien a ese formulario
[78:31] entonces con una con le vamos a decir
que al formulario formulario
[78:36] sea igual a quién al documento
documento
[78:42] ya sabemos que podemos usar el
elector pero también podemos usar otro
[78:48] que se llama el get ID que simplemente
también nos llama al ID en este caso
[78:53] registrar Entonces no hay que decirle
que esa numeral porque él ya sabe que es
[78:58] un ID Entonces ya este formulario ya lo
ubicamos Entonces vamos a crearle que un
[79:04] evento Entonces al formulario
formulario punto advenelice
[79:12] listo
cuándo crea el evento cuando él haga un
[79:17] submit
[79:19] y va a cargar A quién a la función de
nuevo cliente entonces cogemos a Nuevo
[79:24] cliente si se lo pasamos para allá
entonces cuando él haga si nosotros
[79:29] vamos aquí a clientes este formulario no
tiene un submit tiene unos botones que
[79:34] es el de El de cerrar y tiene un botón
que
[79:39] creo que es este
Button de es este este botón lo vamos a
[79:46] lo vamos a poner aquí dentro del
formulario y le vamos a decir que sea
[79:53] entonces si venimos a la página y
recargamos
[79:59] y ahí está el botón de
un poquito aceite pero ya no hay por el
[80:03] momento
aquí le van a decirle enviar o cargar
[80:08] datos enviar Entonces ya tenemos al
formulario con una con un evento submit
[80:15] que se pueda realizar entonces venimos
acá
[80:19] a clientes Entonces ya tenemos a
nuestros
[80:22] Entonces esto Esto no nos sirve ahorita
porque la página es cortica pero cuando
[80:29] tengan una página muy larga
ese ese submi le va a generar problema
[80:34] Entonces La idea es quitarle con
con event quitarle ese evento que ya
[80:40] tiene por defecto que tiene por defecto
Entonces
[80:43] le decimos que ese evento sea por
default
[80:47] y
[80:52] si la página fuera más larga el área que
la página se volviera hasta arriba
[80:56] entonces necesitamos que haga eso igual
como nuestra página no es larga Entonces
[81:00] no no lo hace pero igual para que lo
sepa entonces Pero entonces en este caso
[81:06] lo que vamos a hacer es Llamar a todos
los valores de ese formulario entonces
[81:12] para eso vamos a darle una constante
[81:17] y vamos a llamar a quién a la idea de
ese formulario que va a ser igual a
[81:21] quién al documento
[81:28] cuál selector y vamos a seleccionar aquí
pues a la ID que le hayamos dado comilla
[81:36] simple a la ID que le damos nombrado en
formulario entonces hago algo acá pongo
[81:42] esto acá entonces necesitamos a quién
[81:48] al ID entonces aquí está nombrado a esta
ID la necesitaba entonces la ponemos
[81:53] aquí
entonces pero necesitamos el valor que
[81:57] la persona inscriba y Entonces le
ponemos punto
[82:01] valor
[82:05] Vale entonces con él así mismo con todos
entonces control C
[82:12] mejor dicho
[82:17] así con todos Entonces el otro dato que
necesitamos es quien el nombre el nombre
[82:23] de la empresa el cliente Pues el nombre
del cliente
[82:27] nombre cliente y le damos en este caso
sería la constructora Entonces le damos
[82:33] [Música]
a
[82:38] su constructora se dificulta un poco
[82:44] cliente
consultora el siguiente es el nit
[82:53] el siguiente es el representante
[83:00] el siguiente es al correo electrónico
[83:06] correo electrónico el siguiente es al
celular ya es el último entonces venimos
[83:12] acá y le ponemos al celular
y listo Entonces este ya sabemos que es
[83:19] el nit de la empresa
Este es el representante
[83:25] representante
[83:29] este va a ser el correo
y este va a ser quién el celular celular
[83:36] listo entonces para probar que que
estamos haciendo el llamado
[83:41] correcto le vamos a decir
[83:46] vamos a imprimir a uno de estos a uno de
estos datos a ver si no sale Entonces le
[83:51] decimos low con sol
y vamos a imprimir por ejemplo a celular
[83:56] listo entonces ahí celular venimos acá
cargamos sacamos a la consola
[84:04] y aquí cogemos a cliente y dijimos que
celular entonces aquí vamos a poner 3 15
[84:09] 53 frente 96 cuando ya le doy enviar y
listo ahí nos está imprimiendo
[84:15] correctamente a celular Entonces hasta
el momento todas estas variables tanque
[84:20] funcionando Entonces como dijimos vamos
a meterlo en un objeto para así mandarlo
[84:26] a la Api y que él no lo cargue en la
base de datos Entonces vamos a crear una
[84:30] constante Entonces esta constante que es
el objeto que como ya hemos dicho que la
[84:36] Api había recibido quien a registro
entonces aquí es donde la creamos
[84:40] Entonces esta constante que es registro
que es su que un objeto
[84:45] Entonces le vamos a decir que el ID
[84:51] que el ID va a ser dos puntos igual A
quién a este ID
[84:58] que el nombre cliente
[85:03] perdón
igual listo
[85:07] que el nombre Cliente
va a ser igual a quién Pues a nombre
[85:13] cliente
[85:16] así con
el
[85:22] coma
y así con el nit
[85:28] así con
el perdón aquí eran dos puntitos
[85:33] así con el nit así con el representante
y así con el correo
[85:41] y así con el celular
[85:46] Entonces como aquí javascript no se
entiende que este objeto está haciendo
[85:52] referencia a una variable Entonces
nosotros nos podemos ahorrar este
[85:57] nombramiento
señor
[86:08] ah no porque yo estoy llamando es a a
unas a unas variables Entonces yo a la
[86:13] variable no tengo que ponerle comillas
[86:22] no no no no iría así por ejemplo si yo
quisiera agregarle un dato directamente
[86:26] a la base de datos Pues yo lo haría con
comida
[86:34] a este
[86:38] [Música]
Ah sí creo que
[86:42] no porque es un objeto
[86:48] No creo que no
[87:05] Entonces no necesitamos ponerlos
[87:09] entonces esos datos son los que ese es
el registro y me acabo de acordar de
[87:14] algo
[87:17] que como este va a ser el objeto que
nosotros vamos a ingresar en nuestra en
[87:22] nuestra base de datos los nombres que
este registro debe tener es debe ser
[87:26] conforme a nuestra base de datos Qué
significa que este ID debe llamarse como
[87:31] ahí dijo constructora Entonces como
estamos usando este método de
[87:38] no nombrar las variables entonces
también hay que darle aquí arriba el
[87:42] mismo nombre para que lo entienda
entonces nombre constructora
[87:48] aquí nombre cliente que sería el nombre
constructora le damos aquí nombre
[87:52] constructora
nit Entonces el nit sería acá y también
[87:58] se lo damos acá
el nombre representante
[88:15] y nombre representante
[88:20] teléfono
[88:31] y listo entonces Para probarlo vamos a
entonces a mandar a la consola este
[88:37] objeto a ver si está funcionando si no
está agarrando los datos Porque ese es
[88:40] el que vamos a mandar Entonces vamos a
comprobarlo entonces cogemos y vamos a
[88:44] imprimir aquí a registro entonces
venimos aquí a la página
[88:50] recargamos
abrimos el moda entonces la ID en este
[88:55] caso sería 4
constructora pongámosle inventamos una
[89:01] pongámosle así póngale la hora que
quiera el nit puede ser cualquier número
[89:06] representante Pues digamos que soy yo
Michael David el correo
[89:12] Ah por acá hay un celular Acá hay uno y
vamos a enviar y listo aquí nos están
[89:20] cargando todos los datos de ese de ese
de ese de ese objeto listo Entonces ese
[89:26] objeto no está funcionando y es el que
vamos a mandar Entonces como es el que
[89:31] vamos a nosotros mandar vamos primero a
crear una validación para que todos los
[89:38] datos estén llenos entonces
[89:41] vamos a
con unis vamos a crear una validación
[89:47] una una función que es de validación de
la función todavía no está hecha ya la
[89:52] hacemos entonces
vale da tiempo pongámoslo así
[89:58] de quién de registro
[90:03] entonces esa calidad de registro abrimos
aquí comillas y le decimos con una
[90:11] alerta
[90:14] que
[90:17] todos los datos son
[90:22] obligatorios
[90:28] en caso de que no pues simplemente
retornamos
[90:35] retornamos aquí pues a registro
[90:40] pero este retum Entonces ya vamos a
mandarlo entonces directamente quién a
[90:45] la Api Y a quién debemos A quién debo a
quién debemos mandárselo Pues a Nuevo
[90:50] cliente que es el que está esperando a
ese objeto entonces nuevo cliente
[90:54] venimos aquí a clientes y en nuestro en
nuestro en nuestro Ay perdón aquí en
[91:02] nuestro import aquí lo vamos a agregar
para que nos llame esa función
[91:10] bueno igual se llama nuevo cliente
Entonces ese nuevo cliente que es la
[91:15] función entonces venimos acá y es la que
nosotros vamos a retornar entonces nuevo
[91:19] cliente y esto lo ponemos entre
paréntesis
[91:23] no al cliente me retorne esto pero este
esta validación todavía no está creada
[91:30] entonces la vamos a crear
[91:40] entonces la creamos con una función
le decimos válidation
[91:47] que me valide A quién a un objeto porque
eres un objeto Entonces es
[91:54] un objeto
entonces esa validación es así es el
[91:59] código fue el que nos pasó nuestro
profesor entonces simplemente nosotros
[92:02] retornamos
[92:06] retornamos aquí
[92:12] a la función Oye
[92:19] values
[92:24] a quien de objeto
[92:32] punto Every
creo que aquí son todos Ebrio creo que
[92:37] son todos
Element
[92:43] sea
[92:47] de elemento
[92:51] y esto lo haga y esto lo haga con una
comparación vacía
[93:01] listo creo que sí va el código entonces
lo que estamos validando aquí es que
[93:06] todos los datos se llenen Y si todos los
datos se llena Entonces ahí sí me va a
[93:10] retornar al nuevo cliente Entonces vamos
a probarlo esperemos que no error
[93:13] entonces aquí recargamos
[93:18] clientes 37
[93:33] señor
[93:39] no en este caso no porque estamos es
mandando datos no cargando datos
[93:46] Entonces en este caso dice
[93:55] Ah okay okay okay creo ya sé por qué la
función
[94:04] nuevo cliente se llama igual a la
función que tenemos allá entonces hay
[94:09] que cambiarle el nombre a esta función
entonces pongámosle simplemente una s
[94:13] clientes y aquí clientes Listo ya no se
llaman igual Entonces ya simplemente
[94:18] aquí recargamos y ya con sol Listo ya el
error se fue es que estábamos llamando
[94:22] la función que traíamos de la Api con
igual a la función que teníamos Entonces
[94:27] ya hay dará un error Entonces vamos a
probarla entonces clientes el ID ya
[94:32] sabemos que es el 4 aquí ponemos los
mismos datos números al azar Michael
[94:39] David correo pongamos esta celular este
y mandemos
[94:44] todos los datos son obligatorios de
estar dando un error
[94:53] submit
[95:10] dónde profe
[95:20] así
[95:32] 4 instructora
[95:38] Michael Estrada celular
[95:43] Listo Ya está mandando cerramos acá
actualizamos datos
[95:54] listo teníamos un tenemos un error sino
mandar los datos sino que yo aquí había
[96:01] escrito mal el código en esta parte le
había dicho que igual y es con flecha
[96:05] entonces arreglan eso y ya quedó
Entonces vamos a probarlo entonces aquí
[96:11] cerramos cargamos nuevamente la página
lo podemos cerrar aquí son las pruebas
[96:15] que hicimos entonces aquí no cliente le
decimos hay de 6
[96:20] constructora el nit el representante
pongamos a
[96:29] darle el correo el correo el celular
y enviamos y como no tenemos el código
[96:38] para recargar la pena todavía pero aquí
ya nos está cargando todos los datos
[96:56] Bueno
continuamos ahora vamos a hacer el el
[97:03] borrar cliente entonces para eso
obviamente necesitamos un botón Que
[97:07] obviamente nos falta Entonces eso vamos
Ese botón lo vamos a agregar en la
[97:12] tablita entonces aquí
[97:16] lo vamos a hacer aquí para rapidez
Entonces es un Bot es un voto
[97:23] Perdón esta mayúscula
[97:27] entonces un botón que sea eliminar
le vamos a dar una clase que sea btn
[97:36] btn btn igual btn btn
a Danger
[97:44] eliminar y este no lo vamos a arrastrar
[97:49] para dónde para
aquí en nuestro cliente en la parte de
[97:54] arriba Aquí vamos a crear un nuevo TD
y lo vamos a agregar acá
[98:07] venimos acá
[98:11] y lo ponemos acá Ese botón eliminar
venimos a la a la página y lo revisamos
[98:19] y listo aquí está el botón de eliminar
lo escribimos bien eliminar
[98:28] entonces para eliminar para hacer el
club de eliminar nosotros necesitamos
[98:33] decirle a nuestro código cuál debe
eliminar Entonces vamos a hacer el crud
[98:40] primero primeramente vamos a hacer quién
vamos a hacer a la función a la función
[98:46] de eliminar Entonces vamos a crear aquí
[98:51] dentro de nuestro objeto nuestro
[98:56] de nuestro de nuestra llavecitas
quedamos otra función pública entonces
[99:01] pública
y funcione
[99:07] le vamos a decir que sea un delete
delete cliente listo entonces aquí damos
[99:15] cerramos paréntesis abrimos llaves
Entonces le decimos que conectar
[99:23] es igual a quién al parent es el mismo
de antes simplemente para hacer la
[99:28] conexión entonces dice más conexión
[99:37] conexión
conexión
[99:44] cierro ahora parent ahora llamamos a la
a la función de de los caracteres
[99:55] abrimos y cerramos
y listo Entonces ahora sí vamos a
[100:00] decirle como el código de
sql Entonces sql le vamos a decir que
[100:07] sea igual a quién entonces aquí vamos a
decirle que delete del from de quién de
[100:16] la de la base de datos a la cual
nosotros a la cual nosotros deseamos
[100:21] eliminar en este caso es a la de
constructoras entonces constructoras
[100:27] se la ponemos acá Entonces vamos a
eliminar uno de los datos de la tabla
[100:33] constructora Entonces le vamos a decir
que eso lo haga cuando ella reciba que
[100:37] un ID Entonces le vamos a decir
QR
[100:41] huele y le tenemos que decir
[100:46] A quién cuando ella reciba a este
parámetro entonces venimos aquí al
[100:52] visual y le mandamos a ese parámetro
entonces aquí con ese parámetro le
[100:59] decimos que
sea igual a signo de pregunta
[101:07] ahí le están diciendo que espere el
valor de ID listo entonces Seguimos
[101:12] entonces abrimos pesos y le decimos sql
es igual a la variable conectar
[101:26] de con flechita le decimos prepare
[101:31] prepare
[101:34] a
esa variable llamada sql
[101:41] Esto entonces aquí cerramos Aquí también
Se nos olvidó cerrar
[101:46] con punto y coma listo sql después sigue
otra vez abrimos la
[101:53] sq sql le vamos a decir que
[102:03] un bit Bin
[102:06] Ahí es donde a la variable
a la variable ID le vamos a pasar esa
[102:11] función y aquí la variable todavía no se
la hemos dado Entonces se la vamos a
[102:15] crear acá ID esto esa variable ID es la
que va a contener esa ID entonces bien
[102:21] value bien vale Esteban mayúscula bien
Vale entonces aquí uno la única que hay
[102:31] la 1 y le da y le damos a esa variable
que es ID listo
[102:38] cerramos pasamos a la siguiente ya
simplemente le tenemos que decir que se
[102:43] ejecute entonces aquí es sql
le decimos que se ejecute
[102:59] que se ejecute y listo y retornamos
[103:04] a una variable llamada resultados
[103:09] que va a ser igual A quién a sql
[103:15] que me muestre
a todo el fech
[103:31] y ya nuestra conexión el pdo
[103:42] fecha
[103:53] lista entonces
[104:19] cuál
[104:22] esta no esta no
[104:27] Ah sí sí sí sí sí sí sí
[104:31] que es la variable que estoy llamando de
conexión listo
[104:36] [Música]
Ahora hay que después de haber quedado
[104:40] la función Entonces vamos a crear el
controlador Entonces vamos a crear el
[104:43] caso
entonces para ese para ese caso
[104:49] controlador Entonces vamos a crear
al caso delate desde aquí casi
[105:00] va a ser con el ID delete
le agregamos los dos puntos y a esta hay
[105:07] que pasarle la variable datos
[105:12] es igual
[105:16] a
alquilar
[105:20] y le pasamos la función y le pasamos la
función que es la del modes cual
[105:26] funciones
que para la escribimos bien de
[105:31] letra Esta función se la pasamos al
controlador
[105:36] abrimos paréntesis y le decimos que
cuando venga por el método get por el
[105:43] medio get
Y quién va a venir por el medio get el
[105:47] ID entonces venimos acá y le damos a ID
[105:57] Cuál cuál
[106:08] si tiene razón
[106:13] listo entonces aquí ya
con los corchetes y
[106:20] ahora con un hecho vamos a retornarlo en
que Jason
[106:27] en code
[106:31] y le decimos que
cliente eliminado
[106:38] y listo entonces para este caso entonces
necesitamos retornar retornar el ID
[106:45] entonces para retornarlo Entonces vamos
a ir a la Api señor
[106:57] vamos a ir a la Api y vamos a crear a
esa función que nos va que va a recibir
[107:04] la ID y que va y que lo va a borrar
entonces de una decimos que exporte la
[107:11] función a la función la creamos con una
constante
[107:16] le vamos a decir que delete delete
cliente
[107:22] de este cliente va a ser igual aquí a la
SIM
[107:30] así de quién del ID
[107:35] del ID y Esto va a ser un arroz
abrimos cerramos abrimos
[107:43] le damos el tricash
[107:48] aquí en el código le decimos que es a
wait le decimos al fecha
[107:54] y abrimos paréntesis aquí
necesitamos la URL que no se elimina
[107:59] entonces Vamos a sacarla que en este
caso es simplemente aquí deber de
[108:05] decirle insert vamos a decirle el caso
que tenemos
[108:09] al caso que es delete Entonces el
control c aquí le damos delete
[108:15] y listo nos dice que está esperando un
ID para ejecutarse
[108:21] entonces cogemos este código
[108:26] creamos aquí la url
en la Api
[108:33] con una constante
[108:38] y le vamos a decir que la URL del
cliente borrar
[108:47] esta Va a ser igual
[108:50] a esta url
que es la que nosotros vamos a pasar
[108:55] aquí y aquí sí hay que tener mucho
cuidado con el código siguiente porque
[108:59] toca poner tal cual es la url entonces
después de abrir los paréntesis vamos a
[109:04] abrir a nuestro
[109:08] Entonces le ponemos A quién a la
variable que contiene todo ese código
[109:16] y le vamos a decir
[109:22] la metemos primeramente en una
en nuestra en nuestra llavecitas
[109:31] y le vamos a poner una y
le vamos a decir que va a ser igual a la
[109:37] y
d y que la ID va a ser igual a la
[109:42] variable que estamos esperando que es va
a ser la ID
[109:48] y le vamos a dar después citó antes de
los paréntesis
[109:55] abrimos llaves separamos y ahí es donde
le vamos a poner el método que el método
[110:01] que tiene Entonces el método es dos
puntos delete
[110:09] y aquí simplemente imprimimos el error
[110:16] el error entonces aquí aquí está
esperando la ID para mandarlo Y borrarlo
[110:22] entonces lo que vamos a hacer es
mandarle la idea entonces aquí es donde
[110:25] vamos a ir a nuestro cliente y a este
botón es el que nosotros le vamos a
[110:31] asignar la ID de cada usuario para que
aquí en el cada cada cada botón tenga la
[110:39] idea que le corresponde según su usuario
Entonces le damos a decir aquí
[110:45] control c que su ID va a ser Ay perdón
su ID va a ser igual a quién al ID de
[110:54] cada de cada de cada cliente y le vamos
a agregar aquí una clase llamada
[111:00] delete que es la que vamos a usar para
ubicar a este botón entonces venimos acá
[111:06] abajo y vamos a hacer esa función vamos
a hacer esa función entonces la función
[111:12] de borrar
[111:18] de borrar
[111:21] entonces necesitamos que cuando se
oprima el botón de borrar ejecuta esta
[111:28] función Entonces vamos a llamar a Ese
botón ahora la cosa es que no podemos
[111:32] llamar al botón de cualquier manera como
Ese botón no existe en el html o sea
[111:38] existe aquí en el javascript pero en el
html significa que no lo va a llamar por
[111:43] qué Porque si nosotros le ponemos
[111:49] le ponemos por ejemplo Es que para no
hacer la larga mejor no se puede lo que
[111:54] vamos a hacer es Llamar a a alguien que
exista dentro de clientes que contenga
[112:00] Ese botón y como sabemos el que lo
contiene es este este esta tablita de
[112:05] datos clientes Entonces vamos a llamarla
a ella y que a través de ella nos ubique
[112:10] al botón entonces cogemos a esta ID nos
vamos a cliente le damos a una constante
[112:20] creamos una constante que llamemos que
la llamamos eliminar ella va a ser igual
[112:25] a quien al documento
[112:28] punto cuarzo lector abrimos le decimos
que sea el ID le envasamos el ID
[112:36] entonces a ella le vamos a crear a un
evento entonces eliminar punto
[112:43] advenicen y le pasamos el método de
Y que ejecute cuando se le dé clic la
[112:51] siguiente función la de quien la de
borrar
[112:55] y listo ahí ya se está ejecutando la
función de borrar y si yo le pongo e
[112:59] punto Target
[113:03] Perdón low con sol
[113:11] e punto Target
[113:18] entonces venimos aquí recargamos damos
clic derecho y le damos inspeccionar Y
[113:24] si yo le doy clic alguna de ellas
él empieza a que a ubicarme a todo a
[113:31] todos los datos que tiene en su interior
inclusive a quien al botón entonces
[113:36] necesitamos que
[113:41] reducir
este clic a que solo se active cuando
[113:45] del botón Y eso cómo lo hago con un If
Entonces le voy a decir que cuando If
[113:52] en su que en sue.tarjet
[113:57] contenga una clase Se acuerda la clase
que le creamos al botón aquí es donde le
[114:03] vamos a usar que cuando tenga una clase
aquí le ponemos
[114:09] que cuando tengo una una clase que
contenga
[114:17] a quién le decimos que si contiene a
dilete a delate Entonces
[114:24] si si ella tiene esto Entonces sí
ejecutes Entonces contáis sí para
[114:30] verifico que soy un escrito cuando
[114:34] listo Entonces le vamos a decir
aquí que lo console Para probarlo al e
[114:42] punto Target
Entonces
[114:46] esto ya no debe ejecutarse solos debe
ejecutarse Solo cuando yo le dé al botón
[114:50] entonces si yo le doy clic a todos ellos
ninguna de ellas ejecuta pero si le doy
[114:54] al botón ahí vemos Que qué que sí se
está ejecutando solo cuando le doy al
[115:00] botón y cuando le doy al botón usted ya
pueden ver que hay que en la ID Vale
[115:05] Según al que yo les a quien yo le doy
clic por ejemplo a este y su ID vale 6
[115:10] Entonces ese valor es el que necesitamos
capturar y mandar de nuevo entonces aquí
[115:16] vamos a crear aquí a una constante
[115:22] llamada
y de cliente
[115:28] que sea que igual a quién al e punto
Target
[115:33] que contenga un get
[115:39] atributo
[115:43] que contenga qué atributo a la ID
Entonces él va a valer esto Si al que yo
[115:51] le doy clic contiene una idea entonces
Para probarlo entonces démosle low con
[115:58] sol
y le damos a quién al ID cliente
[116:02] entonces
recargamos y le damos aquí a clic y como
[116:09] verán se está imprimiendo la ID del
botón entonces aquí la ID 2 Yo le doy
[116:14] aquí a la idea Se imprime que la y 16
Entonces ya estamos capturando el ID de
[116:20] cliente entonces este es el que nosotros
necesitamos mandar
[116:25] a quien a la Api para que cuando él
reciba ejecute la función de borrar en
[116:31] la base de datos
Entonces vamos a usar un confirmar eso
[116:38] es un eso es
[116:43] un eso es un método nativo Entonces
vamos a irle con confir va a ser igual
[116:51] al método con con
qué va a hacer Va a preguntarle desea
[117:01] eliminarlo
Entonces si él estos en caso es
[117:08] verdadero Entonces le decimos
a la variable confir
[117:15] que
ejecute
[117:22] ejecute a que ejecute la función de que
está aquí en la Api A quién a este
[117:28] Entonces vamos a cogerla vamos a
clientes vamos aquí y la vamos a
[117:34] importar
clientes y aquí es donde nosotros la
[117:39] vamos a usar Entonces si él da si él
dice que sí Entonces
[117:43] le mandamos a quién a la ID clientes
Entonces como esta ID clientes es la que
[117:50] está esperando quién la Api entonces
aquí le vamos a decir que es esta y esta
[117:57] y de cliente y ID clientes Entonces en
teoría ya ya deberíamos estar mandándole
[118:04] la idea del cliente Entonces vamos a
probarlo
[118:08] recargamos y vamos a eliminar el sexto
veamos que sí recargamos Y a ella la
[118:16] eliminó
[Aplausos]
[118:26] bueno
[118:29] Ay Buenos días

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
