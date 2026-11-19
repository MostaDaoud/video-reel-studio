# Build log — what broke, and how it was proved fixed

Every entry comes from a real build in this repo, not a hypothetical. The pattern is the same each
time: a gate or a viewer caught something, the first explanation was often wrong, and the fix only
counted once it was re-measured.

---

## 1. “The film is 30 s but the old end card paints itself over 7–30 s”

`compose.REFERENCE.html` computes `DUR = caps.total + outro`, and `outro` starts at `caps.total`.
So `caps.total` is not “when captions end” — it is **the length of the body**. Setting it to the end of
the last caption (7 s) told the renderer the film was 7 s long and let the outro fill the rest.

**Fix:** `caps.total` = film duration. With that, the outro starts at the end, where it belongs.

**Lesson:** a field named `total` in a captions file is not necessarily about captions.

---

## 2. “The last caption card sticks” — it did not

Symptom: a caption pill visible at 9 s, over the motion chapter, long after its card ended.

First diagnosis (wrong): the renderer keeps the last card. Written up as an engine defect.

Actual cause: `_chunks()` adds a **0.6 s hold** to the final chunk, so a card ending at 6.98 s is
painted until 7.58 s — straight across a chapter cut at 7.0. Nothing was stuck; the hold was doing
what it says.

**Fix:** an explicit caption stop for a film whose captions end with the voice, plus a real guard so
bad data cannot bleed: every card is clamped to `[0, VEND]` and every word to its card at load, and
`caption()` / `capChunk()` return at `t >= VEND`.

**Verification:** disable the explicit stop, re-render 9.0 s, confirm the pill is gone; re-enable,
re-render 6.8–10.2 s, confirm the delivered frames come back byte-identical.

---

## 3. `06c_loudfix.sh` was wrong four ways at once

It printed a green success line while missing every target: `colr nclx` instead of `prof`, −15.2 LUFS
instead of −14, and a true peak of −0.6 dBTP instead of ≤ −1.5.

Four independent causes — missing `+prefer_icc`, `linear=true` skipping the limiter, one loudnorm pass
falling short on compressed speech, and `-ar` resampling after the limiter. Full chain and numbers in
[`patches/README.md`](../patches/README.md).

**Lesson:** a tool that reports “✅ done” can be lying. Measure the artefact, not the log line.

---

## 4. Depth: the head has to be smaller than the frame

A word behind the subject only reads if the subject is occluded **and** the word has room around them.
Two failed attempts are worth recording:

- **Auto-layout.** The stack fitter, given a tight talking head, stretched the first word into a
  full-width kashida beam and dropped a stray word at the bottom. Hand-placed type on a cutout stage
  beat it.
- **Person scale.** `cutout` restages from the mask bounding box, so the head lands at
  `1950 − TARGET_H`. With `TARGET_H = 760` and a 1920 frame the head sits at 1190 — type coordinates
  have to be derived from that, not guessed.

**Platform constraint:** the safe-zone gate measures the bottom band (y 1620–1920) because that is
Instagram's caption tray. A third text plane “in front of the chest” lands there by construction
(3.07 % vs a 0.20 % allowance). On a tight framing, two planes is the honest maximum.

---

## 5. A safety gate improved the composition

The right-side rail check failed at 6.38 %: a 470 px digit at `x = 866` reached into the like/comment
rail. Moving the pair inward to 315/765 cleared the rail **and** gave both digits a real occlusion
edge against the head. The fix was better than the original.

---

## 6. The 4K source has letterbox bars baked in

`cropdetect` said the image was `3840×2024` at `y=68`, not `3840×2160`. The obvious 9:16 crop
(`1215×2160`) therefore kept a 20 px black bar top and bottom, which survives scaling and reads as a
defect on a phone. The correct crop is `1138×2024` at `x=1351`.

**Lesson:** crop from what `cropdetect` reports, not from what `ffprobe` reports.

---

## 7. The transcription language flag matters more than the model

`faster-whisper` on a take that mixes English with Arabic code-switching, with `language="ar"`,
produced «لقد فعلت so much» — an Arabic hallucination over an English phrase. The same 60-second
window with `language="en"` produced the real sentence.

**Rule:** choose the language per clip, not per project, and read the transcript before trusting it.

---

## 8. Five words in a caption card leaves a one-frame flash

compose splits caption cards at four words. A hand-written five-word card became 4 + 1, and the last
word sat alone for 0.27 s. Grouping by phrase instead (`just remembering` / `everything I did`) removed
the flash without changing a single timestamp.

---

## 9. A cover shot from the master carries the master's UI

`28_cover.py` photographs the delivered file, so the HUD, the caption pill and the progress bar end up
inside the cover. Shooting the clean base (`--video base14.mp4`) gives a plate with nothing on it.

---

## 10. The repo caught its own false claim

A post caption said three modes had no footage. But `assets/video/montage.mp4` had been in the repo —
and on the landing page — the whole time. The real gaps were podcast and product review.

The claim was corrected in the caption before publishing. A showcase that overstates is worth less
than one that is checkable.

---

## What is still missing

**Product review** is the only mode with no footage anywhere in this repo. The shot spec is 10 s on a
table, 10 s of detail passes, 10 s in use, 5 s clean hero, no talking — the mode adds tracked callouts
and a voiceover. Until that exists, the roster names it and nothing pretends otherwise.

---

## 11. The caption style assumed every caption was Arabic

The `chunk` style anchors the first word at the **right** edge and walks left. That is correct for Arabic
and reverses every Latin caption: an English card reading “content that” rendered as “that content”.

Found on the first English build in this repo. The first preview looked like a typo in the caption data;
it was the layout. The patch picks the direction from the text itself — a capsule containing Arabic
codepoints keeps RTL, everything else lays out LTR — so the Arabic-first case the style was written for
is unchanged. See [`patches/compose-ltr-captions.patch`](../patches/compose-ltr-captions.patch).

**Lesson:** "Arabic-first" is a design decision, not a licence to hardcode direction in a renderer.

