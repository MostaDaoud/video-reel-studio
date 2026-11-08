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
