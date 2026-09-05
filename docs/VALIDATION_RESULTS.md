# Resultados de validación

Fecha de trabajo: 5 de septiembre de 2026. Entorno: Windows 11 y Unity 6000.6.0f1.

## Comprobaciones completadas durante la implementación

- Auditoría del Pro Pack: seis personajes, tres cadenas de siete objetos, cincuenta niveles, tres habitaciones/diez slots/treinta variantes y diez episodios.
- Motor match-3 compilado con Roslyn y ejecutado con Mono/NUnit: **26/26 pruebas correctas**. Incluye aperturas jugables sin matches, determinismo, intercambios inválidos, cascadas, creación/encadenado de especiales, cinco obstáculos, boosters y victoria/derrota.
- Los objetivos de cajas y mermelada del pack se validan aunque la lista original de obstáculos no los enumere.

## Integración en curso

La compilación completa de Unity, los tests EditMode integrados, las capturas de la aplicación y el resultado de compilación Windows se registrarán aquí al terminar la integración. No se consideran aprobados por los resultados aislados del motor.

La instalación original de Unity tenía módulos Windows y WebGL. Se inició la instalación de Android Build Support y sus dependencias mediante Unity Hub. Un módulo descargándose no equivale a un APK generado.

## Sin validar en esta estación

- Comportamiento táctil y rendimiento de un teléfono Android físico.
- Safe areas reales, accesibilidad asistida, temperatura y memoria en gama media.
- Balance humano y tasas de victoria de los cincuenta niveles.
- Firma de producción, subida a Play Console y revisión de tienda.
- SDKs y consolas reales de Firebase/AdMob, consentimientos y despliegue de Cloudflare.

Los registros temporales se escriben en `artifacts/` y los ejecutables en `FrutiCity/Builds/`; ambos se excluyen de Git. La matriz y el recorrido de aceptación están en [QA.md](QA.md).
