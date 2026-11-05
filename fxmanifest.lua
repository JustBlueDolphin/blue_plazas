fx_version 'cerulean'
game 'gta5'
author 'Blue-Box'
description 'Seven blank rentable shops with uniform double doors and storefronts at Del Perro Plaza: bp_dp01-05, bp_dp07 and bp_dp08. Built by _assets/blue_plazas/tools/build_delperro.py'
version '1.7.1'

this_is_a_map 'yes'

-- Three shell detail tiers plus baked storefront LOD/SLOD proxies.
-- Existing stock LOD map hierarchy is retained. No additional runtime scripts.

-- stream/_manifest.ymf registers the seven interiors (one *_milo_ ymap each) and loads bp_delperro.ytyp with them.
-- stream/ also replaces sm_11_bld2, its emissive layer and sm_11_0 collision and the hei_sm_occl_03 occluders with copies that have the shopfronts opened.

-- Audio occlusion: stream/<proxyhash>.ymt per unit + room audio settings. Built by tools/build_audio.py
files { 'audio/blue_plazas_game.dat151.rel' }
data_file 'AUDIO_GAMEDATA' 'audio/blue_plazas_game.dat'
