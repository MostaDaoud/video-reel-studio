# Local engine patches

Baseline: upstream **6.6.0**. Four defects are patched in the installed engine and verified on the
showcase builds in this repo. Each file here is a unified diff against the 6.6.0 source.

Apply from the skill root (the folder that contains `scripts/`):

```bash
cd ~/.claude/skills/video-ad-editor      # or wherever the skill is installed
git apply /path/to/patches/06c-loudfix.patch
git apply /path/to/patches/compose-reference.patch
git apply /path/to/patches/04-render-frames.patch
# without git:
patch -p1 < /path/to/patches/06c-loudfix.patch
```

## What each one fixes

| patch | file | symptom without it |
|---|---|---|
| `06c-loudfix.patch` | `scripts/06c_loudfix.sh` | writes `colr nclx` (Apple plays it brighter), lands ≈ −15.2 LUFS instead of −14, and lets the true peak hit −0.6 dBTP |
| `compose-reference.patch` | `scripts/compose.REFERENCE.html` | a caption can paint past its own card and past `VEND`, over the next chapter |
| `04-render-frames.patch` | `scripts/04_render_frames.js` | renders fewer frames than the base video and says nothing |

## Why `06c` needed four changes

It reported success while missing every target:

1. `-movflags +faststart` without `+prefer_icc` drops the container profile.
2. `linear=true` applies gain only and skips the true-peak limiter.
3. One dynamic `loudnorm` pass lands ~1.2 LU short on compressed speech.
4. `-ar 48000` on the output resamples **after** the limiter and raises the peak again.

The patched chain is:

```
aresample=48000 → acompressor(3:1 @ −20 dB) → loudnorm ×2 → aresample=48000
→ alimiter(limit=0.85, level=disabled) → +faststart+prefer_icc
```

`level=disabled` matters: `alimiter` auto-levels by default, which *raises* the signal to the ceiling.

## Verification

On `showcase-30/ad-final.mp4`, patched `06c` returns:

```
−14.65 LUFS · −1.50 dBTP · 48 kHz · colr prof
```

The camera colour gate (`G5b`) is the one that catches the old behaviour: it fails an `nclx` file for
the right reason.

These patches are written against 6.6.0. If upstream moves, hunks may drift — `git apply --3way` or
`patch -p1 --fuzz=3` will usually still land them.
