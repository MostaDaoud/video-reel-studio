# Ecosystem — where this fits, and what we deliberately don't include

Four projects come up constantly when people look for "agent video". They solve different problems than this one, and three of them are worth pointing at. None of their code is vendored here, and this page says why.

| Project | What it actually is | License | Relationship to us |
|---|---|---|---|
| [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 66 code-drawn film **styles**, each a `STYLE.md` + a demo film, plus `DIRECTOR.md` and `TECHNIQUE.md` | MIT (code) · CC BY 4.0 (films) | **Art-direction menu.** We have 17 styles and a move bank; they have 66 deeply specified looks. Complementary, not a dependency. |
| [athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos) | **Research + gallery**: 424 source posts, nine-frame sampling, content/style/colour/cost findings | CC BY 4.0 (writing) | **Evidence.** Use it to justify production choices, not to render anything. |
| [0xsline/OpenChatCut](https://github.com/0xsline/OpenChatCut) | Local-first **editor** with a real multitrack timeline, transcript editing, and an MCP server agents can drive | AGPL-3.0 | **Manual-edit escape hatch.** We ship a finished MP4; they ship an editable project. Different last mile. |
| [clonn/awesome-agent-video-skills](https://github.com/clonn/awesome-agent-video-skills) | **Directory** of 184 agent video skills, with licence and safety cards | MIT | **Distribution.** Where this repo should be listed, and a good map of neighbours. |

---

## 1. Lemo-Opuscar — the style library we are not

**What it does well.** Sixty-six fully specified film styles, each with a prompt and a demo made entirely in code by an agent — no video model. The style prompt describes palette, type, camera grammar, rhythm and sound. `DIRECTOR.md` covers directing, `TECHNIQUE.md` covers frame-by-frame rendering.

**Why we don't merge it.** Their pipeline is their own engine; ours is built on the five `video-ad-editor` skills. Bolting 66 styles onto our scene grammar would mean rewriting both.

**What we can take, honestly.**
- A **style shortlist** for our `35_moves.py` board: when a client asks for "watercolour", "Swiss", "blueprint" or "paper-cut", their `STYLE.md` is a better brief than anything we'd improvise.
- Their **"make a style your own"** flow (safe to change / changes character / can't change) is the same instinct as our brand onboarding — worth copying as *thinking*, not as files.

**Rule if we ever quote them:** films are CC BY 4.0, so any frame we show needs credit to LemoLab with a link; the code is MIT. We currently link only.

---

## 2. Awesome Claude 5.5 Videos — evidence, not a toolkit

**What it does well.** It samples 424 real source posts and measures them: content domain × visual style, palette splits, production paths, reported task cost. It separates "what a preview shows" from "what the author claims", which is rarer than it should be.

**Two findings that support decisions we already made:**
- **71.6%** of ad/launch files are motion-graphics/UI, and **70.0%** of game/interactive files are 3D — i.e. the format follows the job, not the fashion.
- Motion-graphics work splits roughly **198 dark-neutral vs 152 light-neutral** among 350 files — a single "average palette" would be a mistake, which is exactly why our brand onboarding asks for colours up front instead of defaulting.

**Why we don't import it.** It's a study and a link index. Its value is in the claims, and claims need attribution.

**Rule:** CC BY 4.0 — quote with credit and a link; never lift their charts into our marketing without attribution.

---

## 3. OpenChatCut — the edit we hand over, not the edit we render

**What it does well.** A real timeline (tracks, transitions, keyframes, LUTs), transcript-driven cutting, captions, motion-graphics templates, WebGL effects, and an **MCP endpoint** so Claude Code or Codex can edit a project through validated, undoable commands. Projects stay local and stay editable.

**Where we differ.** Our output is a *decision*: a finished, gated MP4 for a feed. Theirs is a *workspace*: a project a human keeps editing. That is a different product, and pretending otherwise would hurt both.

**The one integration that makes sense.** A hand-off: when a client says "I want to fix the cut myself", we currently point at `40_capcut.py` (CapCut draft). OpenChatCut is the open alternative and speaks MCP, so a future adapter could push our `cut.json` + `caps.json` into its timeline. **Not today** — and if we build it, it must be an MCP client in our repo (MIT), never a fork of their AGPL code.

**Licence note:** AGPL-3.0 is copyleft over the network. Calling a separately installed OpenChatCut over MCP is not linking; copying its code into this repo would relicense everything here. We link.

---

## 4. Awesome Agent Video Skills — where to be found

**What it does well.** 184 repositories in 10 categories, each with an install line, licence and a safety note, plus guides on choosing a stack. It is English-first and explicitly says the install text was **not executed** by the maintainers — an honesty we respect.

**Why it matters to us.** Our category ("Short-form & talking-head", and partly "Editing & post-production") is exactly where a person looking for this repo would browse. A card there is worth more than another badge here.

**Action:** submit a card describing this skill — one prompt, nine gates, Arabic-first, Windows + macOS — with our licence and the honest limitation that podcast mode needs two cameras.

---

## What we are not adding, and why

- **No vendored styles, films or charts.** Three different licences (CC BY, AGPL, MIT) and none of them need to live in this tree.
- **No "one repo to rule them all" list.** There are already two good directories; a third would be noise.
- **No adapter we haven't run.** A half-working OpenChatCut bridge would damage the one claim this repo makes: that a gate either passes or it doesn't.

## If you are choosing between us

| You want | Use |
|---|---|
| A finished, gated vertical video from one sentence, Arabic captions, brand consistency | **this repo** |
| A specific art-directed look from a catalogue of 66 | Lemo-Opuscar, then bring the brief here |
| To keep editing a timeline by hand, with an agent beside you | OpenChatCut (or CapCut via `40_capcut.py` today) |
| To browse what agents can do in video at all | the two awesome lists |

---

## Appendix — scan of our two categories (56 repos)

**Method, stated plainly.** I read the two catalogue pages of
[awesome-agent-video-skills](https://github.com/clonn/awesome-agent-video-skills) that this repo would sit in —
*Short-form & talking-head* (19) and *Editing & post-production* (37). **56 rows total.** I judged each repo from its
**one-line catalogue description only**; I did not open the repos. Anything below is "stated", not "verified".

### What the 56 look like

| | count |
|---|---|
| state some form of check, review or approval | **10** |
| non-commercial licence (PolyForm-NC / CC-BY-NC) | **6** |
| **no licence file at all** (default copyright — not free to use) | **7** |
| MIT / Apache-2.0 / AGPL-3.0 | 41 |

So in the exact categories where this skill competes, **13 of 56 are not usable in client work** without asking the author.

### The ten that check something

| repo | ★ | licence | what it states | closest to us |
|---|---:|---|---|---|
| [YeJe-cpu/SeeCut](https://github.com/YeJe-cpu/SeeCut) | 260 | **NC** | "checks its own output with a video model" | **G4b** — but model judgement, not a threshold |
| [Fagan1024/smart-video-editor](https://github.com/Fagan1024/smart-video-editor) | 9 | MIT | "analyses sampled frames with a vision model, drops unusable takes" | **G4b** visual audit |
| [krusemediallc/video-editor-agent](https://github.com/krusemediallc/video-editor-agent) | 26 | **none** | "frame-level QA" | **G4** frames |
| [erduo1998-cell/erduo-broll-loop-engineering](https://github.com/erduo1998-cell/erduo-broll-loop-engineering) | 209 | MIT | "multi-role review loops" | our fresh-context audit |
| [qingyunAGI/qingyun-cine-skill](https://github.com/qingyunAGI/qingyun-cine-skill) | 10 | **none** | "rendering only after user approval" | gate hold before render |
| [PoetCoderJun/MotionTalk](https://github.com/PoetCoderJun/MotionTalk) | 12 | **NC** | "after the user approves a director plan" | gate hold before render |
| [jaxxchen003/book-video-factory](https://github.com/jaxxchen003/book-video-factory) | 105 | MIT | "auditable evidence, approvals" | evidence trail |
| [yuwenbin121/book-video-production-skill](https://github.com/yuwenbin121/book-video-production-skill) | 17 | MIT | "fact-checked" | content gate |
| [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | 347 | MIT | "export checks" | **G6** package |
| [Samin12/samin-reel-engine-plugin](https://github.com/Samin12/samin-reel-engine-plugin) | 9 | custom | "editing and review" | vague |

### Opened the three closest — what the check actually is

| repo | verdict | evidence from its README |
|---|---|---|
| [krusemediallc/video-editor-agent](https://github.com/krusemediallc/video-editor-agent) | **mechanical** | "edits ... **QA'd frame by frame and in dB**"; its engine "verifies the RENDERED file (frames + dB + seams)"; storyboard coverage; *"unavailable checks are not labeled a clean pass"* |
| [YeJe-cpu/SeeCut](https://github.com/YeJe-cpu/SeeCut) | **hybrid** | "each version **first passes hard-defect checks**, then pairwise-compares against the previous"; calibrated judge, positions swapped, max 3 versions, must show visible improvement |
| [Fagan1024/smart-video-editor](https://github.com/Fagan1024/smart-video-editor) | **model judgement** (selection, not delivery) | per-frame vision scoring → EDL. One objective check in the whole repo: a font-fallback **PSNR** test, after a vision model mis-read a font |

### Correction — my first sentence was wrong

The appendix above first said *"none states machine-checkable thresholds."* That is **wrong** for krusemediallc and too
strong for SeeCut. Both check the rendered file with numbers.

What survives is narrower, and now defensible:

> At least one neighbour runs a mechanical QA pass on the rendered MP4 — frames, dB, seams — and refuses to call a
> skipped check a pass. The difference here is **which gates**, not **whether gates**: Arabic caption timing and
> bidi, brand contrast ratios, safe-zone raster diff against Instagram's chrome, package size, environment readiness —
> plus Windows support and an open licence.

**The licence still bites:** krusemediallc has **no licence file** (all rights reserved by default), SeeCut is
**non-commercial**, Fagan is **MIT**. So of the three, only Fagan's ideas are safely borrowable — and its best idea is
already in our vocabulary: *test the thing mechanically when a model's judgement is the unreliable part.*

**Still true across all three:** none mentions Arabic, RTL or bidi. All three assume a single-script pipeline where
caption timing is a solved problem. That is where this repo is actually alone.

### Caveat that stays attached

Even now this is a README-level audit of three repos, not a code review. A claim like "verifies frames + dB + seams"
is the author's description of their own engine; it was not executed here.
