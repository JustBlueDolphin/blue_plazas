# Del Perro Plaza — v1.7.2 testing checklist

**Status:** v1.7.1's initial user smoke test reported working; detailed verification is pending. The v1.7.2 organized installation and door tuning are file-validated only, with both tuning routes awaiting game testing. All boxes below start unchecked. Compiled-file checks do not count as in-game passes.

Test the actual deployed server with its normal map resources enabled, including `cfx-gabz-mapdata`. Record a result for each shop rather than assuming one passing shop covers the others.

For recipients without Gabz, test the standalone route on their normal server setup. For recipients with an existing `gta5.meta`/`doortuning.ymt` owner, use the merge route. Never enable both. Follow the [installation/merge notice](integration/doortuning/README.md).

## Door-tuning installation gate

- [ ] Record the selected route: standalone companion / existing central-file merge. Verify only one central level-meta owner is enabled.
- [ ] Confirm the central `gta5.meta` points to the intended `DOOR_TUNING_FILE`, with no unnecessary changes to existing metadata.
- [ ] Confirm `bp_shop_standard` and its `bp_shop_door` mapping occur once; all tuning references resolve and existing entries are preserved.
- [ ] Start the server from closed and reconnect. A hot resource restart does not count as reloading level metadata.
- [ ] Test every entrance and all 20 leaves: push both sides, opening/closing, baseline latching behaviour, swing clearance and any existing doorlocks.
- [ ] Test stream-out/back, a fresh reconnect, and mirrored left/right leaves with a second client.
- [ ] Test unrelated stock/Gabz doors for regression, including sliding/garage behaviour where available.
- [ ] Record exact build and baseline/source version. FiveM Legacy b3889 is the current target, but neither route has a recorded in-game pass yet; do not assume other builds/Enhanced are supported.

## 1. Record the test session

- Tester / date:
- Resource version / repository commit:
- FiveM game build and client channel:
- Other plaza/area map resources enabled:
- Graphics settings, extended distance scaling, resolution and any visual mods:
- Time / weather:
- Player count / client hardware for performance comparisons:

Before testing, disconnect players before changing map files. Do not hot-restart or unload the plaza with players connected: this previously caused a crash. Use a clean server start and a fresh connection for installation tests.

## 2. Quick first pass

- [ ] Cold-start the server with its normal resources, connect, and visit the plaza. No missing assets, streaming errors or crash.
- [ ] Walk into and out of every shop through every entrance. No invisible barriers, falls or doorway snags.
- [ ] Stand outside the front of the large ground-floor shop (`bp_dp05`) and look through to the rear door. Trees, road and buildings beyond remain visible instead of disappearing into a blank background.
- [ ] Repeat that view while moving sideways, looking through adjacent front panes, and opening/closing the front and rear doors.
- [ ] Move away from and back toward all storefronts. Window frames and the storefront appearance remain present through the distance transitions.
- [ ] Visit at night. Interiors are usable without the entire plaza glowing excessively or windows becoming featureless white panels.
- [ ] Drive away until the plaza unloads, return, then disconnect/reconnect. The fixes still hold.

## 3. Shop coverage record

Use `PASS`, `FAIL + issue link`, or `NOT TESTED` in each cell. These are the seven active units; there are no active `bp_dp06`, `bp_dp09` or `bp_dp10` units in this build.

| Unit | Doors / collision | Surfaces / usable space | Visibility / LOD | Lighting | Audio | Second client |
| --- | --- | --- | --- | --- | --- | --- |
| bp_dp01 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp02 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp03 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp04 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp05 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp07 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |
| bp_dp08 | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED | NOT TESTED |

## 4. Rear-door visibility and occlusion

Priority regression: exterior scenery was being hidden when looking through the building. A duplicate Gabz occlusion map still contained blockers already removed from the plaza copy.

- [ ] From several positions in the car park, look through front doors and windows toward the rear exit. No missing scenery, solid invisible cut-off or abrupt pop-in.
- [ ] Walk from outside the front, through the shop, and out the rear while looking toward that exit. The view remains consistent as the camera crosses each doorway.
- [ ] Repeat in reverse: look through the rear doorway toward the front, then walk through.
- [ ] Test both sides of the rear opening, its side glass and the transom above it. No narrow strips of missing scenery.
- [ ] Repeat standing, crouched, in first person and in third person. Test close to each jamb and with the camera angled across the opening.
- [ ] Test doors closed, partly open and fully open. Closed glass doors must not incorrectly hide the world beyond them.
- [ ] Check side windows, upstairs windows and views between nearby shops for similar missing scenery.
- [ ] Recheck with normal Gabz resources loaded after a full server restart. No temporary occlusion-disabling diagnostic may be running during acceptance testing.

Operator check: compare the SHA-256 of `blue_plazas/stream/occlusion/hei_sm_occl_00.ymap` with `cfx-gabz-mapdata/stream/gabz-occlusion/hei_sm_occl_00.ymap`. They must match the reviewed compatible file. Older flat installations keep the plaza file directly under `stream/`. The merged correction retains Gabz's 71 boxes and removes 21 plaza-intersecting triangles. Recheck after any Gabz update. Do not fix this by disabling occlusion globally.

## 5. Window LOD and streaming transitions

Walk and drive the same approach from the car park, street/bus-stop side, rear, and both road approaches. Test moving away and moving back in, plus oblique views along the storefronts.

| Approximate distance | What to inspect |
| --- | --- |
| 0–40 m | Close glass, frame edges, doors, floors and lights; no flickering or missing parts. |
| 40–80 m | Reduced interior detail retains the room shape and storefront alignment. |
| 80–170 m | Priority regression range: no interval where windows turn into plain panels before the exterior LOD appears. |
| 170–300 m | Distant storefront textures stay aligned and retain recognizable window/frame detail. |
| 300–500 m and beyond | Whole-building silhouette, roof and signage transition cleanly into the regional distant model. |

Distances are sampling guides, not exact switch points: the game also uses bounds and graphics settings. Distant windows use baked representations; they do not need to expose a fully rendered, transparent interior at long range.

- [ ] Check every distance band in both directions, including stopping near a transition and moving a few metres back and forth.
- [ ] Repeat at ordinary and higher extended-distance settings; record which setting exposes any gap.
- [ ] Check front frames, rear doors, roof edges, corners and upstairs railings for floating parts or abrupt loss of the building silhouette.
- [ ] Verify removed arrow/sign frames and decals do not reappear as the LOD changes. The retained Del Perro Plaza identification should stay consistent.
- [ ] Test a fast vehicle approach and a fresh visit after travelling far away. No persistent missing textures or interiors after streaming settles.
- [ ] Repeat key transitions at night; emissive LODs should not flash, float or turn the storefronts into bright blank rectangles.

## 6. Doors, thresholds and collision

There are ten double-door entrances in this build, with twenty moving leaves. Visit every entrance, including the rear and upstairs access.

- [ ] Both leaves open and close correctly, have consistent proportions and handles, and sit squarely in their frames.
- [ ] Walk, run and crouch through each side of every doorway in both directions. No snag at the jamb, centre seam, floor or top of the opening.
- [ ] Check full door swings against nearby walls, floors, frames and the other leaf. No obvious clipping or invisible leftover door collision.
- [ ] Walk up/down the rear steps and across front thresholds at an angle. No floating feet, sudden drops, stuck spots or mismatched step collision.
- [ ] Walk against all walls, glass and the filled bus-stop-side wall. Solid surfaces stop the player; intended entrances stay passable.
- [ ] Check corners, curved walls, room joins and the edges of the expanded floor area. No walk-through wall or fall-through floor.
- [ ] Check upstairs floor collision and the ceiling beneath it. Players should not fall between levels or enter an unintended roof void.
- [ ] With a second player, confirm both clients see the same moving-door position and passage. If a separate door-lock system is used, test its lock/unlock states separately.
- [ ] Where server rules allow, check a few bullet impacts on walls, glass, doors and steps for misplaced collision. Log the expected glass behaviour before calling breakage a defect.

## 7. Blank-store finish and usable space

- [ ] Walk the full perimeter and every recess of each shop. All intended space is accessible and usable for a tenant layout.
- [ ] Inspect walls and rounded corners at close range. No jagged joins, exposed edges, overlapping surfaces or unwanted old branding.
- [ ] Look up across the entire ceiling and down across the entire floor, especially room joins and storefront edges. No holes, seams showing daylight, floating panels or intersecting surfaces.
- [ ] Inspect the roof from legitimate exterior viewpoints and, in an authorised admin inspection, from above. It should remain a coherent closed exterior.
- [ ] Inspect exposed returns, underside edges and both sides of accessible surfaces for missing backfaces. Do not classify deliberate admin camera clipping through a solid wall as a player-visible defect.
- [ ] Check window rails, sills, door surrounds and floor aprons while moving slowly at shallow angles. No texture flicker or z-fighting.
- [ ] Inspect the rear step treads and risers closely. Textures should be consistent, with no stretched or broken patches.
- [ ] Confirm the bus-stop-side former window section is a finished solid wall from both sides, including distant views.
- [ ] Confirm removed signs and decals are gone at close range while retained architectural features remain intact.
- [ ] If a furnishing system is available, temporarily place representative shelves, a counter and a table near walls, corners and windows. Check floor contact, access and clear sightlines; remove test props afterward.

This resource supplies the shop shells. Rental, purchase, inventories, furniture saving and business scripts need their own integration tests; their absence is not a shell geometry failure.

## 8. Lighting and weather

- [ ] Inspect each shop at midday, dusk and full night. Rooms remain readable without washed-out walls or excessive glare.
- [ ] Walk through front and rear entrances in both directions. No severe exposure flash, unexplained dark patch or lighting boundary across the room.
- [ ] Inspect ceiling panels from below and storefronts from outside. Light sources stay attached to the correct surfaces and look consistent across LOD changes.
- [ ] Check sunlight/shadows near walls, floors and ceilings for large leaks through solid geometry.
- [ ] Repeat representative views in clear, overcast and rainy weather. Note indoor rain/wetness or visual-mod-specific behaviour separately.
- [ ] Compare upstairs, the large ground shop and the strip shops at the same time/weather so one overly bright unit is easy to identify.

## 9. Audio

Use two clients where possible. Test a consistent game-world sound first, then any separate voice/music/business-audio integration. A custom voice or music script may have its own occlusion rules.

- [ ] Listen on both sides of a solid wall, a closed door, an open door and fixed glass. Attenuation should be appropriate and transitions should be smooth.
- [ ] Repeat at the rear doorway while the listener is near the front, and with the source/listener positions exchanged.
- [ ] Walk across each threshold; no sudden silence, stuck muffling or incorrect room sound after leaving.
- [ ] Compare neighbouring shops and upstairs/downstairs. Sound should not behave as though all units are one room.
- [ ] If `blue_audiotools` is enabled, use `/soundcheck` to confirm glass settings affect the intended active unit. Record and restore the starting settings after testing.
- [ ] Reconnect and repeat one door/glass test. Confirm the intended settings survive the normal server setup.
- [ ] Test voice and any shop music separately, recording which audio system produced a failure.

## 10. Multiplayer, performance and stability

- [ ] Have players inside different shops while another approaches from outside. All see the expected interiors, doors and exterior scenery.
- [ ] Join while another player is already inside, then swap roles. No late-join missing geometry or incorrect door state.
- [ ] Repeat a fixed walking/driving route around the block and through the shops. Record average FPS, noticeable frame-time spikes and streaming stutters under the same weather/settings/player count.
- [ ] Repeat on a lower-spec client if available. Compare against an agreed baseline; do not compare different camera views or graphics settings as if they were identical.
- [ ] Compare one occupied shop with several occupied/furnished shops. Separate furnishing-script load from the empty-shell result.
- [ ] Spend at least 20–30 minutes visiting, leaving and returning to the area. Watch for accumulating stutter, texture loss, crashes or F8 errors.
- [ ] After everyone disconnects, perform a clean server restart and reconnect. Confirm both visual regressions stay fixed with normal resource startup.
- [ ] Capture relevant client/server errors and crash timestamps. A single successful visit is not a stability pass.

## 11. Reporting a failure

Create an issue in this repository. Use one issue per distinct defect and link it in the shop coverage table.

```text
Title: [v1.7.2] [unit/area] Short description
Version / commit:
FiveM build / client channel:
Unit and entrance (or coordinates):
Camera position / approximate distance / direction:
Time and weather:
Graphics settings / visual mods:
Players and other map resources involved:
Steps to reproduce:
Expected result:
Actual result:
Reproduces after a fresh connection? Always or intermittent?
Screenshot/video (include an establishing view, then a close-up):
F8/server error or crash timestamp, if relevant:
Performance baseline and measurements, if relevant:
```

Do not attach credentials or unredacted server configuration files.

## 12. Completion

- [ ] Every unit has a recorded result in the coverage table; any untested category has an explicit reason.
- [ ] Both priority regressions pass from multiple angles, distances and clients.
- [ ] Blocking issues are resolved and retested; remaining cosmetic issues have linked tickets.
- [ ] Audio, performance and restart/reconnect checks are recorded.
- [ ] Test props are removed and temporary audio/weather/debug changes are restored.
- [ ] Record the tested version, testers, date and any accepted limitations before calling the build fully verified.
