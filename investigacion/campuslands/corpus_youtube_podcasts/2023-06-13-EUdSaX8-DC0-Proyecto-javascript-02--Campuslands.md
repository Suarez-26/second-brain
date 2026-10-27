---
fecha: "2023-06-13"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "EUdSaX8-DC0"
canal: "Campuslands"
duracion: "29:56"
vistas: 3
url: "https://www.youtube.com/watch?v=EUdSaX8-DC0"
---

# Proyecto javascript 02 | Campuslands

- **Canal:** Campuslands
- **Fecha de subida:** 2023-06-13
- **Duración:** 29:56
- **Vistas:** 3
- **URL:** https://www.youtube.com/watch?v=EUdSaX8-DC0

## Descripción del Video
```text
¡Descubre el fascinante mundo de la programación con nuestro proyecto de JavaScript! En este video, te llevaremos en un viaje de aprendizaje interactivo, donde explorarás las maravillas de JavaScript y su poder para crear aplicaciones web dinámicas.

#soycampuslands #campuslands #javascript  

Suscríbete:
Canal Oficial Campuslands: En nuestro canal, encontrarás una amplia gama de contenido diseñado para todos los niveles, desde principiantes hasta programadores experimentados que desean ampliar sus conocimientos. Nuestro objetivo es hacer que la programación sea accesible para todos, sin importar tu experiencia previa.

Síguenos en nuestras redes sociales: 
Facebook: www.facebook.com/Campuslands/
Instagram: www.instagram.com/campuslands/
Landing page: www.campuslands.com/
```

## Transcripción de Audio / Subtítulos

[00:03] Bueno vamos a continuación a este
desarrollo de la farmacias La idea es
[00:10] que ahora vamos a hacer la configuración
de Jason server vamos a ver cómo se
[00:17] configura en el sistema operativo
Windows
[00:22] Vamos a ingresar por aquí la terminal se
van a dar cuenta que es Exactamente
[00:27] igual a como lo trabajamos desde Linux
para eso pues vamos a abrir
[00:34] navegador web y vamos a buscar la página
oficial que es el github Entonces vamos
[00:43] a buscar como Jason server git
perfecto
[00:49] vamos a buscar por acá
[00:53] y lo primero que nos dice es que
lo instalemos
[00:59] lo instalemos un control c pero antes de
instalarlo antes de instalarlo es muy
[01:06] importante
inicializar
[01:09] el Jason
para inicializar el paquete Jason damos
[01:16] El Comando npm
[01:19] y menos
[01:24] posterior a esto si instalamos
el Jason server un enter esperamos un
[01:32] momento que se haga la descarga y la
configuración
[01:52] listo aquí me dice que quedó instalado
correctamente
[01:56] Ahora nos queda es continuar trabajando
con nuestro proyecto
[02:03] vamos ahora a configurar las tablas
vamos a mirar la documentación oficial
[02:09] tenemos por acá según la documentación
oficial nos dice que tenemos que crear
[02:15] un archivo db
este archivo nosotros lo podemos Ubicar
[02:19] en cualquier parte de nuestro proyecto
lo importante Sí es que contengan
[02:24] inicialmente ese archivo de contener un
objeto de tipo
[02:32] Jason
su interior estará compuesto de cada uno
[02:36] de los elementos
[02:40] tributos clave valor donde el valor de
cada tributo eso array Entonces vamos a
[02:46] mirar como lo estructuramos
por acá
[02:52] llaves y vamos a trabajar con clientes
[03:07] los puntos
y lo tenemos de esta forma ya aquí
[03:11] podemos manipular la información incluso
vamos a hacer que nuestra farmacia esté
[03:17] funcionando a nivel nacional
Entonces vamos a tener ciudades
[03:25] y vamos a establecer una relación mi
relación entre ciudades y Costa Vamos a
[03:33] ponerle
[03:40] de esta forma
[03:44] bien Ahora ahora vamos a empezar a
construir nuestros elementos
[03:50] lo primero que debemos hacer es
determinar Qué elementos va a tener
[03:56] customers Cuáles son esos atributos para
así poder armar el formulario
[04:03] para nuestro ejemplo vamos a hacer que
customer tenga cédula nombre apellidos
[04:11] dirección teléfono correo electrónico
etcétera entonces vamos a abrirnos por
[04:18] acá el bloc de notas
o el notepad que todos conocemos
[04:25] y vamos a colocar lo siguiente para que
no se nos olvide
[04:29] es customer
va a tener cédula nombres
[04:38] apellidos y
[04:43] teléfono
y vamos a colocarle
[04:51] porque tenemos una relación con ciudades
[Música]
[04:57] por defecto Jason server siempre le va a
agregar el atributo ID a cada uno de
[05:03] esos elementos y lo va a tomar como su
identificador
[05:09] Entonces vamos a colocar acá Siri
[05:16] no listo Entonces esto nos va a ayudar a
tener una referencia para poder generar
[05:22] nuestro formulados
por acá ya la tenemos Clara y ahora sí
[05:28] vamos a empezar a definir el formulario
el formulario va a ser otro web Company
[05:35] pero para eso vamos a contar con una
página web
[05:41] que se va a llamar
[05:45] punto
html
[05:49] perfecto inicializamos esto
vamos a importarle bustra vamos a
[05:57] importar a punto js para tener inclusión
de la librería etcétera es un control c
[06:03] y lo tenemos por acá
[06:14] muy bien perfecto entonces aquí en este
momento pues vamos a definir nuestros
[06:21] encabezados
vamos a definir en este caso va a tener
[06:27] el menú Entonces como ya tenemos el
componente vamos
[06:32] Main menú
[06:38] vamos a tener nuestra
cuerpo principal
[06:45] y aquí entre nuestro cuerpo principal
vamos a tener un punto
[06:50] container
perfecto ya con esto hemos estructurado
[06:56] customer punto
html bien Entonces vamos a construir
[07:02] nuestro formulario basado en un
componente entonces aquí donde dice
[07:07] Force vamos a crear todos los
formularios que necesitemos hemos clic
[07:12] derecho un archivo
[07:15] customer
guión
[07:20] punto js recordemos que siempre los
componentes deben estar expresados en
[07:27] palabras compuestas separados por un
guión medio importante tener en cuenta y
[07:33] no olvidarlo
Perfecto entonces aquí vamos a tener la
[07:38] palabra es por nuevamente recordemos que
este componente que exportarlo
[07:46] el nombre de nuestra clase customer
[07:54] recordemos que extiende
[08:00] de html
[Música]
[08:13] recordemos que tenemos un constructor
[08:21] donde ese constructor
tiene un súper que recordemos que el
[08:28] súper está indicando que esta clase va a
heredar de la clase superior Es decir de
[08:36] html elements
vamos a poner dis punto render que es un
[08:42] método que vamos a crear en un momento
el cual se va a encargar de renderizar
[08:48] lo que necesitemos en la página web
Entonces ya vamos a crear aquí render
[08:55] su método
[08:59] Aquí vamos a darle 10 puntos
html igual
[09:07] vamos a poner acá html
[09:13] nuestro famoso back
visto
[09:18] aquí al final vamos a colocar custom
Element punto de find
[09:25] donde vamos a colocar el nombre de
nuestra nuestro web componente en este
[09:31] caso se va a llamar
guión
[09:38] y acá lo relacionamos con la clase
customer
[09:44] perfecto ahora que necesitamos hacer
construir nuestro formulario OK Para el
[09:51] formulario Pues voy a tomar un
formulario ya trabajado anteriormente lo
[09:56] voy a modificar por aquí vamos a
eliminar algunas cosas ya que la idea es
[10:02] que este formulario sólo va a contener
el botón de guardar
[10:07] solamente para guardar datos del usuario
vamos a borrarlo acá
[10:17] eliminar y editar lo vamos a hacer a
partir de una lista
[10:22] vamos aquí la información
[10:36] según lo que creo que borramos algo que
no deberíamos borrar
[10:42] Okay no está perfecto
[10:57] pertenece este señor no no tome mal
esto viene acá
[11:06] Ahora sí vamos a eliminar esto
[11:13] vamos a eliminar
información solamente va a quedar
[11:17] guardar
[11:26] entonces
[11:32] todavía debe pertenecer a este señor
[11:39] sí
cinco y estar por acá
[11:44] este DIF debería pertenecer de la parte
inferior Pues eso
[11:52] es como
orden
[11:55] establecerle a nuestro código para tener
bien claro en donde se abre en donde se
[12:02] cierran los elementos este señor viene
por acá
[12:06] que tenemos esa información
este formulario
[12:11] y por aquí tenemos un dip principal que
nos va a ayudar
[12:18] bueno es importante como les indicó
tener claro ser muy ordenados con cada
[12:26] elemento vamos a ordenar esto
[12:34] clase podemos eliminar el resto para
personalizar lo que necesitamos Entonces
[12:40] vamos allá
voy a borrar todo esto
[12:47] posiblemente las fechas de nacimiento no
porque creo que vamos a necesitar algo
[12:52] con fecha de nacimiento
[13:00] se pertenece acá
[13:06] es importante que cuando copien y peguen
tengamos muy claro la ideación porque
[13:12] eso puede ser fatal Al momento de
desarrollar
[13:21] entonces Vamos a repasar nuevamente
dientes Cuáles son los elementos que
[13:26] tiene
la cédula
[13:30] entonces aquí vamos a colocarle de esa
[13:36] forma incluso voy a dejarle ese atributo
que me parece muy interesante que es la
[13:43] fecha de creación
vamos a dejarlo activo
[13:48] para que se seleccione o incluso esto lo
podemos tomar como un campo oculto campo
[13:55] oculto
vamos a tener entonces
[13:59] nombres
con cédula nombres y apellidos entonces
[14:07] ccc
[14:15] todo cédula
[14:21] o no vamos a colocarle más bien un
documento
[14:27] documento
[14:35] o sea duplicar esto control
[14:41] ubicamos estos son los nombres
[14:49] [Música]
[14:53] recordemos que estos elementos son los
que nos van a ayudar a estructurar el
[15:00] objeto
[15:04] apellidos vamos a poner aquí nombres
recordemos que estamos manejando el
[15:11] sistema de búsquedas de 12 columnas
Entonces por acá tenemos que vamos a la
[15:16] fecha registro Vamos a ponerle tres
cuatro cuatro ocho doce
[15:21] vamos a reducirle
[15:25] tenemos 3 6
[15:31] 10
soles
[15:37] dos tres
tres seis nueve y acá tres
[15:43] y ahora verificamos si podemos modificar
algo más del tamaño
[15:48] que otros datos necesitamos del cliente
juntamos el email
[15:54] y el teléfono
email
[15:59] y teléfono email
[16:03] y teléfono
[16:08] teléfono
[16:14] vamos para acá
pegamos por acá
[16:19] la fecha de nacimiento
[16:25] vamos a colocarle el atributo fecha nac
[16:34] vamos a tomar nuestra colección
pegamos acá
[16:41] pegamos acá y pegamos acá
perfecto con esto pues teoría tenemos ya
[16:51] nuestro formulario vamos ahora a
vincular este formulario a
[17:04] Costa para poderlo vincular a customer
pues lo primero que tengo que hacer es
[17:10] importarlo no
[17:18] punto
[17:22] componentes es las
[Música]
[17:33] aquí ya tenemos
la importación de El formulario ahora
[17:40] necesito definir que mis contenedores
como va a fluir la información
[17:46] tenemos el menú principal
estamos importando el Jason aquí el
[17:53] Index tenemos el menú y por acá tenemos
que Definir la página web de
[18:00] customers
punto html
[18:05] para poder establecer enlace con la
tabla perdón con la página de costo
[18:12] vamos a revisar vamos a revisar Cómo
están nuestro documento si está
[18:18] funcionando bien hasta ahora si está
cargando bien si se carga el menú y si
[18:23] se carga nuestro componente de customers
Ok pero acá vamos a colocar hundir
[18:46] simplemente para probar que esté
funcionando bien vamos a poner
[19:04] vamos acá vamos a comprobar que por lo
menos está cargando ya nuestro
[19:10] formularios y así podemos continuar La
idea es que ese formulario vamos a
[19:16] colocarlo vamos a colocarlo en
[19:23] un en un modal
vamos a cambiar el contexto lo que hemos
[19:28] trabajado
[19:36] acá aparece tenemos un problema f12
[19:42] dice súper solo es válido consultor
derivado vamos a mirar qué error cometí
[19:49] por acá
[20:08] ok
[20:23] lo que está pasando
[20:27] si está bien
[20:35] el menú render
[20:41] wow
[20:46] customer
super
[21:02] no vamos a poner pausa y verificamos
a ver Ya encontré el error
[21:08] un súper error de escritura si ustedes
se dan cuenta que hice con constructor
[21:16] son errores fatales porque al momento de
nosotros codificar pues así que son
[21:25] imposibles de encontrar tenemos acá
clientes
[21:30] igual a ya tenemos nuestro formulario o
se hace que en ese momento nuestro
[21:37] formulario está funcionando pero súper
bien listo Entonces ya con esto Tenemos
[21:44] un gran Avance en donde estamos creando
nuestra interfaz vamos a trabajar con la
[21:51] interfaz primero y luego vamos a
trabajar con la parte de los servicios
[22:01] Ok Perfecto entonces nos vamos a ocupar
del diseño inicialmente que queremos
[22:07] hacer
queremos hacer y bueno Tenemos aquí a
[22:12] clientes
hemos estado barra lateral
[22:17] esta barra lateral tenemos home que nos
vuelve la página principal
[22:21] clientes
es que cuando llegué aquí aquí clientes
[22:26] me muestra un formulario modal
manzana moda esa ventana modal va a
[22:32] contener el formulario para ingresar la
Data del frente buscador
[22:38] me va a abrir una sección que me va a
permitir Buscar
[22:43] los clientes un buscador personalizado Y
de esa manera pues vamos a trabajar aquí
[22:50] voy a vincular
los iconos para esto entramos a la
[22:56] página de voz icons y por aquí tenemos
la opción de enlace por medio de cdn
[23:06] o sea un control
c venimos para
[23:12] nuestro
[23:15] esta página web en este caso clientes
Entonces nos interesan encolar los
[23:21] iconos
nos insertamos
[23:25] y por acá tenemos
lo siguiente
[23:30] tenemos los enlaces un enlace y aquí
tenemos la opción del icono pero vamos a
[23:37] personalizarlo para nosotros aquí
tenemos home tengo para la página
[23:42] oficial de los iconos vamos a buscarla
[23:52] acá
atrás y aquí buscamos
[24:00] ya que nos aparecen unos
ciclos vamos a buscar la casita
[24:05] aquí nos indica buen componentes en este
caso no vamos a traer a trabajar con
[24:11] webcompone sino como fuente y le vamos a
dar clic para copiar
[24:17] venimos para nuestro documento html
[24:24] y lo pegamos por acá
[24:29] en teoría con esto debería salir
el icono vamos a revisar
[24:39] y aquí tenemos la casita vamos a cambiar
esos colores
[24:45] vamos a asignar para clientes y para
buscador
[24:49] Entonces vamos a buscar otro icono
[25:02] de búsqueda
a la Lupita
[25:07] le damos clic
buscamos nuestro
[25:13] enlace
vamos a pegar por acá
[25:24] vamos a clientes vamos a clientes
Buscamos un icono para clientes se puede
[25:32] ver si customer aparece algo
[25:39] Así un poco person
[25:52] vamos a buscar
por ejemplo
[25:58] este señor para indicar que vamos a
agregar
[26:02] seleccionamos
venimos para
[26:10] momento y lo pegamos perfecto
[26:15] ya con eso Hemos puesto los iconos que
nos van a ayudar
[26:22] creo que me equivoqué Le puse en el
buscador de tono de
[26:38] como estos iconos son basados en texto
yo puedo agrandarlos puedo agrandarlos
[26:45] cómo se hace
debemos crear
[26:49] css personalizado
[26:57] sencillo
[27:03] [Música]
[27:34] Paty
cero píxeles
[27:43] entonces
[27:46] podemos decirle
[27:53] que sus iconos
[27:57] vamos a buscar iconos por acá
y buscamos la clase de
[28:10] tamaño más grande
[28:22] lo podemos asignar fácilmente
[28:38] [Música]
[28:43] vamos a vincular nuestro nuestra nuestra
hoja de estilo
[29:06] y aquí como vemos ya no están un poquito
perfecto
[29:14] Si queremos cambiar la fuente en color
blanco pues lo podemos hacer sin ningún
[29:19] problema listo ese menú Es estático no
vamos a darle ninguna interactividad
[29:25] para que se oculte nadie es que en esta
área blanca vamos a trabajar con
[29:31] nuestros elementos
Entonces vamos a darle pausa este video
[29:36] y en el siguiente continuamos trabajando

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
