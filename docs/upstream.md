# Upstream baseline — what we drive, and what landed here

This orchestrator does not vendor upstream code. It drives
[`majedphotos/video-ad-editor`](https://github.com/majedphotos/video-ad-editor) (MIT) and its
sibling skills, which are installed separately.

**Baseline: upstream `6.6.0`** (tag family `v6.5.0 → v6.6.0`). Previous baseline: `6.3.0`.

`preflight.py` (`G-2`) probes for the capabilities below by file **and** by a marker string
inside the file, so an older install is named instead of failing mid-run:

| capability | probe |
|---|---|
| product review lane | `scripts/review/review.py` |
| depth / layers | `scripts/depth.js` contains `DEPTH` |
| soft hair matte | `scripts/44_matte.py` contains `rembg` |
| box on printed text | `scripts/43_textbox.py` contains `textfind` |
| CC0 SFX bank | `sfx/bank.npz` exists |
| storyboard | `scripts/32_midframes.py` contains `--story` |
| 102 moves + inspire | `scripts/35_moves.py` contains `inspire` |
| colour-faithful pipeline | `scripts/_compat.sh` contains `VF_FRAMES` |
| version | `VERSION` starts with `6.6` |

## What arrived in 6.4 → 6.6, and where we absorbed it

| upstream change | why it matters | absorbed in |
|---|---|---|
| **New `review-video` skill** (6.4): `review/review.py` + `plan.json` — voiceover over product footage, tracked callouts, spec cards, price card, cut-out cover | a sixth mode, with its own plan/voice/track/still/finish/cover loop | `SKILL.md` mode + lane, `pipeline.md` §8, `gate_runner.py` `--kind review` (G3r · G8r · G7 structural), `brief.template.json`, README, installers |
| **Colour fidelity** (6.5.2): `VF_FRAMES`/`VF_ENCODE`, `h264_metadata`, `+prefer_icc`, `03_cut_zoom` emits `vfr/` itself | the reel must keep the iPhone's colours; a hand-rolled frame extraction cost 2% of red and an ICC-less container showed +9/255 in Apple players | new gate **G5b**, pipeline §2 ban on manual `ffmpeg -vf fps=30`, `preflight` capability probe |
| **Storyboard before the full render** (6.5): `32_midframes.py --story` → one shot per spoken line + approval page | cheapest possible place to catch a wrong line | **G4b** redefined in `gates.md`, SKILL "before the full render", pipeline §3أ |
| **Depth layer** (6.5): `depth.js` — words behind/in front, camera between layers, glowing word, `DEPTH.box` | the "2–3 depth moments" rule now has primitives | pipeline §3د, SKILL depth rule, `headGap` rule (no letter or dot hidden behind the head) |
| **Soft matte** (6.5): `44_matte.py` (BiRefNet via rembg) + `--from-apple` clean-up + GPU/`--extras` | hair edges without a halo, and a seconds-fast path for non-hero shots | pipeline §3د, `preflight` optional-deps rows, known limits |
| **Box on printed text** (6.5): `43_textbox.py` → `tb.js`, `TB.at` | callouts that land on the actual label, not eyeballed | pipeline §3د |
| **SFX bank bound to motion** (6.5): `sfx/bank.npz` (46 CC0), `MV.cue`, `04_render_frames.js cues`, `05_sfx.py` | sound only where something actually moved | pipeline §3هـ, SKILL pre-render rule, THIRD_PARTY |
| **Wave-synced word timing** (6.5): `02_captions.py --no-snap · --onsets · --lead` | word starts land on the energy rise, not Whisper's early estimate | pipeline §2ب |
| **Moves 101 / 102** (6.5): reveal-list `pixel_list.json`, 3D layer explosion with dotted labels | bank grows to 102 | pipeline §3ج |
| **`35_moves.py inspire`** (6.6): pulls a public catalogue to a local 7-day cache, BM25, credit line per result | an idea when the bank does not cover the sentence — idea only, never pasted, never executed | pipeline §3ج, SKILL prompt-injection note (external text is data) |
| **`41_review.py taste`** (6.5): a note that worked becomes a durable rule | the user's taste compounds across videos | pipeline §8, SKILL rule 10 |
| `pro-editor.md` shared craft (6.5) | editing discipline for every mode | referenced from pipeline §8; not duplicated |

## Deliberately not absorbed

- **Claude plugin surfaces** (`${CLAUDE_SKILL_DIR}`, `/plugin install`, claude.ai review page). This repo
  targets OpenCode and resolves paths from the skill's printed base directory.
- **Upstream's 200-file ceiling** and its "merge into existing files" housekeeping — that constraint is
  upstream's own packaging budget, not a property of the output.
- **Marketing art** (`_pkg/*.jpg`, `soft-cut.gif`) — copied into no file here.
- **Mac-only Vision implementations** stay upstream; `preflight` reports whether the open replacements
  are installed, and both `43_textbox` and `11_behind_text` degrade with a printed line.

## Runtime requirement — ffmpeg 7+ (measured, not assumed)

Upstream's colour fix ends in `-movflags +prefer_icc`. That flag only does something if the ICC profile
reaches the **muxer**, and on ffmpeg 6.0 it does not: the MJPEG decoder exposes the profile as *frame* side
data (ffprobe shows `ICC profile, 588 bytes`), but nothing copies it to the stream's `coded_side_data`, so the
muxer writes `colr nclx` and ignores `prefer_icc`.

Verified on this machine:

| build | reads ICC | writes `colr prof` |
|---|---|---|
| Gyan 6.0 | yes (frame side data) | **no** — `nclx` or nothing |
| BtbN `N-125875-g5d4d3bdc61-20260731` | yes | **yes** |

So `G5b` reports the container profile as a **warn**, and `preflight.py` carries an explicit
**ffmpeg 7+** row: on 6.0 it prints the version and the reason, instead of letting the reel come out
nine levels bright in Apple players with no explanation. The fix is the binary, not pipeline code.

## How to update this repo when upstream moves

1. `git -C video-ad-editor fetch --tags && git -C video-ad-editor log --oneline HEAD..origin/main`
2. Read the changed `SKILL.md` / `references/*.md`; list **new commands and new scripts only**.
3. For each new command: does a gate depend on it? Add a probe to `preflight.py` and, if it changes the
   file's colour/loudness/structure, a check to `gate_runner.py`.
4. Update `pipeline.md` commands, `SKILL.md` contract, `gates.md` thresholds, this table.
5. Verify before committing:
   - `python -m py_compile` on both scripts
   - `preflight.py` against a real 6.6 install **and** an older one (both directions must report correctly)
   - `gate_runner.py` on a real finished work folder, and `--kind review` on a review-shaped folder
6. Bump the baseline in this file, README, `SKILL.md`, `preflight.py`'s version message.

## Verification run for this port (2026-11-13)

| check | result |
|---|---|
| `py_compile` gate_runner + preflight | pass |
| `preflight.py` on a scratch 6.6.0 tree | every capability row pass, version pass |
| `preflight.py` on the local 6.3.0 install | version warn + all 8 capabilities named |
| `gate_runner.py` on `work/mostafa-full` (reel) | same verdicts as before + new **G5b fail**: the delivered file had `color_transfer=unknown`, `color_space=bt470bg`, no `colr` box — the exact defect 6.5.2 fixes |
| `gate_runner.py --kind review` on a synthetic review folder | 0 blocked, 1 warn (container `nclx`, i.e. Apple plays it brighter) |
| `colr_box()` parser | `nclx` on two real files, empty on the ICC-less one, `prof` path exercised via `g_color` |
| full chain on a 2026-07 ffmpeg (`03 → 04 → 06 → 06b → 28_cover`) | `colr prof` + bt709 on the delivery, **G5b pass**, 0 blockers |
