# Optional standalone door-tuning resource

**Use ONLY if your server has no existing custom `gta5.meta`, `replace_level_meta` owner or central `doortuning.ymt`. If it does (including Gabz), merge the plaza additions into your existing files instead. Do not overwrite your setup or start a second competing level-meta replacement.**

Place this folder at `resources/[maps]/blue_plazas_doortuning/`, keeping that exact resource name. Start it before `blue_plazas`:

```cfg
ensure blue_plazas_doortuning
ensure blue_plazas
```

Back up, close the server/disconnect clients, install, and perform a full server start and fresh connection. Keep `doortuning.ymt` as readable XML; do not compile it or move it into `stream/`.

Full route selection, merge instructions, AI-assistant tip and tests: [door-tuning installation guide](https://github.com/JustBlueDolphin/blue_plazas/tree/main/integration/doortuning).

**Status: file-validated, not game-tested.** The target regression environment is FiveM GTA V Legacy b3889. The upstream baseline has no declared exact game build; verify it on your own staging server. Other builds/Enhanced are not verified. Test stock doors as well as all plaza entrances.

See `NOTICE.md`, `BASELINE_SOURCES.json` and `LICENSE-AGPL-3.0.txt` for the pinned AGPL baseline, source and redistribution notices.
