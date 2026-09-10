# Punto de continuación — tras reiniciar Claude Code

10 de septiembre de 2026, final de sesión. Escrito para retomar sin releer nada.

## Lo primero al volver: comprobar que Playwright está

Se dejó `.mcp.json` en la raíz del repositorio exterior con `@playwright/mcp`. **Los servidores MCP se cargan al arrancar la sesión**, así que sólo estará disponible después de reiniciar Claude Code. Node 22 y npx están instalados; `@playwright/mcp` se descarga solo con `npx -y` la primera vez.

Si al volver hay herramientas `mcp__playwright__*`, adelante. Si no, revisar que Claude Code haya aceptado el `.mcp.json` del proyecto (suele pedir aprobación la primera vez).

**Durante toda la sesión anterior NO hubo navegador**, y por eso Firebase se quedó a medias: no se pudo entrar en la consola a crear la app ni a descargar credenciales.

## Lo que hay que hacer con el navegador

Proyecto de Firebase: **khamesoul**. Paquete Android: **`com.khamesoul.fruticity`**. Método elegido por Fran: **Google** (sin correo y contraseña, para no pedirle formularios a nadie).

1. Añadir la app **Android** con ese nombre de paquete exacto.
2. Descargar `google-services.json` a **`FrutiCity/Assets/google-services.json`**. Ya está en el `.gitignore` de los dos repositorios.
3. **Authentication → Sign-in method → Google**, activar.
4. Registrar el **SHA-1** de la firma. El de **depuración también**: si no, el login falla sólo en los builds de desarrollo y parece un fallo del juego. Se saca con `keytool`.
5. Copiar el **Web client ID** que Firebase genera al activar Google.
6. Importar el **SDK de Firebase para Unity**, paquete de Authentication.

Detalle completo en [firebase-auth.md](firebase-auth.md).

## Lo que ya está hecho y verificado

`IAuthService` + `AuthUser`, con `LocalAuthService` (invitado) enchufado en `GameServices.Auth`. `Available` decide si la interfaz **dibuja** los botones de entrar; con `false` se queda una explicación, nunca un botón muerto.

`GameState.playerId`: identificador del **dispositivo**, generado una vez y estable. Sobrevive a «empezar de cero» a propósito.

El perfil y la portada ya leen del servicio. **No hay que tocarlos** al enchufar Firebase: entra un `FirebaseAuthService : IAuthService` y se cambia la línea de `GameServices` que hoy crea el local.

`SaveSync`: qué pasa con el progreso al iniciar sesión. Es la pieza que hace posible «continuar desde cualquier dispositivo». Clase **pura** —sin red, sin disco, sin Unity— y por eso cubierta entera por pruebas.

## La regla que no se puede romper

**Nunca pisar progreso sin preguntar.** Iniciar sesión es la única acción del juego que destruye algo irrecuperable. `SaveSync` sólo decide solo cuando no hay nada que perder:

| Situación | Decisión |
| --- | --- |
| La cuenta no tiene partida | Subir la de este móvil |
| Este móvil sin estrenar | Bajar la de la cuenta |
| La cuenta sin estrenar | Subir la de este móvil |
| Misma partida y aquí más nueva | Subir (se jugó sin cobertura) |
| **Las dos con progreso** | **Preguntar. Siempre** |

Pregunta **aunque la de aquí vaya muy por delante**: eso también sería borrarle un barrio entero a alguien. El `playerId` es del dispositivo, no de la cuenta, así que dos móviles con la misma cuenta nunca caen en la rama automática.

## Lo que falta después de la autenticación

- **Transporte de la copia en la nube.** `ICloudSaveService` existe y hoy devuelve que no a todo. Falta el backend: Firestore, o Cloudflare, que Fran también tiene.
- **La pantalla de elegir** cuando `SaveSync` devuelve `AskThePlayer`. La lógica y los textos (`SaveSync.Describe`) están; falta el modal. Debe enseñar las dos partidas por niveles y estrellas, **no por fechas**: «guardada el martes a las 21:14» no dice cuál conviene conservar.
- **Vincular la partida de invitado** a la cuenta al entrar por primera vez, sin perder el progreso.

Y del plan general siguen pendientes: eventos y temporadas, álbum, compras, analítica. Más dos cabos de la fase 4: persistir el scroll de la ciudad entre sesiones y dar vida ambiental al camino.

## Estado del proyecto

Versión **2.1.0**, etiquetada en los dos repositorios. Estable y autónoma: se instala y se juega entera sin red y sin cuenta.

El APK instalado en el móvil de Fran es el **2.0.0**; el 2.1.0 aún no se ha compilado para Android. Su móvil es de **64 bits puros** (`arm64-v8a`, sin `armeabi-v7a`), así que el atajo de Mono/ARMv7 del `ProjectBuilder` **no sirve**: hay que ir por IL2CPP/ARM64 aunque tarde ~20 minutos.
