## 1. DESCRIPCION DEL JUEGO

### 1.1. HISTORIA

- Nuestro protagonista, Jaro, se adentra en las oficinas centrales del banco
    mas malvado del planeta. Allí se encuentra que la forma del banco cambia
    cada vez que entra y que todos los trabajadores han sido convertidos en
    esclavos agresivos.
- Jaro deberá recorrer los 3 pisos del banco derrotando los enemigos y
    recogiendo todo el dinero posible hasta llegar al ultimo piso donde se
    enfrentará con el director
- Nuestro protagonista tendrá un tiempo limitado para permanecer en el
    edificio, dictaminado por el tiempo que tarden en llegar los policías tras
    que hayan sonado las alarmas


### 1.2. JUGABILIDAD


- El juego consiste en un topdown shooter roguelite como the binding of
Isaac o enter the gungeon. Podremos recoger dinero, disparar, esquivar y
explorar niveles generados proceduralmente.
- El bucle de juego principal consiste en avanzar a través de la mazmorra
recogiendo el máximo dinero posible, escapar, convertir el dinero en
tiempo y repetir la mazmorra pudiendo avanzar más lejos hasta que se
complete el tercer piso.
- TopDown Shooter: El jugador controla al personaje con vista de pájaro y
sus armas abriéndose paso en salas llenas de enemigos. El jugador tendrá
capacidad de esquivar las balas en caso de que la situación se ponga tensa
- Roguelite: Evolución del genero roguelike en el que cada partida se
generaba el mapa de la mazmorra proceduralmente y el jugador debía
empezar de cero. La diferencia de roguelite a roguelike es que el jugador
guarda progresión entre los diferentes asaltos a la mazmorra. En este caso
la progresión que se guarda es el dinero para poder invertirlo en tiempo
dentro de la mazmorra para poder avanzar.
- La mecánica única del juego es el tiempo de permanecer en la mazmorra.
El jugador tiene que abandonar o completar la mazmorra antes de que se
le acabe el tiempo para evitar llegar a un GAME OVER. Cuando termina un
piso y se derrota al jefe se da la decisión de huir e invertir todo el dinero
conseguido en más tiempo para el siguiente asalto o continuar.
- La muerte, como en la vida misma (Y los arcades clásicos), es permanente.
El jugador deberá pensar muy bien lo de continuar a un nuevo piso o
perder todo su progreso.


### 1.3. MANUAL DE USUARIO


- Controles:
o Movimiento del jugador: WASD. Movimiento en 8 Direcciones.
o Apuntado: Flechas de dirección, Disparo en 4 Direcciones
o Esquive: Barra espaciadora.
o Iniciar nivel: Backspace (Tecla de borrado)


- Elementos del juego:

```
1) Jugador: El personaje jugable
2) Bala del jugador, impacta con enemigos
3) Bala del enemigo, impacta con el jugador
4) Enemigos, se acercan hasta el jugador para acabar con él
5) Puerta de sala, se abrirá cuando se maten a todos los enemigos y
podremos avanzar hasta la siguiente sale
6) Pared, nos permite cubrirnos de balas enemigas
7) HUD:
a. HP: Indica la vida del jugador, cuando llegue a 0 el juego
habrá acabado
b. Money: Indica el dinero expropiado por el jugador durante
esta run
c. Floor: Indica el piso en el que nos encontramos
d. Time: Indica el tiempo restante antes de que llegue la
policía y tengamos un inevitable game over.
8) Cuerda Huida, nos permite escapar de la dungeon antes de
terminarla con el dinero recaudado
9) Warp, nos permite cambiar de piso una vez derrotado al jefe
10) Dinero, el dinero es dinero
```
- Pisos: El Palo tiene 3 pisos, identificados por distintos colores (Azul,
    Amarillo y Rojo). Estos colores indican su dificultad.
- Personajes:

```
El Jaro: Protagonista del juego, el avatar del jugador. Tras una infancia
difícil decide atracar un banco para por fin sacarse a él y a los suyos de la
pobreza.
```
```
Enemigo de primer piso: Oficinista del banco en los pisos más bajos,
bastante débil y poco agresivo. Viste un uniforme azul.
```

```
Enemigo del segundo piso: Oficinista superior del banco en pisos
intermedios, un poco más rápido y agresivo que el azul pero no mucho.
Viste uniforme amarillo.
```
```
Enemigo del tercer piso: Oficinista senior del banco en pisos elevados,
bastante más rápido debido al abuso de sustancias químicas. Ataca con
armas automáticas. Viste con uniforme rojo.
```
```
Jefe de piso: Director de cada uno de los pisos. Tiene bastante vida
debido a las mutaciones genéticas sufridas. Ataca con un arma rápida y
contundente.
```
### 1.4. GAMEPLAY

- En la carpeta documentación se encuentra un archivo mp4 de una run
    completa del juego.


## 2. DETALLES DE IMPLEMENTACION

### 2.1. ESTRUCTURA DEL CODIGO

- game.py: Clase principal del juego. Contiene las funciones de inicialización
    de datos, limpieza de datos e implementaciones de las pantallas
    disponibles. Contiene referencias a los managers y listas de objetos.
    Pantallas:
       o start_screen: pantalla de inicio
       o gameover_screen: pantalla de derrota / timeout
       o playgame_screen: pantalla de juego
       o victory_screen: pantalla de victoria, tras terminar el ultimo piso
       o runaway_screen: pantalla de huida, tras terminar un piso y huir

- manager.py: Archivo de los managers del juego. Contiene los managers de
    niveles, de sonido y de HUD.
       o FloorManager: se encarga de administrar los pisos que se
          muestran por pantalla. Contiene referencias a todos los mapas
          para poder limpiarlos fácilmente. Sus funciones mas importantes
          son end_floor (limpiado) y request_floor (pedir nuevo nivel). Los
          pisos se generan por adelantado y se muestran por pantalla a
          peticion del game
       o AudioManager: se encarga de administrar los sonidos
          reproducidos y los canales de estos. Contiene referencias a los
          audios y todas las clases que usen sonidos acceden a él a través de
          game
       o HUDManager: se encarga del dibujado de la HUD para cada una de
          las pantallas. Contiene una función para cada una de las pantallas.
          Mirado en retrospectiva esto pudo haberse implementado
          mediante abstracción (teniendo por ejemplo hud_gameover,
          hud_starscreen que implementen hud_abstract) y una
          implementación distinta de show_hud() para cada una.

- Animation.py: Clase que define una animación. Esta clase es totalmente
    auxiliar y su único objetivo es facilitar el workflow con animaciones.
    Permite dada una Sprite sheet y una velocidad de frame crear una
    animación de forma fácil. Sus función mas importante es get_frame(), que
    devuelve la imagen correspondiente al frame de animación.

- Camera.py: Clase que define la “cámara” del juego. Le llamamos cámara
    por comodidad, pero lo que hace es desplazar todos los gameobjects
    relativos a la posición del jugador. La cámara tendrá indicado un mínimo y
    un máximo de pantalla para mantener centrada la acción.

- Settings.py: Archivo que contiene la configuración de la aplicación, con
    detalles tales como el numero de habitaciones por piso, el tamaño de
    ventana o el numero de pisos por partida.

- Data.py: Archivo que contiene las clases de datos de las entidades del
    juego y las armas. También contiene la lógica de la vida de los personajes y
    las funciones para recibir daño teniendo en cuenta el tiempo de
    invulnerabilidad. El principal objetivo de esta clase es separar lógica de
    datos para su más fácil manejo. Mirado con retrospectiva hubiera sido
    cómodo que esta clase recogiese los datos de otro archivo aparte en vez
    de tener los números hardcodeados, así como de también encargarse de
    todos los datos de los sprites a modo de manager de recursos.
    
- Sprites.py: Archivo que contiene los sprites de los elementos del juego. Las
    relaciones de estas clases serán explicadas más adelante. Las clases son:
       o Player
       o FirstFloorEnemy, SecondFloorEnemy, ThirdFloorEnemy,
          BossEnemy
       o Gun, Bullet
       o Background
       o Door, Rope, Wall, Warp
       o Money
- Tilemap.py: Archivo que se encarga de todo lo relativo a la creación
    procedural de mapas y niveles. Su funcionamiento será explicado más
    adelante. Contiene las siguientes clases:
       o Floor : Clase decoración que contiene un piso entero y sus
          funciones para generarlo y borrarlo
       o Map : Clase que define el piso mediante la carga de habitaciones
          desde un archivo, la elección aleatoria de estas y la generación de
          objetos
       o Room : Clase auxiliar usada para contener los datos de cada una de
          las habitaciones y facilitar su borrado posterior.
       o BossRoom : Clase auxiliar usada para contener los datos de una
          habitación de jefe y facilitar su borrado posterior. Visto en
          retrospectiva pudo haberse diseñado como una extensión de
          Room o que ambas fuesen implementaciones de AbstractRoom.


### 2.2. ASPECTOS RELEVANTES


- La clase principal del juego es game, que se le pasa como referencia a
todos los sprites a la hora de inicializarse para que estos puedan acceder a
las funciones de estado y a los managers.
- El juego cambia de estado cuando alguno de los sprites lanzan la función
de “run_xxx_screen”, aunque fue considerado un patron observador en el
que la propia clase del juego es la que decide cuando cambiar de estado
basado en el jugador.
- El juego corre mediante sincronización del reloj a unos fps indicados en el
archivo de configuración.
- La implementación del mapa se basa en un tilemap con cuadriculas, de
forma que es super fácil diseñar salas para él y, en un futuro, implementar
inteligencias artificiales complejas para los enemigos basándose en
algoritmos de búsqueda.
- La configuración del mapa se almacena en settings.py, donde tenemos el
tamaño de las tiles, el tamaño de las habitaciones del mapa, el número de
habitaciones por piso y el número de pisos.
- Los diseños de habitaciones se almacenan en un txt donde están
codificados basándose en caracteres, que luego son parseados por la clase
de tilemap.py para generar los gameobjects correspondientes.
o Números: Paredes
o E: Enemigo

- Los diferentes pisos del juego contienen diferentes enemigos que también
    son decididos a la hora de generar en tilemap.py. También esta
    considerado en el código la posibilidad que los diseños de habitaciones
    cambien según el piso.
- Los grupos de sprites en el juego son:
    o **Background** : se dibuja antes que el resto, es el fondo (color plano)
       de las habitaciones
    o **Walls** : Almacena las paredes y las puertas cerradas, usado para
       detectar colisiones
    o **Enemy** : Almacena los enemigos, usado para detectar “daño”
    o **Player** : Almacena al jugador, usado para detectar “daño”
    o **Rope** : Almacena las cuerdas que dropea el boss cuando es
       destruido
    o **Warp** : Almacena los warps que nos permiten cambiar de piso
    o **Money** : Almacena las bolsas de dinero que el jugador recolecta
- El uso de los distintos grupos de sprites es mayormente dentro de la clase
    Jugador, que tiene funciones para on_<group_name>_collide
- Las clases jugador y enemigo son las dos extensiones de la clase Entidad,
    que contiene el comportamiento común de movimiento y apuntar y tanto
    jugador como enemigo se encargan de definir cuando se realizan estos
    movimientos:
       o **Enemigo** : El movimiento y apuntado se hace basándose en la
          posición propia y la posición del jugador
       o **Jugador** : El movimiento y apuntado se hace mediante teclado
- Las clases <nth>FloorEnemy y BossEnemy son extensiones de la clase
    Enemigo pero con diferentes datos y sprites introducidos
- En cuanto el jugador entra en colision con:
    o **Paredes** : se cambia la posición del jugador (x o y, dependiendo de
       por donde se realice) a la tile anterior a dicha colision para dar la
       impresión de “que choca”
    o **Warp** : se llaman a las funciones de borrado y generación de mapa
       y se transporta al jugador al inicio del siguiente piso
    o **Rope** : se llama a la función de borrado de mapa y se traslada el
       juego al estado runaway, donde todas las monedas se convierten
       en tiempo para la siguiente run
    o **Money** : se añade la cantidad de dinero del elemento colisionado
       al jugador
- Las entidades funcionan mediante estados y un if-then-else, aunque
    podría haberse implementado un patron estado mediante abstracción de
    comportamiento. Los estados permiten definir las animaciones que se
    muestran y el comportamiento de las hitboxes. Los enemigos solo tienen
    un estado por simpleza. Los estados son:
       o **Idle** : El jugador tiene vector de movimiento nulo. Es vulnerable.
       o **Run** : El jugador se mueve de acuerdo al vector de movimiento. Es
          vulnerable
       o **Dodge** : El jugador se mueve de acuerdo al vector de movimiento
          al inicio del dodge durante un determinado tiempo. Es
          invulnerable.

- Las armas del juego están almacenadas en la clase gun, desde la que se
    decide la posición en la esta mirando el arma a la hora de renderizarla. Las
    armas disparan balas, definidas en la clase bullet. Las balas salen con un
    vector de dirección determinado, un target definido (jugador o enemigo),
    desaparecen tras un tiempo y tienen diferentes acciones dependiendo de
    con lo que colisionen:
       o **Target** : El target de la bala siempre va a ser una entidad, ya sea
          jugador o enemigo, y van a triggerear la función de recibir daño.
       o **Wall** : La bala desaparece
- Las características de las armas están en el archivo data.py, desde el cual
    controlamos la duración de las balas, la cadencia de fuego y el daño que
    hacen. Igual que con los datos de enemigos y jugador mencionados
    anteriormente hubiera sido buena idea almacenar los sprites de las armas
    en esta clase también para mayor facilidad de cambios.
- A la hora de generar el nivel el FloorManager interactuará con la clase
    Floor, que esta llamará a las funciones de Map que interactuarán con las el
    mapa de tiles y el archivo de Rooms para generar el mapa. La generación
    procedural probablemente sea el apartado más destacado del juego.
- La arquitectura de datos/lógica hace muy sencillo añadir mas elementos al
    juego


### 2.3. ASSETS


- Musica:
o **Alarm** : Sonido de alarma del juego de acción/sigilo Payday 2
o **Defeat** : Sonido de derrota del juego de acción/estrategia
Warthunder
o **Victory** : “Fanfare” de victoria del juego de rol por turnos Final
Fantasy VII
o **Runaway** : Cancion de misión completada en el juego de
rol/estrategia Pokémon Mistery Dungeon DX
o **Gameplay** : Base con letra eliminada mediante Inteligencia
Artificial de la canción Punk, Sintes, Flamenco de El Coleta
- SFX:
o Obtenidos de páginas de efectos de sonido sin copyright y
editados con Audacity
- Sprites:
o Niveles: Paredes de colores dibujadas para el proyecto
o Cuerda: Objeto de cuerda huida de Pokémon
o Puertas: Dibujadas para el proyecto
o Dinero: Dibujado para el proyecto
o Jugador: Sprite de jugador con animaciones para el topdown
shooter Enter The Gungeon
o Arma: Escopeta de Enter The Gungeon
o Enemigos: Modificaciones de el Sprite del jugador con distintas
paletas de colores y diseños
**2.4. BUGS**
- Las volteretas pueden dar velocidad infinita al jugador si se mantiene la
barra espaciadora. La solución es simple, pero para la comunidad de
speedruns este bug puede ser de ayuda.


