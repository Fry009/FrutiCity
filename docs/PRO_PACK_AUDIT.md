# Auditoría del Pro Pack v1

Fecha: 5 de septiembre de 2026. Fuente preservada: `Frutinovelas_Pro_Pack_v1/`, incluidos GDD, bucles, economía, JSON, dirección artística, arquitectura, backlog y master prompt.

## Lo que aporta el pack

| Área | Contenido recibido |
| --- | --- |
| Identidad | Seis personajes, personalidad, profesión y habilidades descritas |
| Merge | Tres cadenas, siete niveles cada una y tres generadores identificados |
| Match-3 | 50 fichas de nivel 8 × 8 con movimientos, objetivo, obstáculos y premio |
| Casa | Tres habitaciones, diez puntos decorables y tres variantes por punto |
| Historia | Diez títulos de episodio con tareas, niveles asociados y cierre genérico |
| Código | Siete scripts iniciales de datos, wallet y guardado; ningún juego conectado |
| Arte/audio | Manifiesto y prompts de producción; ningún sprite, animación o audio terminado |

## Contradicciones y decisiones

| Hallazgo | Resolución para FrutiCity |
| --- | --- |
| El pack dice Frutinovelas y `com.khamesoul.frutinovelas` | Prevalece la instrucción del propietario: FrutiCity, `com.khamesoul.fruticity`. Los IDs de contenido existentes se conservan. |
| Pide Unity LTS sin versión y la carpeta real usa 6000.6.0f1 | Se utiliza exactamente la versión instalada para evitar una migración innecesaria. |
| Objetivos de romper cajas/limpiar mermelada aparecen en niveles cuya lista de obstáculos no contiene ese elemento | La creación de niveles debe introducir suficientes objetivos reales y validar los tableros; el pack no describe sus coordenadas. |
| El onboarding necesita una estrella en el primer pedido y el JSON solo concede estrellas cada cinco niveles | La economía de encargos debe permitir la primera reforma sin esperar a cinco victorias. |
| Variantes de muebles sin ID, coste ni posición visual | Conservar ID de habitación + slot, y usar un índice de variante estable; no usar nombres traducidos como claves de guardado. |
| Diez episodios sin diálogo real ni asociación entre tarea y mueble | Se necesita contenido narrativo complementario y una regla de progresión explícita. Los títulos recibidos siguen siendo referencia. |
| Generadores sin probabilidades, cooldowns ni esquema de pedidos | El modelo de juego define valores iniciales revisables y pedidos realizables con las cadenas existentes. |
| Habilidades profesionales descritas solo en prosa | No dar por implementadas las seis pasivas por importar su descripción; cada efecto requiere comportamiento verificable. |
| Rendimiento «60 FPS» sin dispositivos de referencia | Es un objetivo; solo una medición en Android permite afirmarlo. |
| «Preparado para producción» junto a un backlog sin completar | Distinguir código jugable, contenido inicial, QA real, integración de servicios y publicación. |

## Dirección y experiencia

La referencia casual se traduce en botones amplios, jerarquía visual clara, piezas reconocibles por forma y color, respuesta inmediata, rebotes suaves y celebraciones cortas. Personajes, marca, composición y arte conservan identidad propia. La navegación une Casa, Taller, Jugar, Historia y Tienda sin exigir una cuenta.

Las recompensas y los encargos deben permitir sesiones breves. La monetización permanece opcional y desactivada durante la validación. Son necesarias pruebas con personas de distintas edades para evaluar comprensión, tamaño de lectura y ritmo; «todos los públicos» es una intención de diseño, no una clasificación de tienda emitida.

## Requisitos externos pendientes

- Firma Android de producción y alta de la app en Play Console.
- Configuración propia de Firebase/AdMob, consentimiento y declaración de datos cuando se activen SDKs.
- Dominio y datos reales de soporte para publicar páginas en Cloudflare.
- Balance mediante partidas humanas, pruebas táctiles en Android, accesibilidad y mediciones de rendimiento.
- Revisión final del contenido, capturas auténticas, icono, ficha y clasificación de edades.
