# Android y servicios externos

## Configuración reproducible

| Ajuste | Valor |
| --- | --- |
| Editor | Unity 6000.6.0f1 |
| Nombre | FrutiCity |
| Company | KhameSoul |
| Application ID | `com.khamesoul.fruticity` |
| Orientación | Vertical |
| Referencia de diseño | 1080 × 1920; vista de prueba 540 × 960 |
| Android mínimo | API 26 |
| Android objetivo | API 36 |
| Backend Android | IL2CPP |
| Arquitectura | ARM64 |
| Versión inicial | 0.1.0 / versionCode 1 |
| Publicación | AAB con clave de subida propia |

API 36 responde al requisito publicado para nuevas apps y actualizaciones de móvil desde el 31 de agosto de 2026. Revisa el requisito otra vez al publicar. [Google Play: nivel API objetivo](https://support.google.com/googleplay/android-developer/answer/11926878?hl=en-GB_ALL).

El menú **FrutiCity → Configure mobile project** aplica estos valores. No cambia el SDK activo de tu Editor ni elimina tus escenas. La compilación incluye únicamente la escena FrutiCity. El módulo Android se comprueba antes de intentar crear APK/AAB; si falta, usa Unity Hub → Installs → 6000.6.0f1 → Add modules → Android Build Support, Android SDK & NDK Tools y OpenJDK. [Unity: dependencias Android](https://docs.unity3d.com/6000.0/Documentation/Manual/android-install-dependencies.html).

## Firma y entrega a Play

El APK del menú usa firma de desarrollo para probar. Para el AAB, configura tu **upload keystore** en Player Settings → Publishing Settings, guardándolo fuera de Git. También puedes inyectar en el proceso de compilación:

```text
FRUTICITY_KEYSTORE_PATH
FRUTICITY_KEY_ALIAS
FRUTICITY_KEYSTORE_PASSWORD
FRUTICITY_KEY_PASSWORD
```

Las variables no se escriben en logs. No pegues contraseñas en código, README, consola compartida ni commits. El generador de AAB restaura la configuración de firma del Editor al terminar y nunca crea ni publica credenciales por su cuenta.

Antes del primer lanzamiento: instalar el APK en varios Android, revisar guardado tras suspensión/cierre, generar AAB firmado, incrementar versionCode en cada subida, completar ficha y clasificación, introducir política de privacidad y datos de soporte reales, declarar los datos efectivamente recogidos, revisar el informe previo al lanzamiento y las condiciones de prueba aplicables a la cuenta en Play Console. Esta entrega no realiza subidas a la consola.

## Firebase

La arquitectura debe seguir funcionando sin Firebase. Para conectarlo, registra la app Android con **el paquete exacto** `com.khamesoul.fruticity`, descarga su `google-services.json` e importa únicamente los módulos de Firebase Unity que vayas a utilizar. Primero configura Analytics/Crashlytics en una compilación de prueba; guardado en la nube y Remote Config necesitan decisiones de producto adicionales. No incluyas cuentas de servicio en el cliente. [Guía oficial de Firebase para Unity](https://firebase.google.com/docs/unity/setup).

`google-services.json` y `GoogleService-Info.plist` están excluidos de Git para mantener separada la configuración de cada entorno. Su ausencia no debe impedir jugar localmente. Un adaptador sin SDK es una interfaz de integración, no una conexión real con tu consola.

## AdMob

Los anuncios y las compras reales permanecen desactivados. La integración posterior requiere tu ID de aplicación AdMob, unidad de anuncio recompensado, Google Mobile Ads Unity Plugin y el flujo de consentimiento apropiado. Valida con anuncios de prueba y entrega el premio una sola vez al recibir la confirmación de recompensa; cerrar o fallar el anuncio no debe concederlo. [Instalación oficial de AdMob para Unity](https://developers.google.com/admob/unity/quick-start), [consentimiento en Unity](https://developers.google.com/admob/unity/privacy).

La selección real de audiencia y países en Play/AdMob determina cómo configurar la publicidad. No se ha marcado ficticiamente ningún consentimiento ni activado ningún anuncio por disponer de una interfaz de servicio.

## Cloudflare

El juego local no necesita Cloudflare. Su primer uso práctico puede ser alojar la web de soporte, la política de privacidad y `app-ads.txt` cuando exista un publisher ID verificado. Hace falta un dominio o proyecto Pages real, datos de contacto reales y contenido revisado antes de desplegar.

Pages permite conectar un repositorio o subir archivos precompilados. Elige el método según cómo quieras mantener la web; los proyectos Direct Upload y Git integration tienen restricciones para cambiar posteriormente de método. No se ha creado ningún dominio, página pública ni servicio remoto. [Cloudflare Pages: Git integration](https://developers.cloudflare.com/pages/get-started/git-integration/), [Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/).
