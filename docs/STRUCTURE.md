# Resource folder guide

This is a folder-only reorganization of the v1.7.1 runtime assets. All 108 streamed filenames and binary contents are preserved; geometry, portal settings, LOD distances and audio behaviour have not been changed by the move.

The subsequent v1.7.2 door-tuning package adds `integration/doortuning/`, an opt-in companion under `optional/`, and the Normal Door (7) archetype correction. That metadata correction is separate from the folder-only move. See the [mandatory route-selection/merge notice](../integration/doortuning/README.md) before enabling door tuning.

## Where files belong

| Location | Contents |
| --- | --- |
| `stream/_manifest.ymf` | Registration/dependencies for the seven MLO interiors. Kept at the stream root. |
| `stream/interiors/bp_dpXX/` | One folder per active shop: shell, frames, glass, collision and `*_milo_.ymap` placement. |
| `stream/shared/` | `bp_delperro.ytyp`, `bp_interior.ytd`, and `bp_shop_door.ydr`. |
| `stream/exterior/models/` | Modified stock building, ground, detail and emissive drawables. |
| `stream/exterior/collision/` | Exterior collision and its high-detail counterpart. |
| `stream/exterior/lod/` | Exterior LOD/SLOD drawable dictionaries, including their embedded textures. |
| `stream/occlusion/` | `hei_sm_occl_00.ymap` and `hei_sm_occl_03.ymap` visual visibility overrides. |
| `stream/audio/` | Seven numeric proxy-hash `.ymt` files for interior audio occlusion. |
| `audio/` | `blue_plazas_game.dat151.rel`, registered explicitly in `fxmanifest.lua`. |
| `tools/` | Offline maintenance helpers, not client/server gameplay scripts. |

FiveM recursively scans `stream/` and registers streamed assets by filename, rather than by subfolder. See the [Cfx.re streaming implementation](https://github.com/citizenfx/fivem/blob/master/code/components/citizen-server-impl/src/ResourceStreamComponent.cpp). The shared `.ytyp` is still loaded through the unchanged `_manifest.ymf` dependencies. The existing `AUDIO_GAMEDATA` registration and root `audio/` location stay the same.

Do not rename asset files or keep two files with the same basename in different stream folders. Folders organize the resource; they do not create separate asset namespaces.

## Updating a flat installation

1. Disconnect players and close the server before changing streamed file paths. Do not hot-unload this map while clients are connected.
2. Back up the current resource. For a clean Git checkout, a fast-forward pull applies the tracked moves. For an archive installation, replace the old `stream/` directory with the new one rather than copying nested folders over the old flat files.
3. Keep any server-specific configuration backed up and reconcile it before replacing the resource. The resource name remains `blue_plazas`.
4. Ensure the Gabz `hei_sm_occl_00.ymap` compatibility copy still matches `stream/occlusion/hei_sm_occl_00.ymap`. This reorganization does not move the file inside Gabz.
5. Start the server normally, reconnect, and run the [quick testing pass](../TESTING.md#2-quick-first-pass), particularly doors, front-to-rear visibility, distant windows and audio.

The folder-only move does not require regenerating the compiled map/audio data. The authoring workspace's audio builder has been updated to discover nested maps/archetypes and retain their locations when regeneration is needed.

## Checking or organizing a build

From the resource root, with Python installed:

```powershell
python tools/resource_layout.py .
```

This reports the asset count and any planned moves without changing files. It rejects duplicate basenames and unknown asset categories. An already organized resource reports zero moves.

For a flat build, back it up and close the server, then apply:

```powershell
python tools/resource_layout.py . --apply
```

The helper checks destination paths before moving and compares all asset hashes afterward. On Windows, the command also refuses to apply while FiveM or FXServer is running. When using it on another platform, ensure the server is stopped yourself.

The main authoring builder now writes to these categorized directories. Historical one-off review/build scripts may still assume a flat stream folder: use a separate staging copy, select the correct output folder, and run the layout check before deployment. Never merge a newly compiled flat output into an organized live resource and leave duplicate basenames behind.

## Scope of verification

- Every streamed basename and SHA-256 must match the pre-move resource.
- Exactly seven shop placement maps and seven numeric audio metadata files must remain discoverable.
- Regenerating audio from the organized staging copy must preserve its folder layout and expected content.
- A fresh in-game start remains necessary to verify the new installation on the server.
