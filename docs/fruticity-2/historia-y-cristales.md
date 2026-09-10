# Auditoría de la historia, y el plan de los cristales

10 de septiembre de 2026. Escrito para continuar sin releer nada.

---

## 1. Auditoría: ¿están relacionadas las viñetas y la historia?

**Sí, y bastante mejor de lo que parecía.** No hay incoherencia entre el contenido y las viñetas. Lo que hay es un desajuste **entre el contenido y lo que Fran cree que cuenta**.

### Lo que hay escrito

`EPISODES.json` tiene 10 episodios × 5 niveles = **50**, cada uno con 3 tareas (30 en total) y un **gancho** que enlaza con el siguiente. El arco está cerrado de principio a fin:

| Ep | Título | Gancho hacia el siguiente |
| --- | --- | --- |
| 1 | La cocina del desastre | Llega un paquete para alguien que aún no vive aquí |
| 2 | El paquete imposible | Fresi anuncia que retransmitirá la receta en directo |
| 3 | Fama con sabor a fresa | Piden un postre que sepa a casa para todo el barrio |
| 4 | Una receta viral | Bajo la alfombra, una tabla suelta y una llave de latón |
| 5 | La casa cruje | Pina propone recuperar la fiesta |
| 6 | Fiesta sin permiso | Nora ve muchos planes y ningún rato libre |
| 7 | El diagnóstico del barrio | El pedido de inauguración llega antes de tiempo |
| 8 | Entrega a contrarreloj | La última caja trae invitaciones de todo el barrio |
| 9 | El gran servicio | Todo listo; al otro lado de la puerta espera FrutiCity |
| 10 | La inauguración | Fin de temporada |

Las **viñetas** (`ComicLines` en `EpisodeJourney.cs`, 10 capítulos × 2 paneles) **siguen esos ganchos uno a uno**. Comprobado: la viñeta 1 termina con Pablo y el paquete, y el episodio 2 se llama «El paquete imposible». La viñeta 2 termina con Fresi y su aro de luz, y el episodio 3 es «Fama con sabor a fresa». La secuencia está bien cosida.

### El desajuste de verdad

Fran describe los 50 niveles como **«la historia de reformar la casita de fresa»**. El contenido escrito es otra cosa: la protagonista es **Mona Manzana**, chef, y el arco va de su cocina destrozada a la inauguración del local con todo el barrio. **Fresi (la fresa) es secundaria**: aparece como la que retransmite en directo, en los episodios 2–3.

Además, las tres habitaciones de la reforma (`room_0`, `room_1`, `room_2`) son **cocina, salón y dormitorio**, y se repiten cada tres episodios.

### Por qué esto importa antes de tocar nada

Las **diez ilustraciones del camino** (`Resources/Art/Journey/episode_01..10`) están dibujadas **sobre esta historia**: el episodio 1 es literalmente una cocina con mermelada por las paredes y una manzana con gorro de chef. Reescribir el arco para que la protagonista sea Fresi **deja huérfanas las diez ilustraciones**, que son el asset más caro y más bonito que tiene el juego.

### Las tres salidas

1. **Dejar la historia como está y corregir la idea**: la protagonista es Mona, y lo que se reforma es *su casa y su cocina*, con Fresi como amiga influencer. Coste cero. La historia ya es coherente.
2. **Reencuadrar sin redibujar**: la casa es **compartida** —Mona cocina, Fresi graba, Pablo reparte— y los 50 niveles son «montar nuestra casa». Se tocan textos, no ilustraciones. Coste bajo, y encaja con que la reforma tenga cocina, salón y dormitorio.
3. **Reescribir para Fresi**: hay que regenerar las diez ilustraciones del camino y las veinte viñetas. Coste alto.

**Recomendación: la 2.** Conserva el arte, arregla la incoherencia que a Fran le chirría y explica por qué la reforma tiene tres habitaciones distintas.

---

## 2. Los cristales morados: el problema de las cuentas

La idea es buena. Tal y como está descrita, **no se puede jugar**.

> «cuando completamos un nivel nos dan un cristal, entonces por ejemplo el nivel 2 requiere 2 cristales»

Si cada nivel da **1** cristal (una sola vez) y el nivel N pide **N**:

| Antes del nivel | Cristales que tienes | Cristales que pide | |
| --- | --- | --- | --- |
| 1 | 0 | 1 | bloqueado de salida |
| 2 | 1 | 2 | **bloqueado** |
| 3 | 2 | 3 | bloqueado |

Siempre te falta exactamente uno. Y si además se **gastan**, es peor: tras pagar el nivel 2 te quedas a cero.

La causa es aritmética, no de implementación: al completar los niveles 1..N−1 tienes N−1 cristales, y el nivel N pide N. **Nunca llegas.**

### Lo que sí funciona, y creo que es lo que quieres

Fran dijo también *«en algunos puntos del mapa requerirá gastar cristales»*. Eso es lo que sale bien:

- **Cada nivel completado da 1 cristal**, una sola vez. Rejugar no da más.
- **Los niveles normales no cuestan cristales.** Se siguen desbloqueando en orden.
- **Al final de cada capítulo hay una puerta** que cuesta **3 cristales** para abrir el barrio siguiente.

Por capítulo ganas 5 y gastas 3, así que **acumulas 2**. Eso hace tres cosas a la vez: nunca te bloqueas, el cristal *significa* algo porque se gasta, y quien rejuegue niveles antiguos no gana nada (ya los cobró), así que no hay granja.

Y deja sitio para venderlos en la tienda más adelante sin romper nada, porque el suelo está garantizado por el propio juego.

### Alternativa si quieres más tensión

Puerta de **4** cristales por capítulo: ganas 5, gastas 4, acumulas 1. Aprieta, pero sigue sin bloquear. **Cinco no**: con 5 vas justo y un solo nivel fallado te deja fuera.

---

## 2 bis. Decidido por Fran

**Puertas de 3 cristales.** Ganas 5 por capítulo, gastas 3, acumulas 2.

**Niveles de bonus.** Idea de Fran, y encaja perfecto con el margen anterior: un nivel de bonus da **un cristal extra**, así que sirve para desatascar a quien haya rejugado poco o quiera adelantarse. Modo propuesto por él: **supervivencia** sobre el mismo motor de puzle —sin límite de movimientos, aguantar lo máximo— que es exactamente lo que pide el plan (§13): romper la monotonía **sin construir un minijuego nuevo**.

Dónde ponerlos: uno por capítulo, colgando del camino y no dentro de la fila de niveles, para que se lea como un desvío opcional. El primero, no antes del capítulo 2: el jugador tiene que entender el cristal antes de que le ofrezcan una forma alternativa de conseguirlo.

**Ojo con una cosa**: si el bonus se puede rejugar y dar cristal cada vez, es una granja infinita y las puertas dejan de significar nada. Tiene que dar cristal **una sola vez**, igual que los niveles normales, o dar cristal sólo la primera vez y monedas las siguientes.

## 2 ter. Los números finales, y el fallo que casi se cuela

Fran fijó: **1 estrella = 1 cristal, 3 estrellas = 2**, más el nivel de bonus, que es el **antepenúltimo de cada bloque de cinco**. Las 2 estrellas no las fijó; aquí pagan 1, para que el salto que se note sea llegar a las **tres**.

**El bonus es uno de los cinco niveles, no un extra.** Eso cambia las cuentas respecto a lo escrito más arriba: cada capítulo tiene cinco niveles que pagan cristal, no cuatro.

Como las 2 estrellas también pagan 1, **el suelo de la temporada es exactamente 50**: es lo que tiene quien se pasa los cincuenta niveles sin sacar tres estrellas ni una sola vez.

| | Cristales |
| --- | --- |
| Suelo (nunca 3★) | **50** |
| Normal (~15 niveles a 3★) | 65 |
| Techo (todo a 3★) | 100 |

### El fallo

Un primer reparto de puertas subía de 5 a 9 y sumaba **71**. Con un suelo de 50, eso deja **encerrado para siempre** a quien juegue toda la temporada sin sacar tres estrellas — el peor resultado posible, porque le pasa al jugador que más ha jugado.

Lo cazó la prueba `TheWholeSeasonIsFinishable`, que existe justo para eso y se queda como red permanente: si alguien sube las puertas en el futuro, salta.

### Lo que sí cierra

**Puertas: 4, 4, 4, 4, 5, 5, 5, 5, 5 → 41 cristales.** Margen en el peor caso: **+9**.

Y cada puerta sigue significando algo: con **4** hay que completar al menos cuatro de los cinco niveles del capítulo; con **5**, el capítulo entero. Ninguna puede costar más de 5, o encerraría al jugador del suelo.

### Cómo se guarda

El saldo **no se guarda: se calcula**.

```
saldo = ganados(mejores estrellas de cada nivel) − gastados(puertas abiertas)
```

Lo ganado sale de `levelRecords`, que ya guarda la mejor marca de cada nivel. Eso resuelve solo los dos problemas de este tipo de moneda: **no hay granja** (rejugar no cambia tu mejor marca) y **no hay bloqueo** (mejorar estrellas sube el total automáticamente). En el guardado entra **un solo entero**: `gatesOpened`.

Guardar un contador aparte habría exigido además una lista de «niveles ya pagados», y esa lista es justo la que se desincroniza y acaba regalando o robando cristales.

### Las estrellas pagan dos veces, y es a propósito

Las que se **gastan** en la reforma (`state.stars`, una por nivel la primera vez) y las que quedan **registradas por nivel** (`levelRecords[].stars`, la mejor marca) son cosas distintas y no interfieren. Sacar 3★ da una estrella gastable para la casa **y** dos cristales para la puerta: la misma buena partida paga las dos cosas.

## 2 quater. NÚMEROS DEFINITIVOS (sustituyen a los de arriba)

Fran fijó **6 cristales por puerta**, las nueve iguales. Sale, **pero sólo si el nivel de bonus paga 2 como mínimo**:

| | Cristales |
| --- | --- |
| 9 puertas × 6 | **54** |
| Suelo por capítulo si el bonus paga 1 | 5 → **bloqueado en la primera puerta** |
| Suelo por capítulo con el bonus pagando 2 | 4×1 + 2 = **6** |
| Suelo de la temporada | 10 × 6 = **60** |
| Margen en el peor caso | **+6** |

Por eso `ForBonus` tiene un mínimo de 2. **No es un capricho de balance: es lo único que hace que una puerta de 6 no encierre a nadie.** Está escrito junto a `GateCost` para que nadie lo baje sin ver la consecuencia.

El bonus es el **antepenúltimo de cada bloque de cinco** (índices 2, 7, 12…), como pidió Fran. Cae bien además porque deja dos niveles normales después para volver al ritmo antes de la puerta.

**Pagos:** 1★ = 1 · 2★ = 1 · 3★ = 2 · bonus = 2, y 3 si se borda.

## 2 quinquies. El arte del cristal: hecho

`art/blender/modelo_cristal.py`, registrado en `exportar.py` como grupo `RECURSOS`. En `Resources/Art/res_cristal.png`.

```powershell
blender --background --python art/blender/exportar.py -- cristal
```

Seis caras y **sombreado plano**: en cuanto se suaviza, las facetas desaparecen y queda una zanahoria morada. Punta de arriba más larga que la de abajo y el conjunto algo ladeado, porque un cristal perfectamente simétrico se lee como un icono y no como un mineral.

**Trampa pagada**: en la primera versión el alma interior estaba modelada **y no se veía un solo píxel de ella**, porque el cuerpo era opaco — geometría muerta que se renderiza para nada. El cuerpo pasa a translúcido por Fresnel (centro 0,72) y ahora se le ve el fondo, que es lo que hace que una gema parezca cara. Mismo truco que el hielo, y **la misma trampa**: `Facing` vale 0 mirando de frente y 1 en el canto, no al revés.

## 2 sexies. El HUD de cuatro píldoras: hecho

La fila pasó de tres a cuatro, y **no fue meter una más**. Las tres viejas medían 163, 143 y 176 px y ocupaban de 18 a 522 de los 540: no cabía nada. Se rehizo entera.

- Píldoras de **126 px**: 4×126 + 3×6 de hueco = 522, con 9 de margen a cada lado.
- Icono de 64 a **52 px**, número de cuerpo 23 a **20**.
- Cifras acortadas por encima de diez mil: `12,3K` en vez de `12.400`. Por debajo se escribe entero, porque ahí cada moneda cuenta.

Lo que **no** se tocó: el icono asomando por fuera del borde. Es lo que le da el aire de juego; meterlo dentro convierte la fila en una tabla de datos.

**Trampa pagada:** los contadores no pueden ajustar línea. `UiKit.Label` lo hace por defecto, y con las píldoras estrechas «50 / 50» salió **partido en dos líneas**, medio fuera de la píldora. Ahora desbordan en horizontal —si un número no cabe, que asome— y el texto de rayos es `50/50` sin espacios.

**El `+` sólo en monedas y rayos.** Estrellas y cristales se ganan jugando; ponerles un `+` sería prometer un atajo que no existe.

## 3. Lo que habría que construir

En orden, y ninguno depende de cuentas ni credenciales:

1. ~~Reglas y guardado~~ **HECHO**: `CrystalRules` + `GameState.gatesOpened`, 12 pruebas.
2. ~~El arte del cristal~~ **HECHO**: `res_cristal.png`.
3. **La barra pasa a CUATRO píldoras**: monedas, estrellas, cristales y rayos. Las tres de ahora ocupan de 18 a 522 de los 540 disponibles, así que **la cuarta no cabe con el formato actual**: hay que rediseñar la fila entera, no encajarla a martillazos. Es el siguiente paso y el más delicado.
4. **La puerta de capítulo en el mapa**, con su coste visible y qué pasa al abrirla.
5. **El modo bonus**: 2 minutos, muchas combinaciones cayendo, progresivo, a máxima puntuación. Sobre el mismo motor de puzle.
6. **La tienda**, con el cristal como concepto nuevo.
7. **Efectos y sonido**: los hereda gratis. La animación de gasto está enganchada al contador, no a cada botón.

Las estrellas también tienen que aparecer en el HUD **como recompensa** al ganarlas, no sólo como contador.

---

## 3 bis. La historia: el fallo encontrado y arreglado

Fran lo describió así: «si termino un episodio, el siguiente parece que no tiene que ver».

**Tenía razón, y la causa era concreta.** El campo `cliffhanger` está escrito en los diez episodios de `EPISODES.json` desde el principio, se declara en `GameContent.cs`… y **no se lee en ningún sitio**. Nadie lo usaba. La costura entre capítulos existía en los datos y el jugador **no la veía jamás**.

Arreglado: la frutinovela pasa de dos viñetas a **tres momentos**. Tras las dos viñetas viene «En el próximo episodio…», con el gancho y el título del capítulo que viene.

Va al final y no al principio a propósito: un capítulo que se cierra del todo se lee como un final, y uno que se cierra con una pregunta abierta es el que hace querer jugar el siguiente. Y **no se enseña la ilustración del capítulo siguiente**, que destriparía justo lo que se está prometiendo.

El último episodio no tiene gancho: cierra la temporada.

## 4. Estado al escribir esto

- **140/140 pruebas EditMode**, con las once nuevas de compras.
- Compras reescritas: el contenido lo concede `EntitlementService`, idempotente por transacción y con memoria en el guardado. Antes `Iap.Purchase` devolvía un `bool` y **cada reintento de la tienda regalaba el pack otra vez**.
- Precios en euros escritos a mano, fuera. Los pone la tienda del país de quien mira.
- Monedas y rayos: animación de gasto y **sonido propio de cada uno**. Los rayos ya no suenan a moneda.
