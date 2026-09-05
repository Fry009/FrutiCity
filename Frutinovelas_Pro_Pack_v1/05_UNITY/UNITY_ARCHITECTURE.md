# UNITY ARCHITECTURE

## Unity
Usar una versión LTS estable disponible en el momento de empezar producción.

## Rendering
Para un juego 2D ligero:
- URP 2D opcional;
- Sprite Atlas;
- Addressables solo cuando el contenido lo justifique;
- evitar shaders caros.

## Escenas
1. Boot
2. Main
3. Merge
4. Match3
5. Home
6. Story
7. Shop

Para MVP se puede simplificar a:
- Boot
- Main
- Gameplay

con paneles cargados aditivamente.

## Servicios
`GameServices`
- SaveService
- EconomyService
- ProgressionService
- AudioService
- SceneService
- AnalyticsService
- AdsService (stub)
- IAPService (stub)

## Datos
Preferir ScriptableObjects para authoring.
Guardar IDs estables y serializar solo progreso.

## Entidades
- CharacterDefinition
- MergeItemDefinition
- MergeChainDefinition
- OrderDefinition
- Match3LevelDefinition
- FurnitureDefinition
- EpisodeDefinition

## Runtime
- MergeBoardController
- MergeCell
- MergeItemView
- GeneratorController
- OrderController

- Match3BoardController
- TileView
- MatchDetector
- CascadeResolver
- ObjectiveController
- PowerupResolver

- HomeController
- FurnitureSlot
- DecorationSelectionPanel

- StoryController
- DialogueLine
- DialoguePanel

## Save
JSON local:
- currencies;
- unlockedEpisodes;
- characterXP;
- completedLevels;
- stars;
- furnitureSelections;
- mergeBoard state;
- daily reward timestamp.

Añadir versionado de save desde el día 1.

## Android
- orientación portrait;
- IL2CPP para release;
- ARM64;
- minSdk según necesidades reales del SDK de ads/analytics;
- target API actualizado al requisito vigente de Google Play;
- App Bundle `.aab`.

## iOS futuro
No acoplar:
- rutas Android;
- plugins Java;
- billing;
- notificaciones.
Encapsular todo en interfaces.

## Rendimiento
Objetivo:
- 60 FPS en gama media;
- memoria controlada;
- atlas por pantalla;
- pooling para fichas, VFX y objetos merge;
- evitar Instantiate/Destroy repetido durante cascadas.
