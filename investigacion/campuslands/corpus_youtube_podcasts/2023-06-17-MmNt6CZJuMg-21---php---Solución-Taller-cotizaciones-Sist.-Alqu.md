---
fecha: "2023-06-17"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "MmNt6CZJuMg"
canal: "Campuslands Bucaramanga"
duracion: "33:12"
vistas: 339
url: "https://www.youtube.com/watch?v=MmNt6CZJuMg"
---

# 21 - php - Solución Taller-cotizaciones Sist. Alquilartemis - Using Composer - by Camper Cami Amaya

- **Canal:** Campuslands Bucaramanga
- **Fecha de subida:** 2023-06-17
- **Duración:** 33:12
- **Vistas:** 339
- **URL:** https://www.youtube.com/watch?v=MmNt6CZJuMg

## Descripción del Video
```text

```

## Transcripción de Audio / Subtítulos

[00:00] Hola buenos días a todos Mi nombre es
Camila Maya y el día de hoy Les voy a
[00:05] enseñar mi solución a la siguiente
actividad el reto era el siguiente la
[00:11] empresa de alquiler de material de
construcción alquilar tenis necesita
[00:14] construir un sistema sencillo de
cotizaciones desde cero
[00:18] este sistema era el alquiler de
productos de construcción para sus
[00:22] constructoras clientes teníamos el
requisito de que cada cotización era
[00:27] generado por un empleado que tenía un
usuario un password en el sistema y que
[00:30] la cotización debía tener dos partes un
encabezado con los datos de la
[00:34] constructora cliente a quien se alquila
y el empleado además de la fecha y demás
[00:40] detalles
generales y un detalle de cotización en
[00:44] la cual se deben registrar los productos
que se alquilan fecha hora y bueno más
[00:48] detalles para resolver este reto
Teníamos dos maneras de hacerlo una era
[00:56] usando un apicult en php y consumiendo
dicho servicio desde la Api otra forma
[01:02] de hacerlo era sin Api con un patrón mbc
enviando solicitudes desde el propio
[01:08] modelo hacia la base de datos yo decidí
resolver esta actividad de la segunda
[01:14] manera directamente
haciendo solicitudes desde el modelo Así
[01:19] que les voy a enseñar
digamos mi trabajo tenemos la entidad
[01:26] empleados clientes productos categorías
y cotizaciones y dentro de la base de
[01:31] datos alquilar tenis tenemos seis tablas
en este momento cinco entidades y seis
[01:37] tablas luego les hago como más en
profundidad de que va digamos las tablas
[01:44] más interesantes
ahora yendo al código tenemos una
[01:49] carpeta backend y una carpeta frankends
dentro de la carpeta backing tenemos un
[01:55] archivo de database sql donde tengo
anotado pues cada tabla y sus atributos
[02:02] sus columnas y pues qué valores son los
que se guardan dentro de esas columnas
[02:08] también dentro de la carpeta de backing
tengo una carpeta de configuración donde
[02:13] tengo la conexión a la base de datos
esto ya se había visto en clases pasadas
[02:19] este archivo se conecta a este otro de
dv.php donde tenemos estas variables
[02:25] estas variables simplemente son el tipo
de base de datos el nombre de la base de
[02:31] datos el usuario y la contraseña y
simplemente las inyectamos dentro de
[02:36] nuestra clase abstracta conectar la cual
pues nuestra conexión a la base de datos
[02:41] es este atributo debe conexión
utilizando vídeo
[02:46] esta línea ya sea explicado en clases
anteriores pero pues simplemente estamos
[02:50] diciéndole a cuál base de datos nos
vamos a conectar Y además que nos
[02:55] devuelva por defecto a raíz asociativos
ahora yendo más hacia la carpeta del
[03:02] frontend tenemos varios módulos que se
parecen bastante
[03:06] a módulos que hemos hecho en clases
anteriores entonces voy a tratar de
[03:11] profundizar A lo mejor en soluciones o
en detalles que todavía nos han
[03:17] explicado digamos hay módulos que son
bastante parecidos por ejemplo
[03:21] categorías clientes empleados y
productos voy a poner de ejemplo
[03:26] clientes tenemos nuestra vista clientes
que después nuestro documento html al
[03:33] cual le insertamos datos utilizando php
de manera ya renderizado se vería de la
[03:39] siguiente manera
con nuestro modal con nuestro formulario
[03:42] que pues envía los los datos a el
siguiente archivo agregar punto php
[03:48] mediante el método post tenemos nuestro
modelo cliente el cual tiene que empezar
[03:55] de sus atributos sus seres
[03:59] Y tenemos Asimismo tres archivos de
agregar borrar y editar eso ya lo hemos
[04:06] visto en clases anteriores Entonces no
voy a ahondar demasiado en esto lo que
[04:12] sí es nuevo que decidí añadirle es al
módulo de categorías y es lo siguiente y
[04:18] se los quiero mostrar que por ejemplo en
categorías
[04:21] que añadirle imágenes sin embargo
solamente había logrado hacerlo mediante
[04:26] una URL pero no es eso no es tampoco tan
intuitivo para la persona que lo va a
[04:33] usar sobre todo si es una persona que no
sabe Mucho de tecnología así que pues
[04:38] voy a hacer un ejemplo como para para
que ustedes puedan ver entonces por
[04:44] ejemplo acá no sé alguna descripción y
lo que hice fue que tú puedas
[04:50] seleccionar archivos directamente desde
tu explorador de archivos entonces tengo
[04:55] esta imagen ladrillos punto png la
guardo
[04:59] y se me va a guardar
mi nuevo mi nueva categoría incluyendo
[05:05] la imagen y esta imagen se va a guardar
automáticamente
[05:09] en esta carpeta de categoría imágenes
Entonces miren Aquí está ladrillos png
[05:17] que es la imagen que acabamos de
insertar en nuestra categoría ladrillos
[05:23] también podemos Pues editar
nuestra nuestro registro y no pasa nada
[05:31] podemos borrarlo también si queremos
tampoco pasa nada y Bueno les voy a
[05:37] mostrar Cómo fue que hice esto
[05:41] venimos aquí al código y en categorías
más nos vamos a nuestro a nuestra
[05:53] este
[05:58] [Música]
[06:03] listo ahora Estamos aquí en categorías
nos vamos a ir a nuestra vista
[06:09] categorías que es nuestro documento html
al cual insertamos datos con php en
[06:15] nuestro modal donde está el formulario
por el cual yo envío datos mediante post
[06:21] a el archivo de agregar punto php tengo
que añadirle el siguiente atributo que
[06:28] es end type multipart form deira esto lo
que hace es que el formulario pueda
[06:34] recibir archivos que son imágenes
entonces necesitamos Poner este atributo
[06:41] dentro del atributo del formulario
porque si no esto no va a funcionar Así
[06:46] mismo nuestro input es de tipo file para
que nos permita abrir el explorador de
[06:52] archivos y que la persona pueda subir su
imagen luego venimos aquí
[06:58] a agregar punto php y acá está lo
interesante tenemos Pues nosotros nos
[07:04] conectamos a nuestro modelo de
categorías creamos una nueva categoría
[07:09] cuando la persona presione el botón para
registrar una nueva categoría Le ponemos
[07:16] el nombre con el dato que se haya
llenado dentro del input y así mismo con
[07:20] la descripción pero
acá viene lo interesante quiero que vean
[07:25] Incluso si hacemos un by down de lo que
es
[07:30] la variable global files así como
compost pero files Esto es para poder
[07:37] visualizar o bueno para poder enviar
archivos Entonces esto es para que vean
[07:44] que recibo yo con esta variable global
Entonces si por ejemplo vengo acá a un
[07:50] nuevo registro no sé cualquier cualquier
cosa
[07:54] le doy guardar me va a aparecer una con
lo que he recibido recibo un array que
[08:01] tiene solamente un elemento llamado
imagen y ese elemento tiene a su vez una
[08:07] raíz con seis elementos uno con el
nombre de mi imagen que si recuerdan es
[08:14] ladrillos punto png y además otros otros
tipos de datos como el otros datos como
[08:20] por ejemplo el tipo que es una imagen
png y lo que nos interesa en este
[08:26] momento Es sobre todo el name y el tempo
porque el tmp es la ruta en la cual
[08:38] se guarda la imagen pero de manera
temporal es una ruta temporal donde se
[08:44] guarda la imagen pero si la persona
cierra el navegador Esa esa imagen se va
[08:48] no No se va no se guarda en ningún lado
Entonces se borra lo que nosotros
[08:52] tenemos que hacer es agarrar esta ruta
Temporal y pasar el archivo desde de
[08:58] esta ruta a la ruta que nosotros
queremos que a donde nosotros queremos
[09:02] guardar nuestras imágenes Entonces ya
que vimos pues lo que recibimos con esta
[09:10] variable files lo que se hace es pues
guardar primero lo que hice fue guardar
[09:17] primero en una variable de el basement
de la imagen el nombre el nombre de mi
[09:24] imagen que en este caso es ladrillos
punto png y además también guardé la URL
[09:30] temporal es con files entrando a imagen
y
[09:35] admp que es la ruta temporal la ruta a
la cual yo quiero subir mis imágenes es
[09:43] ctg de categórico images Slash el nombre
de mi imagen entonces le estoy diciendo
[09:51] mire en esta carpeta de acá que yo creé
usted me va a guardar esa
[09:57] de imagen va a pasármela está esta
función de move uploader file es la cual
[10:04] me ayuda a pasar la imagen desde la URL
temporal a la ruta a la cual yo quiero
[10:11] subir mi imagen Qué es esta de acá
entonces
[10:15] simplemente es una función propia de php
entonces hacemos uso de esa función le
[10:21] decimos páseme mi imagen desde esta URL
a esta carpeta y simplemente ponemos a
[10:28] nuestra instancia de categoría el set
img la ruta a subir la ruta que tiene
[10:35] que seguir para encontrar esa imagen le
damos insertada Entonces es algo nuevo
[10:42] que quería probar es la manera en la que
pues podemos guardar y Mostrar imágenes
[10:47] Por así decirlo guardar
de manera más intuitiva para el usuario
[10:53] entonces me pareció algo muy interesante
que que a lo mejor podría ser Útil para
[10:58] otras personas otra cosa que quiero
mostrarles es el módulo de cotizaciones
[11:07] nos estaban diciendo que cotizaciones
debía tener un empleado que es empleado
[11:12] Pues el empleado que Atendió la
cotización y la empresa a la cual le
[11:18] vamos a realizar la cotización además
como otros datos como la hora la fecha
[11:23] etcétera entonces
yo quise utilizar los acordeones de
[11:28] bootstrap y cada acordeón es una
cotización diferente por ejemplo le voy
[11:34] a dar clic Y este tiene el ID de la
cotización la empresa a la cual se le
[11:40] realiza esta cotización y el empleado
que estuvo atendiendo al cliente la
[11:45] fecha en la cual se realizó la hora y el
día del alquiler Así mismo como su
[11:51] ahorita también les quiero mostrar este
botoncito de generar PDF porque es algo
[11:57] que estuve probando y pues eso no es un
poco más
[12:02] no es algo que hayamos visto en clases
anteriores pero pues quiero repasarlo o
[12:09] echarle como Una miradita así para que
vean más o menos también lo que se puede
[12:15] hacer así mismo podemos
insertar lo que son productos dentro de
[12:21] nuestra cotización y ya les voy a
explicar Cómo podemos hacer esto
[12:24] nosotros insertamos los productos y nos
suma los precios para recibir un total
[12:30] Entonces eso es lo que hace esta página
cómo se cómo cómo cómo se pudo hacer eso
[12:36] pues acá lo normal un formulario
método post y simplemente pues acá
[12:44] añadimos los datos normales de una
cotización acá están los clientes acá
[12:50] empleados Esto es lo que ya hemos venido
viendo desde antes sin embargo quiero
[12:56] mostrarles esta tabla de productos por
cotizaciones es una tabla pivote es la
[13:02] tabla la cual me permite poder añadirle
productos a mi cotización Entonces yo
[13:09] genero una nueva cotización y mediante
mi tabla pivote de productos con
[13:14] cotizaciones lo que hago es asignarle
productos a una cotización en específico
[13:20] Entonces si podemos Si vemos aquí en php
My admin lo único que tengo es el id
[13:27] único el identificador único el ID del
producto y el ID del detalle simplemente
[13:34] entonces acá le estoy diciendo el
producto con el ID número uno
[13:39] añádamelo al detalle o bueno si al
detalle de cotización con el ID número 3
[13:45] entonces de esta manera podemos
normalizar
[13:50] una relación que es de muchos a muchos
para que pase de ser de uno a muchos así
[13:57] que pues viéndolo más en detalle a nivel
de código vamos a ver aquí en
[14:05] cotizaciones
tenemos lo mismo de siempre nuestro
[14:10] nuestra vista que eso ya hace ya pasa a
ser un poco más complejo pero bueno voy
[14:19] a tratar de explicarlo paso por paso
[14:23] Bueno aquí en cotizaciones tenemos
lo importante son estas instancias de
[14:30] aquí primero hacemos una instancia de mi
clase de cotización que es esta clase de
[14:37] acá que pues es un modelo normal con su
constructor sus atributos sin embargo lo
[14:45] que quiero que le pongamos atención Es
sobre todo a estos dos a estos dos
[14:50] métodos Pero más adelante vamos a ellos
Entonces tengo dos instancias bueno o
[14:57] dos dos variables claves que de una es
old cotizaciones que tiene la
[15:02] información de mis cotizaciones pero con
el método de obstain all con universale
[15:08] Qué es esta de aquí es pues Exactamente
lo mismo A lo que veníamos viendo
[15:14] solamente que con un Inner join y porque
un Inner join porque yo en mi tabla
[15:20] cotizaciones yo no tengo
realmente el nombre de la constructora a
[15:27] la cual le voy a vender los materiales
ni el nombre del empleado que atendió a
[15:31] la constructora yo lo que tengo es
lucidez Pero a mí no me sirven los
[15:35] ideales yo necesito Mostrar los nombres
correspondientes a esos ideas y por eso
[15:39] utilizo el Inner entonces a la que acá
lo que estoy diciendo es que me
[15:43] seleccione de la tabla cotizaciones el
ID de cotización de la tabla empleados
[15:48] el nombre del empleado en la tabla
constructoras el nombre de la
[15:52] constructora y así con varios datos
tengo varios datos ahí que me seleccione
[15:58] todos estos datos desde cotizaciones
también me haga un Inner join de
[16:05] empleados donde cotizaciones en la tabla
cotizaciones el ID del empleado sea al
[16:12] líder empleado que está dentro de la
tabla empleados
[16:15] suena un poco enredado pero no es tan
difícil simplemente estamos diciéndole
[16:20] que lo que haga es que me agarre la
tabla constructoras y donde esta tabla
[16:26] coincida en esta columna y esta otra
columna entonces que me junte esas dos
[16:34] tablas que me las combine De cierto modo
donde en mi tabla cotizaciones coincida
[16:40] el ID de la constructora con el ide de
la constructora en la tabla
[16:44] constructoras simplemente Espero que que
se entienda más o menos como como es la
[16:52] vuelta pues
no sí simplemente que coincidan y que
[16:57] ahí me una de esas dos tablas Por así
decirlo entonces ahí lo que hago es
[17:02] obtener todos los datos que yo necesito
de mi cotización y luego obtener
[17:07] productos
con este obtener productos Pues luego
[17:11] más adelante utilizaré este método que
ya más adelante lo voy a explicar porque
[17:15] es un poco más complejo Bueno lo que me
interesa en este momento es este fritch
[17:23] con este todo este fritch Por qué Porque
este fritch es mi acordeón cada digamos
[17:31] estoy pidiéndole que me recorra todas
mis cotizaciones y que por cada
[17:38] cotización me genere un nuevo acordeón
Sí
[17:42] para así decirlo de manera fácil
entonces
[17:46] primero le estoy pidiendo que me cree
pues mi vida acordeón y estoy insertando
[17:52] la fecha la hora el día bueno lo que ya
hemos visto con mis etiquetas de php
[17:59] insertando los datos de la base de datos
normal eso hasta ahora pues no no es
[18:05] nada nuevo
más adelante vemos esto por ahora
[18:09] ignórelo luego más adelante pues lo
explicaré que es para crear PDF a partir
[18:14] de la cotización pero no vamos a
adelantarnos ahí todavía bueno esta
[18:18] instancia que yo había declarado en la
parte superior del documento de obtener
[18:22] productos le voy a Añadir Bueno más bien
le voy a aceptar el ID del ID de la
[18:29] cotización
que se está creando en este Bridge Por
[18:33] así decirlo le voy a poner ese ID para
mediante esta instancia Llamar a mí a mi
[18:41] método productos para qué Para obtener
los productos que corresponden la
[18:47] cotización que yo estoy imprimiendo en
mi documento sí Entonces ahora sí vamos
[18:52] a revisar que tiene nuestra función de
optim productos es lo mismo de siempre
[18:58] solamente que
utilizamos
[19:02] alias pero no es nada complicado es Cómo
hacer un Select dentro de un Select
[19:10] le estamos pidiendo vamos a leer Primero
este este paréntesis No necesitamos que
[19:15] pidiendo que me seleccione de mi tabla
pivote productos por cotizaciones el
[19:21] líder del producto y el ide del detalle
Además del nombre del producto y el
[19:26] precio que me lo seleccione y me haga un
Inner joint para poder traerme el nombre
[19:31] del producto donde donde coincida con el
ID del producto no es más
[19:36] además
deslizamos diciendo tráigame todos esos
[19:41] Pero qué pasa no me sirve únicamente eso
Porque entonces me va a traer la tabla
[19:48] de productos por cotizaciones completa
con con todos los registros de todas las
[19:53] cotizaciones a mí me interesa solamente
traerme los productos que están añadidos
[19:59] a mi cotización
específica Entonces digamos le estoy
[20:07] diciendo tráigame toda esta tabla y
póngale el alias resultado toda esta
[20:12] tabla póngale por ahora nombre de
resultado ahora seleccione de resultado
[20:18] donde el ide de detalle sea igual al
parámetro que yo le voy a mandar que va
[20:25] a ser este ID es un poco confuso Espero
que se haya entendido más o menos
[20:32] Pero simplemente es hacer un seleccionar
varias columnas hacer un innerjol y de
[20:40] ese resultado de ese Inner join digamos
hacer un filtrado para solamente obtener
[20:45] los productos de la cotización que yo
quiero obtener Espero que se haya
[20:52] entendido entonces pues gracias a este
método yo qué hago es obtener todos los
[21:00] productos de una sola cotización que es
la cotización que estoy imprimiendo acá
[21:03] Entonces esto simplemente es el cuerpo
del acordeón y si tengo un forich dentro
[21:09] de un forich
tal vez es un poco confuso pero pues un
[21:14] foriche es para crear el acordeón y el
otro forich es para crear nuestra tabla
[21:19] productos entonces simplemente
recorremos el array que nos devuelve mi
[21:25] método para que por cada producto me
genere una fila de la tabla Entonces
[21:31] digamos genera una variable que se llama
suma Total que es igual a cero y por
[21:37] cada producto yo le voy sumando a esa
suma total el precio del producto esto
[21:43] para qué Para poder
imprimir el total el precio total de
[21:47] todos mis productos que vienen en la
cotización entonces pues simplemente
[21:53] imprimo el ID del producto el nombre del
producto y el precio por día de mi
[22:00] producto entonces simplemente también
imprimo en mi total y la suma Total que
[22:07] es la suma de todos los precios de mis
productos eso es como lo más interesante
[22:13] digamos de la cotización Espero no haya
sido muy enredado yo creo que tal vez lo
[22:18] más enredado fue esta parte Pero bueno
espero que se haya se haya entendido Y
[22:25] sí pues me parece que se ve bastante
chévere otra cosa que quería Mostrar es
[22:31] lo estuve experimentando un poco con
composer composer es un gestionador de
[22:39] paquetes algo así como npm para
javascript así lo es composer para php
[22:45] entonces encontré un paquete en composer
llamado mpdf y gracias a esta a esta
[22:52] librería se pueden generar
pdfes entonces yo dije estaría súper
[22:58] genial poder generar un PDF a raíz de
una cotización Así que si yo le doy clic
[23:05] en generar PDF me genera Efectivamente
mi cotización esto es una plantilla que
[23:11] yo hice pero le estoy insertando tanto
el nombre del empleado como el ide de la
[23:16] cotización como el nombre de la
constructora cliente como el nit de la
[23:21] constructora cliente y como de los
productos así que voy a tratar de
[23:26] explicar Pues de una manera sencilla
pero a la vez que se entienda Cómo fue
[23:32] este proceso
listo ahora para poder continuar con la
[23:38] parte de composer Y mpf
estos son los archivos que
[23:45] digamos son necesarios para poder
generar estos pdfs primero que nada
[23:51] debemos tener instalado con Bowser en mi
caso pues
[23:57] ahí pueden ver que yo tengo la versión
2.5 y pues debemos correr el siguiente
[24:03] Comando Bueno de hecho podemos buscarlo
aquí mismo en
[24:09] en la web Ah bueno php unit es otro otra
librería pero por ejemplo en esta página
[24:15] de packagist podemos Buscar muchos
paquetes que están incluidos en composer
[24:21] entonces si yo busco mpf me sale
la librería que yo utilicé para generar
[24:29] mis pdfs lo que tenemos que correr en la
línea de comandos es pues este Comando
[24:35] de acá con power
mpflash mpf y después de eso tenemos que
[24:41] pues no lo voy a hacer ahorita porque yo
ya lo tengo hecho pero al correr eso se
[24:47] nos va a crear estos dos archivos de
composer.reation y con powser.log este
[24:53] composer punto lo que es muy importante
Ya que usualmente se suele ignorar
[24:56] ignorar la carpeta vendor que es una
carpeta que también se crea de manera
[25:00] automática con todos los
todas las de las dependencias de la
[25:06] librería
esta carpeta es muy pesada y digamos
[25:09] para subirla a gits a github pues se
suele se suele ignorar esta carpeta por
[25:15] lo tanto el compost el punto lock es
donde están todas las instrucciones
[25:20] todas las dependencias instaladas y
simplemente es un archivo en el cual
[25:25] están todos los detalles de Cuál es la
versión exacta que necesita instalar y
[25:30] traer de la web en caso de que
trabajemos con alguien más o en caso de
[25:34] que cambiemos de computador bueno estos
dos archivos son muy importantes el
[25:39] compostera punto Jason me está diciendo
que yo estoy utilizando mpdf en la
[25:43] versión 8.1 sin más
[25:48] después de haber
corrido El Comando de composer required
[25:55] tenemos que correr el comando de
composer install
[26:01] y ya con eso debería comenzar a
funcionar
[26:06] Ahora
les voy a mostrar yo tengo pues una
[26:10] carpeta con
mi mis archivos de mpdf y el más Sí
[26:17] Prácticamente el que funciona es este
Esta es la la plantilla que yo utilicé
[26:21] que yo creé para poder pues generar el
PDF ya que esta librería lo que me
[26:26] permite es crear pdfs a partir de pues
html así que esto funciona de una manera
[26:34] pues muy simple simplemente Ah bueno
algo importantísimo que se me estaba
[26:40] olvidando Pues yo puedo imprimir un PDF
pero necesito traerme los datos de la
[26:46] cotización en específico que pues de la
cual quiero imprimir la cotización Sí
[26:51] así que esos datos pues me pareció más
fácil hacerlo tipo get digamos mediante
[26:59] la URL con el botón que yo les mostré
que había por acá
[27:05] con este botón de generar PDF lo que
hago es mandar mediante la URL todos mis
[27:12] datos Eso sí queda una URL larguísima
pero
[27:17] funciona pues bastante bien
mi botón está por acá
[27:25] nada más bueno Tengo este es el botón
donde yo mando todo todos todos mis
[27:32] archivos simplemente es un botón que me
redirecciona a mi archivo cotización
[27:38] punto php este archivo de acá de mi
carpeta mpf y le estoy mandando todos
[27:43] mis archivos le estoy mandando el ide de
la cotización el nombre del empleado el
[27:47] nombre de la constructora bueno todo eso
fácil lo que más me pareció complicado
[27:50] es poder enviarle los productos porque
tú como mandas
[27:59] unos productos que ni siquiera sabes Qué
cantidad de productos son puede ser un
[28:04] producto pueden ser dos pueden ser cinco
pueden ser 10 y pues lo más lo que más
[28:11] sentido le vi fue a lo mejor poder
mandar directamente el array Cómo puedes
[28:18] mandar un array por URL bueno resulta
que sí se puede mandar un array por URL
[28:23] de hecho es este esta variable de acá de
enviar productos Ese es mi manera de
[28:31] enviar una raíz mediante la URL Entonces
ahora sí venimos a estas líneas que
[28:38] habíamos ignorado antes Y pues
simplemente
[28:43] recordemos registro PDF es la variable
en la cual yo guardo todos los productos
[28:50] de mi cotización entonces utilizo en los
siguientes métodos primero sería Liz y
[28:57] en code entonces lo que hace él sería
Live es que representa un objeto en un
[29:04] String y URL en code pues lo que hace es
convertirlo para poder enviarlo mediante
[29:09] una URL simplemente Entonces eso queda
una cadena de texto enorme larguísima
[29:17] pero
digamos que es una manera en la que se
[29:21] puede hacer así que pues yo mandé todos
los datos por URL incluyendo mi array
[29:27] con mis productos luego aquí en
cotización lo que hago es recibir mi
[29:33] array Entonces yo recibo mi array
mediante el método get de productos y le
[29:41] aplicó estos tres estos tres métodos
para poder
[29:47] volverlo Y pasarlo de nuevo a una raíz
de hecho si deshacemos esto si
[29:53] descomentamos estas líneas de código
podemos ver que
[29:58] me genera me vuelve a pasar mi array el
array que yo había enviado desde mi otro
[30:05] archivo Así que eso es bastante
interesante y es algo que no sabía hasta
[30:10] haber realizado esta actividad es
bastante chévere entonces pues lo que
[30:17] hice fue guardar en variables
todos los
[30:21] cuero y parámetros que pues me mandé
mediante la URL las guarde en variables
[30:27] y simplemente las imprimí aquí en mi en
mi html eso
[30:33] no tiene digamos
grave pero lo que sí es de nuevo es la
[30:39] tabla la tabla de productos que se
genera al yo crear mi PDF esta tabla de
[30:45] acá porque lo mismo yo no sé cuántos
productos me van a enviar yo no sé o sea
[30:51] tiene que ser funcional para cualquier
cantidad de productos por lo tanto lo
[30:55] que decidí hacer fue crear una variable
Table que sea un String vacío y un
[31:02] forich
que me recorra mi array de matriz
[31:07] productos que es de nuevo mi array con
todos los productos de mi cotización y
[31:13] que me lo recorra y por cada producto me
genere una línea una una fila de mi
[31:19] tabla simplemente lo que hago es
concatenarle
[31:24] estas etiquetas Entonces le concateno un
TR de apertura le concateno el té de que
[31:32] tiene el ide del producto le
concatena un TD que tiene el nombre del
[31:39] producto y así mismo Pues todos los
datos de mi producto y eso que me lo
[31:44] repita por cada producto que necesito
imprimir simplemente por cada producto
[31:49] me genera una fila y ya eso es en
síntesis Y pues lo mismo que en el
[31:57] archivo pasado tengo una variable de
precio total a la cual se le van sumando
[32:02] el precio por día y para darme el total
el precio total y ya
[32:09] simplemente
cogí la variable Table y la imprimí aquí
[32:14] donde en medio de las etiquetas de
y ya simplemente pues utilizamos el
[32:23] método propio de la librería mpdf para
escribir el html y para pues generar
[32:30] nuestro PDF Así que con ayuda de
composer se pudo generar un PDF con los
[32:37] datos exactos de mi cotización Bueno eso
es en síntesis es todo lo que quería
[32:44] Mostrar espero realmente que se haya
entendido bien pues trate de mostrar lo
[32:51] que no se había podido
A lo mejor
[32:55] mostrar en clases anteriores las cosas
nuevas con las que me puse a
[33:00] experimentar que pueden A lo mejor ser
útiles para alguien más y eso es todo
[33:05] compañeros Espero que les haya gustado y
muchas gracias por por escuchar y por su
[33:09] tiempo

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
