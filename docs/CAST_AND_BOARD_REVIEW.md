# Revisión del reparto y el puzzle · 8 de septiembre de 2026

La primera propuesta de personajes (`reparto_v3`) fue rechazada por su aspecto de muñeco. La revisión `art/blender/reparto_v4.py` exporta seis modelos articulados con ojos almendrados, sonrisas, vestuario y cabezas independientes. Los originales editables están en `art/blender/reparto_v4/`; los FBX y retratos que consume Unity están en `Resources/FrutiCast`.

`art/cast-frutinovelas-reference.png` es una referencia artística generada, no una captura del juego ni un modelo 3D. Los modelos actuales son más sencillos que esa referencia. Se mantiene la composición de la portada y las piezas originales del puzzle.

`CastActor` anima reposo, parpadeo, cabeza, celebración, risa y derrota con recuperación. `CastPortrait` renderiza cada actor en una cámara aislada y libera la cámara y su RenderTexture al salir. La ficha de personajes permite probar «Celebrar» y «Un mal día». El shader dibuja ambas caras de las superficies finas de ojos, boca y hojas.

## Corrección del tablero

La máscara añadida a la capa de piezas usaba padding fijo: en el lienzo escalado recortaba las filas superiores e inferiores. Se retiró. La entrada de piezas nuevas sigue controlada por la animación de cada columna. Verificación visual en `artifacts/board-fixed.png`.

La mermelada tiene contorno orgánico y conserva conexiones entre casillas. El hielo usa cristal azul translúcido y destellos al romperse. Se mantienen las frutas del tablero, las caídas precisas, la pista de dos piezas y los especiales.

## Validación

97/97 pruebas EditMode correctas, incluido el importado de articulaciones, escala y materiales de los seis personajes. Captura de la ficha en `artifacts/cast-v4-unity.png`. La calidad artística requiere revisión visual; las pruebas no miden parecido con la referencia.

También permanecen las cuatro composiciones MIDI de dominio público, los controles de audio, los diez mapas ilustrados y los cómics desbloqueables. Fuentes musicales en `Assets/FrutiCity/AudioSources/README.md`; prompts de mapas en `docs/JOURNEY_IMAGE_PROMPTS.json`.
