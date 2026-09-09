# Prompt para la mega IA (evaluación completa de FrutiCity)

**Cómo usarlo:** copia todo lo que hay debajo de la línea y adjunta las 18 imágenes
de `docs/prompt-mega/`, en orden y con su nombre de archivo. Los nombres importan:
el prompt las cita por número.

Si la IA solo admite pocas imágenes, el mínimo útil es: 02, 06, 07, 08, 10, 11, 17.

---

# FrutiCity — evaluación de dirección visual y de producto

Eres director de arte y director creativo de juegos casuales móviles. Has trabajado
en el nivel de Royal Match, Gardenscapes y Toon Blast. Te paso un juego real, en
marcha, con capturas de verdad tomadas del ejecutable. Quiero tu juicio **sin
piedad** y, sobre todo, **accionable**.

## 1. Qué es

**FrutiCity**: match-3 para móvil hecho en Unity 6. La ambición declarada es
parecerse a **Royal Match, pero con frutas**: pocas pantallas y muy pulidas antes
que muchos niveles. El bucle es el clásico del género:

1. **Match-3** en tablero 8×8, con especiales y combos completos: 4 en línea →
   cohete, 5 → arcoíris, L/T → bomba, cuadrado 2×2 → hélice. Todas las parejas de
   especiales están resueltas y cada combo tiene nombre y puesta en escena propia.
2. Ganar niveles da **estrellas**, monedas y "rayos" (energía).
3. Las estrellas se gastan en **reformar la casa** habitación por habitación.
4. Cada reforma **avanza una historia** por episodios con los vecinos del barrio.

## 2. Estado técnico real (no es un prototipo)

| Dato | Valor |
|---|---|
| Motor | Unity 6 (6000.6), UGUI |
| Diseño de referencia | **540 × 960 vertical**, escalado al área segura |
| Toda la UI | **construida por código**, sin prefabs ni escenas dibujadas a mano |
| Código | 48 scripts C#, ~8.600 líneas |
| Pruebas | 84 EditMode en verde |
| Compilación | Windows y Android APK correctas |
| Contenido | 50 niveles, 10 episodios, 12 personajes, 24 cadenas de fusión |
| Tipografía | Nunito (Heavy para títulos) |
| Música | tres temas clásicos de dominio público **sintetizados en tiempo real** |

## 3. Cómo se produce el arte (esto condiciona tu respuesta)

**No hay ningún artista pintando.** Todo el arte se genera **por script**:

- **Personajes y piezas**: modelados en **Blender con Python**, render a PNG con
  alfa. Trece piezas de tablero y tres personajes principales (fresi/fresa,
  pablo/plátano, nora/naranja) salen así.
- **Composiciones 2D** (portada, fondos, rótulos): **Python + PIL**.
- **Caras de personaje**: no son geometría, son un **sprite plano pegado sobre un
  calco curvo** que sigue la piel de la cabeza. Cambiar de humor es cambiar la
  imagen. Hay 6 expresiones.
- Las piezas del tablero se **hornean a una sola vista** en PNG de 128 px; todo el
  movimiento es transformación 2D a 60 fps. No hay rotación 3D en vivo.

**Por lo tanto**: prioriza cambios que se puedan expresar como **parámetros,
proporciones, curvas, paletas, reglas de composición y número/colocación de
elementos**. Una recomendación del tipo "que un ilustrador pinte texturas" no me
sirve. Una del tipo "sube el radio de esquina a 18 px, baja el valor del marco un
12 % y mete un degradado vertical de dos paradas" sí.

## 4. Las capturas

Las 01–05 son arte de producción (renders). **Las 06–18 son capturas reales del
juego corriendo**, sin retocar.

| # | Archivo | Qué es |
|---|---|---|
| 01 | `01-arte-portada-render.png` | Portada a 1080×1920, tal como sale del pipeline |
| 02 | `02-arte-reparto-3d.png` | Los tres personajes principales, hoja de reparto |
| 03 | `03-arte-expresiones.png` | Las 6 expresiones faciales |
| 04 | `04-arte-victoria.png` | Pantalla de nivel superado |
| 05 | `05-arte-derrota.png` | Pantalla de reintentar |
| 06 | `06-juego-portada.png` | La portada **ya dentro del juego** |
| 07 | `07-juego-casa.png` | Pantalla principal / barrio |
| 08 | `08-juego-mapa.png` | Mapa de niveles del episodio |
| 09 | `09-juego-ficha-nivel.png` | Ficha previa al nivel, con receta de combo |
| 10 | `10-juego-tablero.png` | **El tablero de juego. La pantalla que más se mira** |
| 11 | `11-combo-cohetes.png` | Combo cohete + cohete en marcha |
| 12 | `12-combo-arcoiris.png` | Combo arcoíris en marcha |
| 13 | `13-combo-bombas.png` | Combo bomba + bomba en marcha |
| 14 | `14-juego-reforma.png` | Habitación a reformar |
| 15 | `15-juego-decoracion.png` | Decoración de la casa |
| 16 | `16-juego-historia.png` | Diálogo de historia |
| 17 | `17-juego-vecinos.png` | Ficha de personaje |
| 18 | `18-juego-tienda.png` | Tienda |

## 5. Paleta actual

| Uso | Hex |
|---|---|
| Fresa | `#D8392F` |
| Plátano | `#F5C63A` |
| Naranja | `#FF8A0F` |
| Hoja | `#8CBB5C` |
| Rosa (ropa fresi) | `#F5A2C0` |
| Azul (ropa pablo) | `#3FA9D6` |
| Turquesa (nora) | `#4FC2A6` |
| Cielo de portada | rosa `#FF96BE` → amarillo `#FFE082` → turquesa `#7AE2D6` |

## 6. Lo que yo ya sospecho que está mal

No te limites a esto, y contradíceme si me equivoco. Pero para que no gastes
tiempo descubriendo lo obvio:

1. **Conviven tres estilos que no casan.** El reparto chibi 3D de la portada (06),
   unos personajes "adultos" de cara plana en casa/vecinos/historia (07, 16, 17), y
   una ilustración pintada a mano en el mapa (08). Parecen tres juegos distintos.
2. **La portada dentro del juego no cubre la pantalla** (06): queda una banda
   vacía a la derecha.
3. **Fondos muertos.** Tablero, vecinos, historia y tienda son un degradado
   azul-verde liso sin nada. Royal Match siempre tiene escena detrás.
4. **El tablero está apagado** (10): marco marrón + casillas beige. Las frutas
   compiten con un fondo que no las ayuda a destacar.
5. **No hay logotipo.** "FrutiCity" es una fuente de sistema con contorno, no una
   marca dibujada.
6. **La barra de navegación de 5 iconos sigue visible dentro del nivel** (10).
   Royal Match la esconde al jugar.
7. **El rótulo de combo tapa el tablero** (11): ocupa todo el ancho justo encima
   de la acción.
8. **El HUD no tiene jerarquía** (10): tres píldoras oscuras del mismo peso.
9. **La tienda no vende** (18): es una lista de fichas planas, sin brillo ni valor
   percibido.
10. **La habitación de reforma es una caja vacía** (14).

## 7. Qué te pido exactamente

Responde en este orden y con estos títulos:

### A. Veredicto en una línea
¿Qué le falta a esto para pasar de "juego indie decente" a "juego de tienda"?
Y ponle nota del 1 al 10 comparándolo con Royal Match en: acabado visual,
legibilidad del tablero, identidad de marca y sensación de juego.

### B. Los 5 arreglos de mayor impacto por hora de trabajo
Ordenados. Para cada uno: **qué está mal**, **qué captura lo demuestra**, **qué
hacer en términos de parámetros concretos** (números, hex, proporciones, píxeles)
y **cuánto tiempo estimas**. Sé quirúrgico: "la cabeza es un 8 % grande de más",
no "revisa las proporciones".

### C. Unificar el estilo
Con tres estilos coexistiendo, ¿cuál me quedo y cómo reconvierto los otros dos con
un pipeline por script? Dame la regla que hace que todo se vea de la misma familia
(silueta, contorno, número de tonos, brillo especular, sombra de contacto...).

### D. El tablero, rediseñado
Es la pantalla que más se mira. Descríbeme el rediseño como **especificación
implementable**: colores del marco y las casillas con hex, grosores, sombras,
tamaño de pieza respecto a la casilla, cuánto contraste debe haber entre pieza y
fondo, qué desaparece de la pantalla mientras se juega y qué se queda.

### E. Dirección de arte en una página
Qué debería ser FrutiCity visualmente para no ser ni un clon de Royal Match ni uno
de Candy Crush, sin dejar de leerse en un móvil pequeño.

### F. Paleta corregida
Con hex. Si mis colores fallan en saturación, valor o contraste pieza/fondo, dame
los tuyos y di por qué. Incluye la regla de contraste que debo cumplir siempre.

### G. Logotipo
Descríbeme el logotipo que dibujarías —formas, remates, materiales, contorno,
profundidad— con detalle suficiente para reproducirlo por script en PIL o Blender.

### H. Efectos y sensación
Mira 11, 12 y 13. ¿Los combos se leen? ¿Qué sobra, qué falta, qué tapa el juego?
Dime cómo se debería coreografiar un combo grande: qué pasa en cada décima de
segundo, dónde va el rótulo, cuánto dura, cuándo entra la sacudida.

### I. Plan por fases
Divide todo lo anterior en tres tandas: **una tarde**, **una semana**, **un mes**.
Que cada tanda deje el juego mejor que antes por sí sola.

**Regla final:** nada de generalidades. Si algo no se puede expresar como un
número, una forma o una regla, no lo digas.
