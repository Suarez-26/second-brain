---
fecha: "2023-06-13"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "mkjAgWwwQqw"
canal: "Campuslands"
duracion: "9:19"
vistas: 6
url: "https://www.youtube.com/watch?v=mkjAgWwwQqw"
---

# Proyecto javascript 04 | Campuslands

- **Canal:** Campuslands
- **Fecha de subida:** 2023-06-13
- **Duración:** 9:19
- **Vistas:** 6
- **URL:** https://www.youtube.com/watch?v=mkjAgWwwQqw

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

[00:01] bueno estimados Campers vamos a comenzar
con el cuarto vídeo más o menos no
[00:08] recuerdo bien en este cuarto vídeo vamos
a seguir trabajando con nuestra
[00:12] aplicación de farmacia vamos a recordar
un poco en lo que quedamos en el
[00:17] anterior video
[00:20] para seguir nuestra cadena de producción
estemos nuestra página principal
[00:26] vamos en Index ya tenemos nuestros
clientes
[00:31] esto ya funciona correctamente
ahora lo que vamos a hacer es que en
[00:37] esta tabla se cargue la información de
todos los usuarios de todos nuestros
[00:44] clientes Ok entonces vamos vamos a
hacerlo vamos a mirar cómo cómo lo
[00:48] podemos lograr
[00:52] recordemos que anteriormente habíamos
creado
[00:56] este elemento
donde teníamos definido que ahí vamos a
[01:02] colocar nuestro diseño el diseño de
nuestro nuestra pantalla de nuestra
[01:08] lista la cual se encuentra
de manera fija por acá Ok entonces lo
[01:17] que vamos a hacer inicialmente es que
esta tabla
[01:21] la voy a trasladar directamente para
[01:27] nuestro web component en un control x
por acá y nos vamos para el hueco poner
[01:36] la lista y lo voy a pegar por acá
perfecto como es como primero vamos a
[01:45] justificar esto
segundo pues vamos a ajustar todo voy a
[01:53] tener el vídeo para hacer el ajuste de
la orientación y así no demorarnos mucho
[01:58] Okay miremos acá Entonces si nos damos
cuenta Aquí tengo definido ya
[02:07] la carga
de mis registros estos registros están
[02:13] en ese archivo Jason entonces te voy a
mostrar
[02:20] nuestros dos registros ahora viene la
pequeña explicación
[02:28] lo primero que tenemos que hacer es
arreglar un poco nuestra
[02:34] Api recordemos que esto es una promesa
Recuerden que las famosas tienen dos
[02:39] opciones si se cumplen y se cumplen acá
estoy indicando que por favor me retorne
[02:46] el resultado de esta fecha que hago
desde esta solicitud que le estoy
[02:53] haciendo a mi servidor
[02:59] Entonces
él me va a retornar algo y ese algo es
[03:05] un elemento en formato
Luego si nos vamos para nuestra lista
[03:12] customer
importantísimo tenemos que hacer la
[03:16] importación del método que voy a
utilizar
[03:19] muy interesante porque estamos
independizando
[03:23] funcionalidad en cada uno de los web
componentes Es simplemente nos dedicamos
[03:28] a llamar el elemento que nos interesa
aquí tenemos el constructor el render el
[03:37] rico es aplique cliente
aquí tenemos el render donde estamos
[03:42] Armando la tablita
[03:46] aquí tenemos el rico es cliente que
básicamente lo que estamos haciendo es
[03:52] llamando
la función flecha y al final se
[03:56] convierte en una promesa
recordemos que debemos de preparar las
[04:01] promesas cuando se cumpla tenemos que
Hallar el té tenemos el resumen que va a
[04:08] almacenar lo que me retorne esa promesa
luego de esto llamamos el método render
[04:15] clientes y le pasamos resulta que en
este caso resulta es el objeto literal
[04:23] que viene desde desde
[04:30] acá simplemente llamamos render clientes
el cual vemos una variable vamos a
[04:37] cambiar este nombre Vamos a ponerle
doble click f2
[04:54] limpiamos esa variable luego le
concatenamos crear lista clientes html
[05:01] donde le enviamos cada objeto que viene
nuestro array recordemos que este array
[05:08] Perdón dije anteriormente que era uno
pero no es una raíz es una raíz
[05:15] que contiene unos objetos literales
entonces aquí estamos recorriendo ese
[05:24] arreglo donde cada vez que se cumple
este ciclo se va obteniendo cada
[05:30] elemento el cual se lo estoy enviando a
la función crear lista clientes html
[05:37] donde acá simplemente renderizó la
información clientes clientes clientes
[05:42] clientes clientes
que es el parámetro que se pasa a través
[05:46] de
la llamada de la función donde aquí
[05:51] tenemos cada uno de los atributos ok
luego de esto tenemos el get Element que
[05:59] es lista clientes donde le hacemos un
email hpml
[06:04] ese señor está por acá arriba que es el
t-body que va a contener
[06:12] la información
ya va a contener la información
[06:22] de agrupar de nuestros clientes Entonces
de esta manera hemos logrado que esto
[06:29] funcione a la mil maravillas Entonces
vamos a hacer la prueba a ver si se
[06:35] refresca la página y podemos obtener la
información de la lista de nuestros
[06:40] clientes hasta ahora los botones que
tenemos acá no tiene ningún tipo de
[06:45] funcionalidad tenemos que aplicar lo que
ya vamos para allá
[06:48] entonces vamos a clientes
fecha de registro el día de hoy número
[06:55] del documento
1 2 algo así y vamos a colocarle
[07:02] Carlos
[07:06] no sé más qué sé yo
y de correo electrónico CN arroba Gmail
[07:22] y vamos a colocar por acá una
información
[07:25] fecha de nacimiento vamos a colocar por
acá repasamos en el tiempo
[07:31] tenemos este señor nació en el 2003
[07:36] en mayo
[07:46] ocho y lo voy a guardar y fíjense que él
de manera automática como se hace el
[07:53] refresco de una vez me refresca nuestra
tabla interesante fabuloso ya aquí
[08:00] tenemos ese listado de clientes y
estamos haciendo estamos cumpliendo con
[08:05] uno de los elementos del crudo que es el
de leer
[08:12] Entonces en este pequeño vídeo
nos dedicamos a estudiar el Cómo podemos
[08:20] cargar la información con el código que
ya tenemos desarrollado
[08:28] a continuación a continuación lo que voy
a hacer
[08:33] es a que cuando vemos le damos clic por
acá en el botón de editar Ok me debería
[08:40] aparecer el formulario nuevamente pero
con la información cargada en él en el
[08:49] formulario con los datos de este señor
los cuales quiero modificar entonces
[08:56] Pero eso lo vamos a dejar entonces para
el siguiente video para que este dedito
[09:00] sea corto y directo

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
