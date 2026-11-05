# Source and modification notice

The vanilla `gta5.meta` and `doortuning.ymt` baseline comes from **GTA5 Door Editor**, Copyright (c) 2026 DevSync Studio, published under GNU Affero General Public License v3.0 (AGPL-3.0).

Source: https://github.com/DevSync-Studio/GTA5-Door-Editor/tree/a71ab13d4a9867e62110e1a5b18af0ac3879a001/src/assets/vanilla

The included `LICENSE-AGPL-3.0.txt` is the upstream license. `BASELINE_SOURCES.json` records exact download URLs and SHA-256 values. These readable metadata files are the corresponding source form; no compiled or hidden companion component is distributed.

Blue-Box modifications, 2026-11-05:

- `gta5.meta`: change only the door-tuning resource reference to `resources:/blue_plazas_doortuning/doortuning`.
- `doortuning.ymt`: retain the baseline and append the `bp_shop_standard` profile cloned from `DefaultStandard`, plus `bp_shop_door -> bp_shop_standard`.
- Add a minimal FiveM resource manifest and installation documentation.

Retain the license/source notices and provide the corresponding source and your modification notices when redistributing these AGPL-covered files. No paid Gabz file is included. The baseline license does not grant rights to unrelated game or plaza assets.

This companion is optional and not automatically enabled by `blue_plazas`. Use it only when your server has no existing central custom `gta5.meta` / `doortuning.ymt` owner. Otherwise merge the plaza additions into that owner; do not enable competing level-meta replacements.
