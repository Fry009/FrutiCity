# Reforma y puzle — 6 septiembre 2026

## Dirección aceptada

El tablero usa frutas cartoon **sin ojos ni boca**. Los personajes expresivos se reservan para portada, vecinos e historia. El recorrido sustituye las fusiones: puzle → estrella → mejora visible → episodio. Se ha retirado la pantalla de fusiones y la antigua lista de compra de muebles; los datos y servicios antiguos se conservan para compatibilidad de partidas.

## Implementación

- Cocina, salón y dormitorio originales modelados en Blender, cuatro estados visuales por habitación. Los diez episodios reutilizan estas tres escenas; no son diez escenarios únicos.
- Las tareas existentes consumen estrellas una sola vez. Ya no exigen comprar muebles aparte ni superar un nivel adicional después de pagar. Las estrellas de las antiguas compras de muebles se devuelven una vez al migrar.
- La última mejora entrega una sola vez el premio existente de 100 monedas y 5 de energía. Se puede volver a visitar un episodio terminado. La progresión y la escena se reconstruyen desde el guardado.
- Reposo, salto al tocar personajes, hinchado, explosión y rebote en las piezas; gotas del color de la fruta eliminada. Las hélices despegan y dejan estela hasta su objetivo, la dinamita carga y sacude antes de explotar, las bolas multicolor giran al cargar y las cajas sueltan astillas según reciben daño. Movimiento reducido desactiva partículas y reacciones intensas.
- Modelos propios para dinamita, hélice y bola multicolor. Cohetes orientados por dirección. Los renders de modelos 3D se animan como sprites en el Canvas: no son personajes 3D con esqueleto renderizados en tiempo real.
- Dinamita con radio dos; doble dinamita radio cuatro; hélice despeja vecinos y un objetivo; doble hélice tres objetivos; hélice con especial transporta uno; bola con especial convierte el color más frecuente. Creación y activación tienen eventos visuales distintos.

## Investigación y límites

Fuentes oficiales consultadas:

- [Creación de especiales](https://dreamgames.helpshift.com/hc/en/3-royal-match/faq/6-creating-and-using-the-power-ups/).
- [Combinaciones](https://dreamgames.helpshift.com/hc/en/3-royal-match/faq/7-power-up-combinations/).
- [Tareas y áreas](https://dreamgames.helpshift.com/hc/en/3-royal-match/faq/15-what-are-tasks-and-how-do-i-complete-them/).

El archivo `Assets/royal/uptodown-com.dreamgames.royalmatch.apk` mide 15.554.334 bytes y contiene 2.165 entradas. Su manifiesto identifica `com.uptodown` y `com.uptodown.UptodownApp`; contiene bibliotecas de Uptodown. Es la aplicación de descarga, no una copia analizable del motor de Royal Match. Inventario en `artifacts/royal-apk-inventory.json`. No se han extraído recursos del juego para utilizarlos.

El vídeo aportado (`HictLcfbvDU`) no estuvo disponible ni mediante web ni mediante yt-dlp. No se afirma haber visto sus fotogramas. El contraste de reglas procede de la documentación oficial.

## Reproducción y QA

`art/blender/reforma.py` genera las tres habitaciones y sus estados; `especiales_v2.py`, los especiales. Los originales `.blend` quedan junto a sus PNG en esas carpetas.

`-fruticityCapture <carpeta>` toma capturas reales. `-fruticityDemo` ejecuta jugadas con el motor real y muestra las tres mejoras de cocina. Ambos usan una partida nueva y una carpeta VisualQA separada. La demostración asigna tres estrellas a esa partida de prueba para enseñar las mejoras, sin tocar la partida del usuario.

Pruebas iniciales de esta refactorización: 84/84 correctas. Compilación Windows: 0 errores, 3 avisos previos de API obsoleta. Las comprobaciones visuales y los archivos finales se registran en el handoff.
