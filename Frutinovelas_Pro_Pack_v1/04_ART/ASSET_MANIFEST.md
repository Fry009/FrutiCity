# ASSET MANIFEST — MVP

## Characters
Por cada uno de los 6 personajes:
- full_idle
- full_happy
- full_sad
- full_angry
- full_surprised
- full_working
- portrait_neutral
- portrait_happy
- portrait_angry
- icon_round
- shadow
- 1 idle animation
- 1 celebration animation

Naming:
`char_<id>_<state>.png`

## Merge
### 3 generadores
- gen_cesta_cocina
- gen_almacen
- gen_estudio_social

### 21 objetos
Ver `MERGE_CHAINS.json`.

Naming:
`merge_<chain>_l<level>_<name>.png`

## Match-3
Normales:
- tile_apple
- tile_banana
- tile_strawberry
- tile_orange
- tile_grape
- tile_kiwi

Especiales:
- power_rocket_h
- power_rocket_v
- power_bomb
- power_rainbow

Obstáculos:
- obstacle_box
- obstacle_jam
- obstacle_ice
- obstacle_root
- obstacle_sticky_choco

## Furniture
30 variantes mínimas:
- 10 slots x 3 opciones.

## Backgrounds
- bg_home_exterior
- bg_living_room_empty
- bg_kitchen_empty
- bg_bedroom_empty
- bg_merge_board
- bg_match3
- bg_story_generic
- bg_shop

## UI
Top bar:
- icon_coin
- icon_star
- icon_energy
- icon_gem

Nav:
- nav_home
- nav_merge
- nav_play
- nav_story
- nav_shop

Buttons:
- btn_primary
- btn_secondary
- btn_close
- btn_reward
- btn_locked

Panels:
- panel_dialogue
- panel_order
- panel_reward
- panel_shop_card
- panel_level_result

## VFX
- vfx_merge_pop
- vfx_match_small
- vfx_match_big
- vfx_coin_fly
- vfx_star_fly
- vfx_confetti
- vfx_unlock
- vfx_powerup

## Audio
Music:
- music_home
- music_merge
- music_match3
- music_story
- music_victory

SFX:
- tap
- merge
- match
- combo
- powerup
- coin
- star
- reward
- decorate
- unlock
- victory
- fail
