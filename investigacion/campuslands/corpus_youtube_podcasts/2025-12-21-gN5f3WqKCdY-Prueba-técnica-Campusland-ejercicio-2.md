---
fecha: "2025-12-21"
contexto: campuslands
tipo: youtube-transcripcion
video_id: "gN5f3WqKCdY"
canal: "DevGamerColombia"
duracion: "N/A"
vistas: 17
url: "https://www.youtube.com/watch?v=gN5f3WqKCdY"
---

# Prueba técnica Campusland ejercicio 2

- **Canal:** DevGamerColombia
- **Fecha de subida:** 2025-12-21
- **Duración:** N/A
- **Vistas:** 17
- **URL:** https://www.youtube.com/watch?v=gN5f3WqKCdY

## Descripción del Video
```text
Ejercicio 2 adaptador de control Tv con Java
```

## Transcripción de Audio / Subtítulos

[00:06] Hola, buen día.
Jair Mona, aspirante a la vacante del
[00:13] docent en la empresa Camping Flight.
Continuación voy a hacer la sustentación
[00:19] del ejercicio dos de la prueba técnica
de campus.
[00:25] En este segundo ejercicio implemento el
patrón de diseño adapter.
[00:30] El objetivo es permitir que distintos
tipos de controles, incluyendo un
[00:35] smartphone, puedan manejar un televisor,
aunque tengan interfaces incompatibles.
[00:42] Con este ejercicio demuestro principios
de diseño como abstracción,
[00:48] polimorfismo, delegación de
responsabilidades y el principio
[00:52] abiertos errores.
[00:56] Eh, ¿cómo es la organización del
proyecto y paquete?
[01:00] Este, como sabemos, utilizo estoy
utilizando el ID entorno desarrollo
[01:09] y el ID Intel y ID. Sí,
acá está mi árbol del proyecto,
[01:18] mi organización del proyecto.
Todos los ejercicios está contenido
[01:23] dentro del paquete control TV. Hice un
paquete,
[01:28] un package y le coloqué como el nombre
control T para tenerlo bien organizado.
[01:35] El uso de paquete permite organizar,
[01:41] permite agrupar clases relacionad.
Todo este paquete está relacionado con
[01:48] con el tema del
del app control TV.
[01:54] evitar conflictos de nombres y mantener
el proyecto organizado, especialmente
[01:59] cuando el sistema crece.
[02:03] Entonces, acá ya estamos mirando
cómo tengo registrado mi proyecto. Todo
[02:09] organicé dentro del control.
[02:15] Eh,
comienzo definiendo la interfaz control
[02:22] TV. Control T
es esta.
[02:27] Esta
interfaza representa el contrato común
[02:33] que cualquier tipo de control debe
cumplir para interactuar con un
[02:38] televisor.
Gracias a esta interfaz, el sistema no
[02:43] depende de una implementación concreta,
sino de un comportamiento abstrato.
[02:48] Entonces, ¿cuáles son los
comportamientos de un control de T
[02:53] normal? son es encender, apagar,
eh subir el volumen, bajar el volumen y
[03:03] cambiar entrada.
Ya sabemos a qué referimos en cambiar
[03:08] sea o sí es HMI1, HM2.
Eso eso es referencia.
[03:18] Eso permite que el código
cliente trabaje siempre con control TV
[03:23] PB, independientemente si el de si el
control es infrarrojo, físico o el
[03:30] smartphone.
[03:34] Vuelvo implemento la clase del televisor
[03:40] que representa el dispositivo real.
Esta clase contiene la lógica de negocio
[03:46] del televisor
como encender, apagar, cambiar volumen o
[03:51] entrar.
El televisor no sabe quién lo controla,
[03:55] simplemente ponen métodos para ejecutar
opciones.
[04:00] Entonces, acá estamos. Televisor es
opción.
[04:06] public class televisor
son el paquet control
[04:12] tiene sus atributos que son privil
aplicando al filar
[04:19] de la programación orientado
gestoamiento
[04:22] está privar
[04:33] y están Hmm.
[04:39] Y acá estamos con los métodos de la
clase que son encender, apagar,
[04:47] subir volumen, bajar volumen y cambiar.
Esto, esto
[04:54] hace referencia un televisor de la
[05:04] eh
sigue el principio de responsabilidad
[05:09] única, ¿sí? Ya que el televisor solo se
encarga de su propio confort también.
[05:17] La la clase. Ahora vamos a la clase
control infrarrojo.
[05:25] Sí.
Control infrarrojo normal. El que
[05:33] eh la clase de control infrarrojo
implementa la interfaz control C. Acá lo
[05:39] podemos ver. public class control ojo
implements como en el primer ejercicio
[05:45] control Pierfaz
Control P
[05:51] representa un control tradicional
compatible con el televisor.
[05:56] Esta clase recibe un televisor por el
constructor
[06:02] televisor TV.
Esta
[06:09] clase reción televisor y por por el
constructor y delega todas las acciones
[06:13] al televisor.
Sí.
[06:17] Entonces acá como podemos ver control
implementa el control televisor private
[06:22] televisor que es de la del televisor y
por nombre.
[06:31] Entonces estamos colocando el
constructor, control infrarrojo,
[06:35] televisor
y
[06:41] eso escribemos todos los métodos del
televisor nuevamente
[06:48] es encender, apagar, subir volumen,
bajar volumen y cambiar entrada. Como
[06:53] podemos ver el el control TV si es
compatible con el televisor, ¿cierto?
[06:59] porque tiene este tiene está tiene
susasiones.
[07:14] Ahora proseguimos a la clase smartphone.
[07:23] Ahora creo la clase smartphone. Acá está
control TV. Esta el paquete o la carpeta
[07:33] y public class smartphone
[07:38] con.
[07:42] Entonces, obviamente, los eh los métodos
de un de un control por smart
[07:48] smartphone, o sea, que control del
televisor,
[07:52] eso hace referencia a un control de
televisor controlado por su smartphone o
[07:58] teléfono inteligente.
[08:02] como los hay hay en muchos regulares que
pueden controlar el televisor con su
[08:08] celular móvil y celular inteligente.
Entonces, pero entonces acá las los
[08:14] métodos no son compatibles. Sí, porque
está abrir app, conectar WiFi, tocar
[08:22] encender, tocar apagar, subir volumen,
app, bajar volumen app, seleccionar
[08:27] entrar.
Sí, no son iguales a
[08:33] al televisor
[08:39] esta clase representa un componente
externo o existente que no es compatible
[08:43] con interfaz control TN. Sus métodos
tienen nombre y flujos.
[08:50] Ver
esta es la interfaz del del control del
[08:54] televisor y se ve que ninguna es
compatible con la clase marat.
[09:02] Esos métodos tienen un nombre y flujos
distintos como abrir una app o
[09:05] conectarse a Wii, lo que impide usarla
directamente como control.
[09:12] Este es un escenario realista donde no
podemos modificar una clase existente o
[09:18] de terceras.
[09:23] Entonces, el problema de diseño, en este
punto existe un problema. El sistema
[09:28] espera un control TV, pero el smartphone
no cumple ese contrato. Sí, porque mire,
[09:36] que todos los todos los métodos son muy
diferentes a la interfaz del control.
[09:46] Modificar la clase smartphone no es una
buena práctica, ya que violaría el
[09:50] principio abierto cerrado.
[09:58] Eh, ahora entonces hacemos una entonces
que si no no podemos modificarla porque
[10:04] el smartphone tiene su propia clase,
¿cierto? Ellos ya vienen programados de
[10:09] fábrica con su propia con sus propios
métodos y algo que ya son este. Entonces
[10:16] no los podemos modificar, o sea,
podríamos fácilmente hacerlo, pero eso
[10:23] en la vida real no pasa colocar los
mismos métodos de la interfaz acá en la
[10:28] clase de smartphone, pero eso en la vida
real no pasa.
[10:32] Entonces, que lo que si pasa en la vida
real es hacerle unaorción
[10:37] para que sea compatible.
Entonces, ¿qué es la solución a este
[10:42] problema? Es para resolver este problema
implemento el patrón adapter mediante la
[10:48] clase smartphone adapter.
Entonces yo creé una clase smartphone
[10:53] adapter y acá es donde vamos a hacer
adaptar el smartphone a que sea
[10:59] compatible confaz del control.
Para resolver este problema implementa
[11:05] el patron adapter la clase smartphone.
Esta clase implementa la interfaz
[11:12] control. Entonces acá podemos ver public
smartphone adapter
[11:17] control.
[11:20] es, pero internamente utiliza un objeto
smartphone.
[11:26] Cada método del control se traduce a una
o varias acciones del smartphone.
[11:32] Entonces, acá lo podemos ver. Public
smartphone adapter
[11:36] y está implementado un un smartphone,
¿cierto?
[11:44] en el consultor.
[11:51] Aquí el adapter actúa como un traductor
entre dos interfaces incompatibles.
[11:57] No modifico la clase smartphone, sino
que la adapto cumpliendo el principio
[12:02] abierto cerrar.
[12:06] Entonces, ahora ya dice la el adaptador.
Sí. Ahora vamos
[12:12] al control TV.
[12:20] Es en la clase principal control TV
reguas del sistema.
[12:27] Esta es la clase principal. Mire
[12:32] out. Y acá vamos a probar nuestro.
[12:41] Creo un televisor y luego utilizo dos
controles distintos, un control infrar
[12:45] rojo y un y un smartphone adaptado.
Ambos se manejan como control TV, lo que
[12:53] demuestra polimorf.
[12:59] Entonces acá, acá lo tenemos.
Hacemos un objeto de televisor que llama
[13:05] TV
New Televisor. Sí.
[13:10] Entonces ahí hacemos los dos controles,
control TV, control 1, que es el intro
[13:15] rojo, y el control dos que es el
smartphone.
[13:19] El control smartphone adaptado.
[13:24] Y acá hacemos con el control infrar rojo
hacemos nuestra prueba, ver si funciona
[13:30] y hacemos nuestra nuestra prueba con el
smartphone.
[13:35] ¿Qué hace esto? que primero lo que hago
es encenderlo
[13:39] con el infier rojo, control
después subir volumen, después cambiar
[13:45] la entrada HMI2
y después lo aparto. Y lo mismo hacemos
[13:51] con el control de smartphone.
Lo encendemos ahí, lo estamos haciendo
[13:56] al mismo televisor que este, ¿cierto?
Estamos lo estamos haciendo. Entonces,
[14:03] lo que hacemos es control
eh el mismo TV, el mismo televisor
[14:09] estamos utilizando el control rojo y
control smartphone. Entonces, con el
[14:13] smartphone estamos haciendo un sender
también, subir volumen,
[14:18] cambiar entrada a Netflix y control dos
que es apagar con el smartphone.
[14:30] Y ahora le damos
run
[14:39] y nos menciona nuestro adaptado.
[14:44] Como podemos ver, control infrarrojo.
Sí, televisor encendido. Volumen subido
[14:52] 11. sabe que el volumen es + 1 es
subir volumen subido más 1
[15:03] 11
eh televisor cambiando entra HN 2 como
[15:11] lo definimos acá arriba y televisor
apagado.
[15:15] Y como podemos ver, el adaptador
funciona correctamente, ya que control
[15:21] de smartphone abriendo la PC del control
remoto, anentando el TV por Wi-Fi,
[15:28] enciendo TV desde Smartf, subiendo, ya
empieza subiendo el volumen desde la app
[15:35] seleccionando entrada Netflix desde
appriendo approxando
[15:42] el T por Wi-Fi, apagando el PV
[15:47] y listo.
Este ejercicio cumple no requerido en
[15:53] ejercicio.
Entonces, con este ejercicio demuestro
[15:57] la implementación
conecta conecta del patrón adapter,
[16:04] aplicando interfaces, delegación,
polimorfismo y principio sólid para
[16:09] integrar componente incompatible y
modificar su código original, ya que
[16:14] nosotros no
no
[16:19] cambiamos ningún código,
[16:23] solamente creamos una clase
[16:27] Adapter, que es la que
es la que va a manejar, es la que va a
[16:32] traducir todas las funciones
que vienen del control A smartphone. Lo
[16:40] traduce para que lo pueda leer el
control T.
[16:48] Muchas gracias por Ok.

---
## 🔗 Conexiones del Segundo Cerebro
- **Entidad:** [[areas/campuslands|Campuslands]]
- **Dossier Central:** [[investigacion/campuslands/dossier_campuslands_completo|Dossier Campuslands Completo]]
- **Investigación Diego Tarazona:** [[diego_investigacion/README|MOC Investigación Diego Tarazona]]
