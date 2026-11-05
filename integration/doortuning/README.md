# Door tuning: choose ONE installation route

> **Already using a custom `gta5.meta`, a `replace_level_meta` resource, or `doortuning.ymt` (including Gabz)? You MUST merge the supplied plaza profile and model mapping into your existing central `doortuning.ymt`. Integrate the `DOOR_TUNING_FILE` reference into your existing `gta5.meta` setup only if needed. Preserve existing entries and unrelated meta settings. Do not overwrite existing files with the standalone files or enable a second competing `gta5.meta` replacement. If your existing `gta5.meta` already points to the central file being updated, its reference needs no change.**

**Tip:** Using an AI coding assistant can make this merge much quicker than doing it manually. Give it your existing `gta5.meta` and `doortuning.ymt` plus the supplied plaza entries, and ask it to merge them while preserving existing settings and avoiding duplicate profiles or mappings. Back up your files and check the result before installing. Share only files you are authorised to share; server secrets are not needed.

## Package contents and status

- Main resource: `blue_plazas`, independent of Gabz and with no `replace_level_meta` directive or dependency on the optional companion.
- Standalone resource: `optional/blue_plazas_doortuning/` in the repository, or the separate companion ZIP in the release. Contains `fxmanifest.lua`, `gta5.meta`, readable XML `doortuning.ymt`, source notices and license.
- Merge route: `plaza_entries.xml`, `merge.py` and `test_merge.py` in this directory. The full local Gabz tuning file is **not** distributed.
- v1.7.2 is **file-validated, not game-tested**. v1.7.1's earlier smoke-test result does not validate this new door configuration.

The standalone baseline is pinned to the vanilla assets in [DevSync Studio's GTA5 Door Editor](https://github.com/DevSync-Studio/GTA5-Door-Editor/tree/a71ab13d4a9867e62110e1a5b18af0ac3879a001/src/assets/vanilla), published under AGPL-3.0. Keep the included license, modification notice and source references when redistributing these baseline-derived files. This baseline license is not a statement licensing all other plaza assets. No paid Gabz tuning or level-meta file is included.

## Route A — no existing level-meta/door-tuning owner

**Before following these steps, check for an existing `gta5.meta`, `replace_level_meta` or central `doortuning.ymt`. If present, use Route B; do not enable this companion alongside it.**

1. Stop the server and disconnect clients. Back up the current installation.
2. Place the main resource at `resources/[maps]/blue_plazas/` so its `fxmanifest.lua` is directly inside that folder.
3. Copy **only** `optional/blue_plazas_doortuning/` (or extract the companion ZIP) to `resources/[maps]/blue_plazas_doortuning/`. Keep the name `blue_plazas_doortuning`: its `gta5.meta` references that exact resource name. Do not leave multiple extracted copies in resources.
4. Add the explicit start order below. Do not add the companion when using Route B.

```cfg
ensure blue_plazas_doortuning
ensure blue_plazas
# Start your existing doorlock/business integration afterward, if used.
```

5. Fully start the server and reconnect clients. A hot resource restart is not proof that level metadata reloaded.
6. Run the door and unrelated-door regression checks below before production use.

The companion's only level-meta change from the upstream baseline is:

```xml
<Item>
  <filename>resources:/blue_plazas_doortuning/doortuning</filename>
  <fileType>DOOR_TUNING_FILE</fileType>
</Item>
```

There is deliberately **no `.ymt` extension in that reference**. The actual resource file is named `doortuning.ymt` and remains readable XML. Do not compile it with CodeWalker or move it into `stream/` for this loading method.

## Route B — Gabz or another existing central owner

Keep your existing central owner and its existing start order. **Do not start `blue_plazas_doortuning`.** For the current Gabz server:

```cfg
ensure cfx-gabz-mapdata
ensure blue_plazas
# Keep existing dependencies and other resources in their normal order.
```

### Automated merge (recommended)

Run from the `blue_plazas` folder with Python installed. This creates a staged file outside the live resource and leaves the original untouched:

```powershell
python integration/doortuning/merge.py --resource "../cfx-gabz-mapdata" --output "../../../staging/blue_plazas/doortuning.ymt"
```

Use your actual central resource path; Gabz may be in another category folder. The example layout assumes the two resources are siblings. The tool verifies that the existing resource manifest loads `gta5.meta` and `doortuning.ymt` and that the level-meta `DOOR_TUNING_FILE` points to `resources:/<existing-resource-name>/doortuning`.

The tool clones that installation's complete `DefaultStandard` profile as `bp_shop_standard`, preserving its schema and values, then adds one mapping for `bp_shop_door`. It retains every unrelated entry and all original source bytes. Repeating it adds nothing. Conflicting custom entries or unresolved references stop the merge instead of being silently overwritten. Existing vendor duplicate mappings are reported and preserved; duplicate plaza entries are rejected.

Review the output and `.report.json`. With FiveM and FXServer closed, install with a backup:

```powershell
python integration/doortuning/merge.py --resource "../cfx-gabz-mapdata" --output "../../../staging/blue_plazas/doortuning.ymt" --install --backup-dir "../../../backups/blue_plazas_doortuning"
```

The automatic installer supports Windows and checks that FiveM/FXServer processes are closed. On other platforms, stage the merge, stop the server, back up the original, and copy the reviewed file into place manually. Perform a full server start and fresh client connection afterward.

**Existing custom paths:** if your central tuning is stored somewhere other than `<resource>/doortuning.ymt`, or your level-meta setup uses different manifest paths, the automated loader check stops. Use the manual procedure below, preserving your existing path. Do not create another level-meta replacement to bypass the check.

### Exact entries for a manual or AI-assisted merge

Open [`plaza_entries.xml`](plaza_entries.xml). It contains **only the plaza additions**, not a replacement baseline:

1. Under `NamedTuningArray`, add the complete `Item` whose `Name` is `bp_shop_standard`, including its entire `Tuning` element. Alternatively clone your existing `DefaultStandard` item and change only its `Name` to `bp_shop_standard`; this is what the merge tool does.
2. Under `ModelToTuneMapping`, add exactly once:

```xml
<Item>
  <ModelName>bp_shop_door</ModelName>
  <TuningName>bp_shop_standard</TuningName>
</Item>
```

3. Confirm every `TuningName` resolves, the custom name/model occurs only once, and existing profiles/mappings are unchanged.
4. Inspect the **existing** `gta5.meta` `DOOR_TUNING_FILE` item. If it already points to the central file you updated, leave it unchanged. Otherwise integrate the reference to your central resource's tuning path, without an extension, and ensure that file is listed in that resource's manifest. Preserve all unrelated metadata. Do not replace the whole `gta5.meta` with the standalone copy.
5. Back up before installation, cold-start and reconnect. Reapply/review the merge after vendor updates.

## Behaviour and model scope

All 20 placed plaza door leaves use `bp_shop_door`; none currently use `v_ilev_ch_glassdoor`. The new profile affects the custom model everywhere it is used, not an individual entrance. Do not map or globally retune the stock model for this plaza.

The supplied baseline keeps `DelayDoorClosingForPlayer`, trigger-box auto-opening disabled, mass/weapon impulse multipliers at 1, latching disabled and `StdDoorOpenBothDir`. Other values, including the rotation-limit value of 0, are retained from `DefaultStandard` without inventing new behaviour. This is not a request for automatic doors or a new swing angle. Door locks/access permissions still belong to doorlock scripting.

The v1.7.2 archetype correction sets `specialAttribute` to **Normal Door (7)**. Dynamic and Enable Door Physics flags were already present; the hinge origin, embedded box collision, mesh, placement and portals remain unchanged. Tuning is not a replacement for correct asset physics.

## Build limitations and verification

- Intended test environment: FiveM GTA V Legacy, with **b3889** as the current project's regression target. The new routes have not yet been game-tested on b3889 or any other build. There is no verified support claim for Enhanced/RedM or other builds.
- The standalone baseline's exact game build is not declared upstream. It is pinned and source-hashed for reproducibility, but should be checked against the recipient's enforced build on a staging server. Do not assume a complete level-meta replacement is universally compatible.
- File validation: 35 baseline profiles and 94 mappings preserved in the standalone copy; one profile and one mapping added. The local Gabz merge preserves its 35 profiles and 326 mappings. Existing baseline duplicate mappings are retained, not newly introduced.
- Merge tests cover repeat application, conflict rejection, missing references, partial merges, baseline field preservation, vendor duplicates and line endings.

Run these checks on the installation route actually selected:

- [ ] Confirm only one central `replace_level_meta 'gta5'` owner is enabled and its tuning reference resolves.
- [ ] After a full server start and fresh client connection, visit every entrance and test all 20 leaves.
- [ ] Push from both sides; inspect opening, return/closing, deliberate no-latch baseline behaviour and swing clearance.
- [ ] Check mirrored left/right leaves and the rear doorway from both clients.
- [ ] Test any existing doorlocks without changing their access configuration.
- [ ] Stream the plaza out/back, reconnect and repeat representative tests.
- [ ] Test unrelated stock/Gabz doors, including a sliding/garage example where available, for regressions.
- [ ] Record build, route, baseline/source commit, results and any differences; leave untested routes marked untested.

References: [demonstrated central-file loading method](https://github.com/Hedgehog-Technologies/doortuning-example), [Cfx.re door asset requirements](https://docs.fivem.net/docs/assets-manual/beginner-series/part-8/), and the pinned source/license records in `BASELINE_SOURCES.json`.
