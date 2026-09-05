# GAME DESIGN DOCUMENT — FRUTINOVELAS

## 1. High concept
En un barrio habitado por frutas antropomórficas, cada personaje intenta progresar en su profesión y arreglar su vida mientras todo se convierte en una pequeña telenovela absurda.

El jugador ayuda a los personajes:
1. fabricando objetos mediante merge;
2. superando puzzles match-3;
3. cumpliendo encargos laborales;
4. consiguiendo Estrellas;
5. reformando una casa común;
6. desbloqueando episodios y nuevas profesiones.

## 2. Fantasía principal
"Estoy construyendo la vida de un grupo de frutas caóticas y cada pocos minutos pasa algo nuevo."

## 3. Pilares
### P1 — Progreso visible
El jugador debe notar mejoras en personajes, casa y tablero con mucha frecuencia.

### P2 — Personajes memorables
Las frutas no son skins: cada una tiene profesión, personalidad, habilidad y pequeñas relaciones.

### P3 — Tres loops conectados
Merge → trabajo → Estrellas/monedas → historia/decoración → match-3 → recursos → merge.

### P4 — Sesiones cortas
Una sesión útil puede durar 2–5 minutos. Una sesión larga puede encadenar varias actividades.

### P5 — Profundidad creciente
El inicio es muy simple. Las cadenas de merge, obstáculos, habilidades y objetivos se combinan progresivamente.

---

# 4. Público objetivo
- jugadores casuales;
- usuarios que disfrutan progresión, decoración y colección;
- sesiones rápidas en móvil;
- audiencia amplia, tono familiar y humorístico.

---

# 5. Core loop

## Loop de 30 segundos
- recoger generadores;
- fusionar;
- completar un pequeño objetivo;
- recibir feedback visual.

## Loop de 3–5 minutos
- completar pedido;
- jugar nivel match-3;
- obtener monedas/estrella;
- avanzar escena.

## Loop de sesión
- resolver varios pedidos;
- mejorar una habitación;
- desbloquear diálogo/capítulo;
- mejorar personaje/profesión.

## Meta-loop
- completar episodios;
- abrir nuevas profesiones;
- coleccionar muebles;
- mejorar la casa;
- desbloquear nuevas cadenas y eventos.

---

# 6. Sistemas

## 6.1 Merge
Tablero recomendado MVP: 7x9.

Tipos de elementos:
- generadores;
- objetos de merge;
- cajas;
- objetos bloqueados;
- recompensas;
- boosters.

Regla base:
2 objetos iguales → 1 objeto del siguiente nivel.

Generadores:
- consumen energía o tienen cooldown;
- generan objetos de nivel bajo;
- se pueden mejorar más adelante.

Pedidos:
- 3 tarjetas visibles;
- cada pedido pide 1–3 objetos;
- recompensas en Frutimonedas + XP profesión;
- algunos pedidos dan Estrellas.

## 6.2 Profesiones
Cada personaje principal tiene:
- profesión;
- nivel profesional;
- XP;
- habilidad pasiva;
- habilidad activa futura;
- cadena de objetos relacionada.

En MVP, tres profesiones tienen cadena merge completa:
- Chef;
- Reparto;
- Influencer.

Las otras tres aparecen en historia y desbloquean sistemas futuros.

## 6.3 Match-3 — "FrutiCombo"
Tablero típico: 8x8.

Piezas:
- Manzana;
- Plátano;
- Fresa;
- Naranja;
- Uva;
- Kiwi.

Combinaciones:
- 3: match normal;
- 4 en línea: cohete;
- 5 en línea: FrutiArcoíris;
- T/L: bomba;
- cascadas: multiplicador temporal.

Objetivos MVP:
- alcanzar puntuación;
- recoger frutas;
- romper cajas;
- limpiar mermelada;
- liberar piezas;
- combinar objetivos.

## 6.4 Estrellas
Las Estrellas representan progreso narrativo.

Se gastan en:
- reparar;
- decorar;
- iniciar escenas;
- subir hitos de episodio.

No deben venderse directamente en MVP.

## 6.5 Frutimonedas
Moneda blanda.

Fuentes:
- pedidos;
- niveles;
- logros;
- recompensas diarias.

Usos:
- muebles;
- pequeñas mejoras;
- reroll de pedido;
- boosters básicos.

## 6.6 Gemas
Moneda premium futura.

Usos:
- cosméticos especiales;
- packs;
- acelerar cooldown opcionalmente;
- continuar un nivel.

En el prototipo pueden estar desactivadas.

## 6.7 Energía
Separar energía de Merge y corazones de Match-3 solo si los tests justifican la complejidad.

MVP recomendado:
- un único recurso "Energía";
- máximo 50;
- regeneración suave;
- eventos y vídeos recompensados opcionales.

## 6.8 Decoración
Tres habitaciones:
1. Salón.
2. Cocina.
3. Dormitorio/estudio.

Cada punto decorable:
- 3 variantes;
- una elección activa;
- posibilidad de cambiar después.

## 6.9 Narrativa
Episodios de 5–10 minutos de contenido distribuido.

Escenas:
- 2–5 líneas;
- entrada rápida;
- gag;
- objetivo;
- pequeña resolución/cliffhanger.

Evitar bloques largos de texto.

---

# 7. Diferenciador: habilidades profesionales
Cada fruta altera ligeramente el gameplay.

### Mona Manzana — Chef
"Toque Gourmet"
Pequeña probabilidad de duplicar un objeto de cocina al completar un pedido.

### Pablo Plátano — Repartidor
"Entrega Exprés"
Reduce ligeramente el cooldown de generadores de reparto.

### Fresi Fresa — Influencer
"Viral"
Los combos largos de match-3 dan bonus de Frutimonedas.

### Nora Naranja — Médica
"Vitaminas"
Una vez por sesión puede devolver una pequeña cantidad de energía.

### Pina Piña — DJ
"Subidón"
Al iniciar ciertos niveles, crea una pieza especial aleatoria.

### Sandi Sandía — Albañil
"Martillazo"
Puede romper gratuitamente un obstáculo débil en ciertos niveles.

---

# 8. MVP

## Contenido
- 6 personajes.
- 3 cadenas merge de 7 niveles.
- 50 niveles match-3.
- 10 episodios.
- 3 habitaciones.
- 30 variantes de muebles.
- 4 boosters.
- 5 tipos de obstáculos.
- 1 calendario de recompensa diaria de 7 días.

## Fuera de MVP
- PvP.
- gremios;
- chat;
- multijugador;
- mundo abierto;
- más de una casa;
- eventos competitivos;
- backend complejo.

---

# 9. UX
Navegación inferior recomendada:
- Casa;
- Merge;
- Jugar;
- Historia;
- Tienda.

Home:
- personaje destacado;
- misión actual;
- botón grande de acción;
- recursos en top bar;
- acceso rápido a recompensa diaria.

---

# 10. Métricas de diseño
Medir desde soft launch:
- D1 / D7 retention;
- nivel donde abandona el jugador;
- ratio de victoria por nivel;
- duración de sesión;
- pedidos completados;
- tiempo hasta primera decoración;
- uso de habilidades;
- ads voluntarios;
- conversión IAP si se activa.

---

# 11. Principios de monetización
- evitar paywall temprano;
- anuncios solo recompensados durante MVP;
- no interrumpir diálogos;
- no vender poder excesivo;
- priorizar cosméticos, conveniencia y bundles claros.

---

# 12. Roadmap futuro
### V1.1
- profesión médica;
- habitación extra;
- eventos semanales.

### V1.2
- DJ y albañil como cadenas merge;
- colección de outfits;
- tablero especial de fin de semana.

### V1.3
- episodios estacionales;
- minijuegos sociales;
- cloud save.
