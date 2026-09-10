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

## 3. Lo que habría que construir

En orden, y ninguno depende de cuentas ni credenciales:

1. **`GameState.crystals`** y el registro de qué niveles ya lo pagaron (para que rejugar no dé más). Mismo patrón que `seenMechanics`: lista de texto, sin subir `SaveVersion`.
2. **La píldora en la barra**, junto a monedas, estrellas y rayos. Ya son tres y una cuarta aprieta: hay que rediseñar la fila, no encajarla a martillazos.
3. **El arte del cristal**, en Blender, mismo estudio que las trece piezas (`comun.py`) — si no, se ve el pegote junto a la moneda y el rayo. Morado, facetado, con brillo interior.
4. **Efectos y sonido propios**, como los que ya tienen monedas y rayos. La animación de gasto ya es genérica: engancha al contador, así que el cristal la hereda sin tocar nada.
5. **La puerta de capítulo en el mapa**, con su coste visible y qué pasa al abrirla.
6. **La tienda**, con el cristal como concepto nuevo.
7. **Tests**: que rejugar no dé cristal, que la puerta no se abra sin pagar, y que el saldo nunca pueda bloquear la partida.

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
