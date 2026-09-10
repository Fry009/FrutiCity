# Cuentas: qué está hecho y qué falta

10 de septiembre de 2026. Proyecto de Firebase: **khamesoul**. Paquete Android: **`com.khamesoul.fruticity`**. Método elegido: **Google** (sin correo y contraseña).

## Hecho y verificado

`IAuthService` + `AuthUser`, con `LocalAuthService` (invitado) enchufado en `GameServices.Auth`. El juego no sabe quién resuelve el inicio de sesión.

`Available` es el interruptor de toda la interfaz: dice si hay un proveedor **de verdad** detrás. Con `false`, ni el perfil ni la portada dibujan botones de entrar — se queda una explicación. **Un botón muerto es peor que ningún botón**, porque el jugador lo pulsa y concluye que el juego está roto.

`GameState.playerId` es un identificador local, generado una vez en `Normalize` y estable a partir de ahí. **Sobrevive a «volver a empezar de cero»** a propósito: sigue siendo el mismo jugador, y es lo que permitirá vincular esta partida a una cuenta sin que el progreso se quede huérfano. Se genera en `Normalize` y no en el constructor porque una partida guardada antes de que esto existiera llega sin él.

**120/120 pruebas EditMode.** Las cinco nuevas cubren lo que, si se rompe, regala progreso o deja la interfaz colgada: que `Current` nunca sea null (la interfaz lo lee sin comprobar), que sin proveedor los métodos **fallen con un motivo escrito** (un éxito falso daría por iniciada una sesión que no existe), que el callback se llame **siempre** (o la interfaz se queda esperando) y que `playerId` ni se regenere en cada carga ni se pierda al reiniciar.

## Lo que falta, y sólo puede venir de la cuenta de Fran

1. **App Android en Firebase** con el nombre de paquete exacto `com.khamesoul.fruticity`.
2. **`google-services.json`** en `FrutiCity/Assets/google-services.json`.
3. **Authentication → Sign-in method → Google**, activado.
4. **SHA-1 de la firma** registrado en Firebase. Se saca con `keytool` del keystore que se use para firmar; hay que registrar el de **depuración** también, o el login falla sólo en los builds de desarrollo y parece un bug del juego.
5. **Web client ID**, que Firebase genera al activar Google. Hace falta para el flujo de Android.
6. **SDK de Firebase para Unity** (paquete de Authentication) importado en el proyecto.

## Seguridad

El repositorio del juego **no ignoraba `google-services.json`**. El exterior sí, pero el fichero tiene que vivir en `Assets/` para que Unity lo empaquete, y ahí no estaba cubierto: el primer `git add -A` tras enchufar Firebase lo habría subido a GitHub. Corregido, junto con keystores, `.p12`/`.pfx` y cuentas de servicio.

## Cuando lleguen las credenciales

Entra un `FirebaseAuthService : IAuthService` y se sustituye la línea de `GameServices` que hoy crea el `LocalAuthService`. **El perfil y la portada no se tocan**: ya leen del servicio.

Lo que habrá que decidir entonces, y no antes:

- **Qué pasa al iniciar sesión con una partida local ya empezada.** Vincular (conservar el barrio) o descargar el de la cuenta. Vincular es lo correcto por defecto; sobrescribir el progreso de alguien sin preguntar es la peor cosa que puede hacer un juego con cuentas.
- **Copia en la nube.** `ICloudSaveService` ya existe y hoy devuelve que no a todo. Es una decisión aparte de la autenticación: se puede tener cuenta sin sincronizar.
- **Borrar la cuenta** frente a **borrar la partida**. Hoy el perfil ya las separa, y tienen que seguir separadas: se debe poder hacer una sin la otra.
