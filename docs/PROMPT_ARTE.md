# Prompt para pedir mejoras de arte a otra IA

Copia lo de abajo tal cual y adjunta las 10 capturas de `docs/prompt-arte/`.
La primera parte describe el estado; la última dice qué quieres que te den.

Las capturas: 01 portada, 02 reparto, 03 hoja de expresiones, 04 victoria,
05 derrota, 06 la portada ya dentro del juego, 07 tablero, 08 mapa de
niveles, 09 pantalla de casa, 10 un combo. De la 06 a la 10 son capturas
reales del juego corriendo, no montajes.

---

## Contexto

Estoy haciendo **FrutiCity**, un match-3 para móvil en Unity 6, con la
ambición de parecerse a **Royal Match** en acabado y fluidez: pocas pantallas
pero muy pulidas, antes que muchos niveles. El juego ya funciona (tablero,
combos, especiales, mapa de niveles, reformas de la casa, historias por
episodios). Lo que quiero subir de nivel es el **arte y la dirección visual**.

**Formato:** móvil vertical. La UI se construye por código sobre un diseño de
referencia de **540 × 960**, escalado al área segura del dispositivo.

## Qué hay hecho (lo verás en las capturas)

**Reparto 3D.** Tres personajes modelados por script en Blender: **fresi**
(fresa), **pablo** (plátano) y **nora** (naranja). Comparten anatomía a
propósito para leer como familia:

- Cabeza de fruta sobre cuerpo humanoide chibi. La cabeza es el **42 %** de la
  altura total (1,60 en unidades de Blender) y es más ancha que los hombros.
- **La cara no es geometría: es un sprite** dibujado y pegado sobre un calco
  curvo que sigue la piel de la cabeza. Hay 6 expresiones (idle, alegre,
  guiño, sorpresa, triste, duda) y cambiar de humor es cambiar la imagen.
  Solo la nariz sigue teniendo volumen.
- Esqueleto de 16 huesos. Como el modelo son piezas sueltas, cada pieza cuelga
  de un hueso: no hay pesos ni deformación.
- Ropa: top y short (fresi), camiseta con manga y pantalón (pablo), vestido
  acampanado (nora), todas con escote y ribete.

**Portada.** Pantalla inicial 1080 × 1920 con los tres personajes, sunburst,
pétalos de sakura, nubes, rótulo con katakana y botón. El fondo se compone en
2D (Python + PIL); de Blender solo salen los personajes recortados con alfa.

**Pantallas de resultado.** Nivel superado y reintentar, con el personaje
animado: ganar es el salto con cara alegre, perder es un desinflado con cara
triste.

## Paleta actual

| Uso | Color |
|---|---|
| Fresa | `#D8392F` |
| Plátano | `#F5C63A` |
| Naranja | `#FF8A0F` |
| Hoja | `#8CBB5C` |
| Rosa (ropa fresi) | `#F5A2C0` |
| Azul (ropa pablo) | `#3FA9D6` |
| Turquesa (nora) | `#4FC2A6` |
| Cielo de portada | rosa `#FF96BE` → amarillo `#FFE082` → turquesa `#7AE2D6` |

## Lo que yo ya veo flojo

Dímelo sin piedad, pero estas son mis sospechas:

1. Los personajes tienen **manos y pies genéricos**, y las siluetas de perfil
   son pobres comparadas con Royal Match.
2. La ropa **no tiene arrugas ni pliegues**: son superficies lisas.
3. La portada tiene **mucho aire muerto** en la franja central.
4. Falta **identidad de marca**: el rótulo es una fuente de sistema (Arial
   Black) con contorno, no un logotipo dibujado.
5. Las expresiones son correctas pero **poco graciosas**; les falta chispa.
6. No hay **iluminación de escena** que cuente algo: es luz de estudio neutra.

## Qué te pido

1. **Crítica priorizada.** Los 5 problemas que más separan esto de un juego
   de primera línea, ordenados por *impacto visual por hora de trabajo*. Sé
   concreto: "la cabeza es un 8 % demasiado grande", no "mejora las
   proporciones".
2. **Dirección de arte en una página.** Qué debería ser FrutiCity
   visualmente para diferenciarse de Royal Match y de Candy Crush, sin dejar
   de ser legible en un tablero de móvil.
3. **Paleta corregida**, con hex. Si mis colores fallan (saturación, valor,
   contraste entre pieza y fondo), dame los que pondrías tú.
4. **Logotipo:** describe el logotipo que dibujarías (formas, remates,
   materiales, contorno) con detalle suficiente para encargarlo.
5. **Portada:** una composición alternativa. Descríbela como una rejilla
   (dónde va cada personaje, dónde el rótulo, dónde el botón, qué pesa más).
6. **Detalles de personaje** que más aportarían por poco coste: qué añadirías
   a manos, pies, ropa y pelo/hojas.

**Importante:** todo el arte se genera **por script** (Blender con Python para
los modelos, PIL para las composiciones 2D). No hay artista pintando a mano.
Así que prioriza cambios que se puedan expresar como **parámetros, perfiles y
reglas** — proporciones, curvas, paletas, número y colocación de elementos —
antes que texturas pintadas a mano.
