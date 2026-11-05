# Blue Plazas

Seven blank shop interiors at Del Perro Plaza, intended for players to furnish as their own businesses.

## Folder structure

```text
blue_plazas/
├── fxmanifest.lua
├── README.md
├── TESTING.md
├── audio/                    # Game audio settings (.dat151.rel)
├── docs/
│   └── STRUCTURE.md          # Folder guide and update instructions
├── tools/
│   └── resource_layout.py    # Validate or organize a build
└── stream/
    ├── _manifest.ymf         # Interior registration
    ├── interiors/
    │   ├── bp_dp01/          # Each shop's shell, frames, glass, collision and placement
    │   ├── bp_dp02/
    │   ├── bp_dp03/
    │   ├── bp_dp04/
    │   ├── bp_dp05/
    │   ├── bp_dp07/
    │   └── bp_dp08/
    ├── shared/               # Archetypes, common textures and door model
    ├── exterior/
    │   ├── models/           # Building and ground drawables
    │   ├── collision/        # Exterior collision
    │   └── lod/              # Distant building models
    ├── occlusion/            # Visual occlusion map overrides
    └── audio/                # Per-interior numeric audio metadata (.ymt)
```

See [the folder guide](docs/STRUCTURE.md) before updating an existing installation. This reorganization preserves all 108 streamed asset names and their contents.

## Testing v1.7.1

**[Open the full testing checklist](TESTING.md)**

Initial user feedback is that the latest fixes work so far. Full testing is still pending. The checklist covers every shop, front-to-rear visibility, window LOD transitions, doors, collision, surfaces, lighting, audio, multiplayer, and performance.

Current units: `bp_dp01`, `bp_dp02`, `bp_dp03`, `bp_dp04`, `bp_dp05`, `bp_dp07`, and `bp_dp08`.

### Latest fixes to verify

- Storefronts remain visible through the transition to the distant building model, without the plain-panel gap.
- The exterior remains visible through the rear door when viewed from the front of the building.
- The plaza and Gabz copies of `hei_sm_occl_00.ymap` use the same compatible correction. Both copies must remain in sync; a vendor update may replace the Gabz copy.

Make map updates with players disconnected. Use a clean server start and reconnect for validation; a previous live map restart caused a client crash.
