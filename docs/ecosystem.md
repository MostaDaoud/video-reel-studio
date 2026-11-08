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

**Action:** submit a card describing this skill — one prompt, ten gates, Arabic-first, Windows + macOS — with our licence and the honest limitation that podcast mode needs two cameras.

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
**one-line catalogue description only**; I did not open the repos in this pass. Anything below is "stated", not "verified".
**Superseded:** the full audit further down opens all 184 repos one by one and decides each.

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

---

## Full audit — all 184 repositories, opened one by one

**What changed from the appendix above.** The 56-repo scan judged from one-line descriptions. This section opens
every README in the catalogue: 184 repositories, fetched at `HEAD/README.md` (falling back to `main`, `master`, and
nine filename variants). **181 downloaded, 3 return 404** — deleted, renamed or made private upstream.

Each verdict answers one question only: **does this change what we build?**

| verdict | meaning |
|---|---|
| **add** | something was taken into the skill in this commit |
| later | worth taking, blocked on something we do not have yet — the blocker is named |
| link | kept as a reference; nothing changes here |
| skip | out of scope, licence unusable, dead, or a duplicate |

### The numbers

| | count |
|---|---:|
| add | 8 |
| later | 4 |
| link | 125 |
| skip | 47 |
| **total** | **184** |

Of the 184: **27 have no licence at all** (default copyright — not legal to copy from), **7 are explicitly non-commercial**, and **3 no longer exist.**

So the catalogue is a good map but a poor shopping list: **34 of 184 rows cannot be used in paid client work** without asking the author.

### What was actually added

| from | what we took | where it landed |
|---|---|---|
| [YeJe-cpu/SeeCut](https://github.com/YeJe-cpu/SeeCut) | absolute scores are unreliable; compare two versions with the positions swapped | `references/gates.md` rule 1 |
| [erduo1998-cell/erduo-broll-loop-engineering](https://github.com/erduo1998-cell/erduo-broll-loop-engineering) | re-render only the affected shot, and recheck the seams it touches | `references/gates.md` rule 2 |
| [tugrawork-creator/saas-motion-kit](https://github.com/tugrawork-creator/saas-motion-kit) | audit the storyboard for repetition before building | `references/gates.md` rule 3 |
| [BusyBee3333/animated-explainer-skills](https://github.com/BusyBee3333/animated-explainer-skills) · [GordenSun/react-bits-video](https://github.com/GordenSun/react-bits-video) | no overlapping text blocks; per-element contrast against its own background | `references/gates.md` rule 4 |
| [aijiduonadegou/Paper-Cut](https://github.com/aijiduonadegou/Paper-Cut) | black-frame and first-frame QA | **gate G4c** in `gate_runner.py` (`blackdetect`) |
| [Mr-funny/hbg-douyin-code-explainer-video](https://github.com/Mr-funny/hbg-douyin-code-explainer-video) | −20.5 LUFS for Douyin | `LOUD` table, `--platform douyin` |
| [sukai213/bilibili-ai-video](https://github.com/sukai213/bilibili-ai-video) | −16 LUFS for Bilibili | `LOUD` table, `--platform bilibili` |
| [Mr-funny/hbg-life-simulation](https://github.com/Mr-funny/hbg-life-simulation) | −22.8 LUFS, near the −23 broadcast reference | `LOUD` table, `--platform cinema` |

G4c and the platform targets are proven, not asserted: prepending one second of black to the finished reel makes
G4c fail with `الفيديو يبدأ أسود عند 0.00 ث (1.00 ث)`, and the same file passes `--platform ig` while warning as
`علو -14.1 LUFS (هدف douyin -20.5 ±1.2)` for Douyin.

### Deferred, with the blocker named

| from | idea | blocked on |
|---|---|---|
| [Fagan1024/smart-video-editor](https://github.com/Fagan1024/smart-video-editor) | PSNR check that the font actually applied — a vision model cannot see a fallback | needs a per-font reference render |
| [smwbev/framewright](https://github.com/smwbev/framewright) | determinism: the same frame from the same inputs, twice | needs a render-twice hook in `video-ad-editor` |
| [AmazingAng/ccvideo](https://github.com/AmazingAng/ccvideo) | rebuild props from raw artifacts and fail on mismatch | needs an asset/props manifest pipeline |
| [Finderchangchang/promo-video-skill](https://github.com/Finderchangchang/promo-video-skill) | ad-law checks on the copy | needs a claims list per market |

### The decision table

Sorted by upstream category, then stars. `★` and licences are from the catalogue's snapshot (2026-10-10).

#### AI Avatars (5)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [cclank/lanshu-create-ai-presenter-video](https://github.com/cclank/lanshu-create-ai-presenter-video) | 2.6k | MIT | link | Presenter pipeline; its table states −16 LUFS ±0.5 and TP ≤ −1 dBTP. Avatar route is outside what we produce. |
| [heygen-com/skills](https://github.com/heygen-com/skills) | 473 | MIT | link | HeyGen API skills — a provider, not a mechanism. Useful only if a project asks for an avatar. |
| [Upload-Post/avatar-mix](https://github.com/Upload-Post/avatar-mix) | 131 | MIT | link | Avatar + captions + auto-publish. The publish step is the one thing we deliberately do not do. |
| [AgriciDaniel/lipnardo](https://github.com/AgriciDaniel/lipnardo) | 22 | Other | skip | Batch/template CLI wrapped around the HeyGen API; nothing transferable. |
| [zlong6943-commits/football-prediction-avatar-video](https://github.com/zlong6943-commits/football-prediction-avatar-video) | 9 | **none** | skip | Niche football-prediction avatar skill, Chinese-only, and no licence file (all rights reserved). |

#### Editing & Post-production (37)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [FireRedTeam/FireRed-OpenStoryline](https://github.com/FireRedTeam/FireRed-OpenStoryline) | 3.5k | Apache-2.0 | link | Conversational editing agent on its own runtime. Apache-2.0, so readable, but adopting it means adopting its stack. |
| [Agentchengfeng/chengfeng-videocut-skills](https://github.com/Agentchengfeng/chengfeng-videocut-skills) | 3.0k | Apache-2.0 | skip | Installer only; the actual runtime lives in a different repo. |
| [0xsline/OpenChatCut](https://github.com/0xsline/OpenChatCut) | 2.2k | AGPL-3.0 | link | Already assessed in this doc: MCP-driven timeline editor, AGPL. |
| [cartesiancs/cartcut](https://github.com/cartesiancs/cartcut) | 803 | MIT | link | Desktop editor exposing its timeline over MCP. We have no GUI to attach it to. |
| [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | 669 | MIT | link | 283 Premiere tools behind one bridge. Relevant only for Premiere-first clients. |
| [JimLiu/baocut](https://github.com/JimLiu/baocut) | 601 | Other | skip | Drives a closed macOS app; not portable to Windows. |
| [zenstory-ai/video-recap-skills](https://github.com/zenstory-ai/video-recap-skills) | 561 | MIT | link | Chinese narration recaps with optional JianYing draft export. |
| [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | 347 | MIT | link | Premiere MCP that explicitly includes export checks. |
| [hassancs91/claude-youtube-editor](https://github.com/hassancs91/claude-youtube-editor) | 327 | MIT | link | Recording → Remotion screen visuals → YouTube upload, end to end. |
| [YeJe-cpu/SeeCut](https://github.com/YeJe-cpu/SeeCut) | 260 | Other · NC | **add** | Adopted the audit rule: absolute scores are unreliable, pairwise with swapped positions is not. Non-commercial, so idea only. |
| [AgriciDaniel/claude-shorts](https://github.com/AgriciDaniel/claude-shorts) | 219 | MIT | link | Preflight checks input, disk and GPU before cutting — same shape as our G-2. |
| [erduo1998-cell/erduo-broll-loop-engineering](https://github.com/erduo1998-cell/erduo-broll-loop-engineering) | 209 | MIT | **add** | Adopted: when one shot changes, re-render only the affected media and recheck the seams it touches. |
| [blixvip/easyedit](https://github.com/blixvip/easyedit) | 154 | MIT | skip | Repository returns 404 (deleted, renamed or private). |
| [znyupup/ai-video-editing-skill](https://github.com/znyupup/ai-video-editing-skill) | 150 | MIT | link | Travel vlog cut from vision analysis + Whisper, with browser preview. |
| [naive-kun/naive-video-skill](https://github.com/naive-kun/naive-video-skill) | 132 | MIT | link | Talking-head workflow with HyperFrames + GSAP preview before the final render. |
| [ayushozha/AdobePremiereProMCP](https://github.com/ayushozha/AdobePremiereProMCP) | 120 | MIT | link | States its verification boundary and checks mutations by timeline/DOM readback. Good discipline, wrong host. |
| [Cassette-Editor/oh-my-cassette](https://github.com/Cassette-Editor/oh-my-cassette) | 119 | MIT | link | Beat-synced cut of a clip folder; its README claims OpenCode support. |
| [Monet-AI-Editor/Monet](https://github.com/Monet-AI-Editor/Monet) | 117 | MIT | link | macOS-only editor with an embedded terminal; breaks our Windows parity. |
| [louisedesadeleer/cut-video](https://github.com/louisedesadeleer/cut-video) | 108 | MIT | link | Recommends trim+concat because ffmpeg select misaligns audio. Checked: our 03_cut_zoom.py already uses trim/atrim + setpts/asetpts. |
| [AKMessi/vex](https://github.com/AKMessi/vex) | 87 | Other · NC | link | Terminal editing agent, 51 check mentions, source-available non-commercial. |
| [JUNKDOGE-JOE/after-effects-mcp](https://github.com/JUNKDOGE-JOE/after-effects-mcp) | 78 | MIT | link | After Effects CEP bridge, ~30 tools. Only for AE users. |
| [kurbaitaev/ghost-editor](https://github.com/kurbaitaev/ghost-editor) | 66 | MIT | link | Reels from a talking head with reference-edit imitation. |
| [hahadu4520/vlog-cut](https://github.com/hahadu4520/vlog-cut) | 49 | Other · NC | skip | Non-commercial, Chinese vlog pipeline. |
| [ops120/video-recap-skills-plus](https://github.com/ops120/video-recap-skills-plus) | 41 | MIT | link | Recap fork with Jianying export; documents the libass requirement for burned subtitles. |
| [darrenli6/JJKoubo](https://github.com/darrenli6/JJKoubo) | 37 | Other · NC | skip | Non-commercial licence. |
| [Kappaemme-git/codex-video-short-maker-skill](https://github.com/Kappaemme-git/codex-video-short-maker-skill) | 35 | MIT | link | Dead-air removal, vertical export, local Whisper captions. |
| [krusemediallc/video-editor-agent](https://github.com/krusemediallc/video-editor-agent) | 26 | **none** | link | Best neighbour on our axis: QA's the rendered file frame by frame and in dB. No licence file, so nothing importable. |
| [manthanpatelll/leadgenman-video-skills](https://github.com/manthanpatelll/leadgenman-video-skills) | 17 | MIT | skip | Repository returns 404. |
| [jincheng2026/jc-remotion-skills](https://github.com/jincheng2026/jc-remotion-skills) | 14 | Other · NC | skip | Non-commercial licence. |
| [cocolayuan/videoclip-AI-skill](https://github.com/cocolayuan/videoclip-AI-skill) | 13 | MIT | link | Flags filler and silence, cuts with FFmpeg, keyword-highlighted subtitles. |
| [ZiadAbdelkarim/beat-synced-edit](https://github.com/ZiadAbdelkarim/beat-synced-edit) | 13 | MIT | link | Beat analysis → cut points, as a standalone tool. |
| [misbahsy/tiktok-ig-shorts](https://github.com/misbahsy/tiktok-ig-shorts) | 12 | **none** | skip | Repository returns 404; no licence file on record either. |
| [PoetCoderJun/MotionTalk](https://github.com/PoetCoderJun/MotionTalk) | 12 | Other · NC | link | Holds at an approved director plan before adding motion — same hold we do at G1. |
| [qingyunAGI/qingyun-cine-skill](https://github.com/qingyunAGI/qingyun-cine-skill) | 10 | **none** | link | Plan-first cinematic edit; its QC section lists loudness and true peak. No licence file. |
| [Fagan1024/smart-video-editor](https://github.com/Fagan1024/smart-video-editor) | 9 | MIT | later | Idea worth taking: verify the font actually applied (PSNR diff) because a vision model cannot see a fallback. Needs a per-font reference render first. |
| [hahadu4520/newcut-video-clipping-skill](https://github.com/hahadu4520/newcut-video-clipping-skill) | 6 | MIT | link | Long video → viewpoint clips with cleaned captions. |
| [jackjls/jtxvideo-skill](https://github.com/jackjls/jtxvideo-skill) | 5 | MIT | link | SRT → reviewed structure → storyboard → HyperFrames. |

#### Explainers & Education (32)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [EverMind-AI/Raven](https://github.com/EverMind-AI/Raven) | 5.3k | Apache-2.0 | link | Two-minute animated film from a repo's git history; a skill inside a larger host. |
| [Alisa0808/vox-director](https://github.com/Alisa0808/vox-director) | 2.2k | MIT | link | Topic → paper-collage explainer; the closest single-prompt pipeline to our motion film. |
| [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | 1.5k | Other · NC | link | Packs QA frames into a 3×4 contact sheet so a review subagent reads one image. Same trick we use; non-commercial. |
| [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill) | 1.2k | MIT | link | Manim best practices. Only relevant when a project is mathematical. |
| [wshuyi/remotion-video-skill](https://github.com/wshuyi/remotion-video-skill) | 394 | **none** | skip | No licence file, and it is a thin Remotion wrapper. |
| [hi-nikola/hand-drawn-explainer-video-nikola](https://github.com/hi-nikola/hand-drawn-explainer-video-nikola) | 374 | Apache-2.0 | link | Hand-drawn explainers via stroke animation or HTML/SVG/GSAP. |
| [shuyicc/MathLens](https://github.com/shuyicc/MathLens) | 357 | **none** | skip | No licence file; Cursor-only; math domain. |
| [Anil-matcha/vox-ai-motion-graphics-generator](https://github.com/Anil-matcha/vox-ai-motion-graphics-generator) | 245 | **none** | skip | No licence file. |
| [runesleo/claude-video-kit](https://github.com/runesleo/claude-video-kit) | 119 | MIT | link | Keeps a pre-render receipt, a review-render and a verify-shorts step — a small audit trail. |
| [sunxiayi/make-blender-education-video-skill](https://github.com/sunxiayi/make-blender-education-video-skill) | 49 | MIT | link | Blender route with frame-exact assembly and final media QA. |
| [znyupup/knowledge-explainer-skill](https://github.com/znyupup/knowledge-explainer-skill) | 45 | MIT | link | Markdown script → Remotion explainer via a CLI. |
| [iart-ai/explainer-video-skills](https://github.com/iart-ai/explainer-video-skills) | 34 | MIT | link | Script / storyboard / render split into separate skills. |
| [vibe-motion/remotion-code-motion-explainer](https://github.com/vibe-motion/remotion-code-motion-explainer) | 33 | MIT | link | Continuous code-driven explainer with a shot component library. |
| [santmun/video-vox](https://github.com/santmun/video-vox) | 32 | **none** | skip | No licence file. |
| [Mr-funny/hbg-douyin-code-explainer-video](https://github.com/Mr-funny/hbg-douyin-code-explainer-video) | 30 | **none** | **add** | States −20.5 LUFS for Douyin and runs a final-video QA pass. Feeds our platform loudness table; no licence file. |
| [Phantomlau3674/voxstylehub-steven](https://github.com/Phantomlau3674/voxstylehub-steven) | 23 | MIT | link | Keeps text and charts deterministic and layers the collage assets. |
| [holy-templar/vox-animated-ad-mcp](https://github.com/holy-templar/vox-animated-ad-mcp) | 20 | AGPL-3.0 | link | One sentence → collage ad, AGPL. |
| [Mng-dev-ai/explainer-video](https://github.com/Mng-dev-ai/explainer-video) | 19 | MIT | link | HTML/GSAP → headless record → merge audio. That is exactly our motion pipeline shape. |
| [aijiduonadegou/Paper-Cut](https://github.com/aijiduonadegou/Paper-Cut) | 18 | MIT | **add** | Adopted: black-frame / first-frame QA — check frames around transitions, head and tail, and run ffmpeg blackdetect on the encode. |
| [cclank/lanshu-html2video-skill](https://github.com/cclank/lanshu-html2video-skill) | 16 | MIT | link | Article → storyboard → 1080p with stated quality gates. |
| [chenyuxiaojin/cyxj-hyperframes](https://github.com/chenyuxiaojin/cyxj-hyperframes) | 16 | MIT | skip | Its own README says maintenance-only. |
| [kakaxi12/vox-director-codex](https://github.com/kakaxi12/vox-director-codex) | 13 | **none** | skip | No licence file, and duplicates vox-director / vox-animated-ad. |
| [ahmdd4vd/MotionCraft](https://github.com/ahmdd4vd/MotionCraft) | 12 | MIT | link | Honest QA table: debug-box overlap checks plus samples from the final export. |
| [ssrajadh/paperview](https://github.com/ssrajadh/paperview) | 9 | Apache-2.0 | link | ppv validate fails a plan before any TTS or render spend — cheap pre-render validation. |
| [Anil-matcha/zack-d-films-ai-video-generator](https://github.com/Anil-matcha/zack-d-films-ai-video-generator) | 7 | **none** | skip | No licence file; bound to the MuAPI platform. |
| [BusyBee3333/animated-explainer-skills](https://github.com/BusyBee3333/animated-explainer-skills) | 7 | MIT | **add** | Adopted the layout rule: no two text blocks may overlap, and each text element needs its own contrast ratio against its own background. |
| [pjecuacion/script-to-video-skill](https://github.com/pjecuacion/script-to-video-skill) | 7 | MIT | link | Topic, script, audio or talking head → one timed HyperFrames composition. |
| [centraltowerlabs/diagram-tour](https://github.com/centraltowerlabs/diagram-tour) | 6 | MIT | link | Codebase → Graphviz diagram → narrated architecture tour. |
| [sukai213/bilibili-ai-video](https://github.com/sukai213/bilibili-ai-video) | 6 | **none** | **add** | Normalises to −16 LUFS for Bilibili — second data point behind our platform table; no licence file. |
| [coding-ax/docvideoer](https://github.com/coding-ax/docvideoer) | 5 | MIT | link | Document → narrated Remotion video with free TTS. |
| [cymcymcymcym/notes-to-video](https://github.com/cymcymcymcym/notes-to-video) | 5 | MIT | link | LaTeX/PDF notes → Manim explainer. |
| [jinjin1/scenewright](https://github.com/jinjin1/scenewright) | 5 | MIT | link | JSON-as-contract between stages plus a script wording lint gate. |

#### Frameworks & Toolkits (29)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 65.9k | AGPL-3.0 | link | Keeps the reviewer as its own skill: schema validation + playbook compliance. Same split we do with fresh-context audit. |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 59.9k | Apache-2.0 | link | The render engine we already run on. Its CLI does scaffold, lint, preview and render. |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | 20.6k | Other | link | Word-anchored workflow that spins many variants; cloud-oriented. |
| [remotion-dev/skills](https://github.com/remotion-dev/skills) | 5.0k | **none** | skip | No licence file, and it targets Remotion while we render HyperFrames. |
| [NarratorAI-Studio/narrator-ai-cli-skill](https://github.com/NarratorAI-Studio/narrator-ai-cli-skill) | 3.0k | MIT | skip | A SKILL.md wrapper around a closed CLI. |
| [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | 2.2k | MIT | link | Workspace with a /scene-review step that verifies visuals before the final render. |
| [vibe-motion/skills](https://github.com/vibe-motion/skills) | 1.3k | **none** | skip | Unmaintained by its own README, and no licence file. |
| [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills) | 758 | MIT | link | ~50 motion skills that include safe areas and frame-accurate rendering. |
| [bangtutorial/bang-motion](https://github.com/bangtutorial/bang-motion) | 587 | MIT | link | Single-file motion with a snap.mjs frame check and a ?debug=1 switch. |
| [kangarooking/director-skills](https://github.com/kangarooking/director-skills) | 179 | MIT | link | Directing skills with a section on dependable video generation. |
| [video-db/skills](https://github.com/video-db/skills) | 127 | MIT | skip | Hosted server-side video work; breaks the local-first promise. |
| [jhartquist/claude-remotion-kickstart](https://github.com/jhartquist/claude-remotion-kickstart) | 120 | MIT | link | Starter kit with transcript-timed captions. |
| [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills) | 90 | MIT | link | Motion design fundamentals plus AE/Remotion engines. |
| [Johnson-Jia/video-clipforge](https://github.com/Johnson-Jia/video-clipforge) | 41 | Apache-2.0 | link | Nine-stage pipeline that can also run on a schedule. |
| [zhouyuechuan2025-ui/ai-self-media-video-packaging-skill](https://github.com/zhouyuechuan2025-ui/ai-self-media-video-packaging-skill) | 37 | MIT | link | Packages a talking head from its SRT, tying every graphic to what is said. |
| [bbylw/hyperframes-cn](https://github.com/bbylw/hyperframes-cn) | 28 | MIT | link | Chinese translation of the HyperFrames docs — a readable reference when the English docs are terse. |
| [GordenSun/react-bits-video](https://github.com/GordenSun/react-bits-video) | 28 | Other | link | Adds a precise rule we lack verbatim: no element under 2.2:1 WCAG luminance ratio against its effective background. |
| [smwbev/framewright](https://github.com/smwbev/framewright) | 23 | MIT | later | Every frame is a pure function of (frame, seed, width), plus a determinism check. Needs a render-twice hook in the sibling skill. |
| [doublesq97-ui/su-card-to-video](https://github.com/doublesq97-ui/su-card-to-video) | 17 | MIT | link | Minimal HTML card + audio → video template. |
| [gloweaseco-leo/hyperdirector](https://github.com/gloweaseco-leo/hyperdirector) | 17 | Apache-2.0 | link | Wraps production as planning → artifacts → validation → delivery, with 18 check mentions. |
| [magichourhq/skills](https://github.com/magichourhq/skills) | 10 | MIT | skip | Vendor skills for a hosting API. |
| [resemble-ai/remotion-resemble-skill](https://github.com/resemble-ai/remotion-resemble-skill) | 9 | MIT | skip | TTS vendor wrapper. |
| [iart-ai/data-animation-skills](https://github.com/iart-ai/data-animation-skills) | 8 | MIT | link | CSV → animated charts where the numbers stay true on every frame. |
| [molkex/mcp-flow-google](https://github.com/molkex/mcp-flow-google) | 8 | Other | link | Veo/Nano-Banana generation through a browser session instead of an API key. |
| [patraxo/ltx2-vidgen-skill](https://github.com/patraxo/ltx2-vidgen-skill) | 8 | Other | skip | Deploys a GPU backend on Modal; infrastructure, not craft. |
| [davidcervinka/vibe-editing](https://github.com/davidcervinka/vibe-editing) | 7 | MIT | link | A written account of an ffmpeg + ElevenLabs + HyperFrames workflow. |
| [VasiniDevi/motion-skills](https://github.com/VasiniDevi/motion-skills) | 7 | **none** | skip | No licence file; Pillow/OpenCV rendering. |
| [vibe-motion/remotion-starter](https://github.com/vibe-motion/remotion-starter) | 7 | MIT | link | Three-layer workbench with hooks as guardrails — the closest structure to ours. |
| [chenyuxiaojin/cyxj-remotion-starter](https://github.com/chenyuxiaojin/cyxj-remotion-starter) | 6 | MIT | skip | Near-duplicate of vibe-motion/remotion-starter. |

#### Motion Graphics & Logos (11)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [diffusionstudio/lottie](https://github.com/diffusionstudio/lottie) | 5.6k | MIT | link | Prompt → Lottie with a player workspace. |
| [nolangz/pixel2motion](https://github.com/nolangz/pixel2motion) | 2.4k | MIT | link | Only animates a QA-verified vector (IoU-gated), which is the right order. We do not do logo animation. |
| [pyang5166/gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) | 1.3k | MIT | link | Three approval gates, then per-second frame sampling and a first-frame purity check. |
| [alexgreensh/anidoodle](https://github.com/alexgreensh/anidoodle) | 873 | Apache-2.0 | link | Deterministic hand-drawn illustration styles, with hash-verified asset download. |
| [MegaTroll222/VOX-COLLAGE-BROLL](https://github.com/MegaTroll222/VOX-COLLAGE-BROLL) | 216 | Other | link | Self-QA from contact sheets, first-frame purity and end-frame comparison. |
| [Liamrjohnston/remotion-motion-graphics-skill](https://github.com/Liamrjohnston/remotion-motion-graphics-skill) | 94 | MIT | link | Kinetic text, workflow diagrams and camera moves, with explicit dark-scene palette rules. |
| [AgriciDaniel/claude-gif](https://github.com/AgriciDaniel/claude-gif) | 28 | MIT | link | Six GIF pipelines incl. palette tuning and looping. |
| [toufuim/personal-ip-brand-intro-skill](https://github.com/toufuim/personal-ip-brand-intro-skill) | 20 | MIT | link | Beat-synced brand intro with a stated refusal to ship a fixed template. |
| [fernandokaraka/remotion-motion-graphics-skill](https://github.com/fernandokaraka/remotion-motion-graphics-skill) | 11 | MIT | link | Exports MP4, transparent ProRes and PNG overlays. |
| [acelera-agency/html-animation](https://github.com/acelera-agency/html-animation) | 9 | MIT | link | Argues animation-as-code is measurable, and publishes its verify.js measurements plus the traps. |
| [zhenwusw/orca-motion-skill](https://github.com/zhenwusw/orca-motion-skill) | 9 | MIT | link | Design tokens drive abstract shapes captured frame by frame. |

#### Music Videos (2)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo) | 2.0k | **none** | skip | Source of one music video, no licence file. |
| [ledbetterljoshua/functional-emotions-video](https://github.com/ledbetterljoshua/functional-emotions-video) | 68 | MIT | skip | Source of one music video, MIT, but nothing generalisable. |

#### Product Promos & Demos (26)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 11.1k | Apache-2.0 | link | 11k★ shot-recipe-card library; the upstream of four copies below. |
| [op7418/guizang-product-video-skill](https://github.com/op7418/guizang-product-video-skill) | 751 | AGPL-3.0 | link | Reuses the real product components instead of redrawing them. |
| [geekjourneyx/hyperframes-motion-director](https://github.com/geekjourneyx/hyperframes-motion-director) | 453 | AGPL-3.0 | link | Plan → assets → composition → validate snapshots/renders → review file. |
| [tugrawork-creator/saas-motion-kit](https://github.com/tugrawork-creator/saas-motion-kit) | 219 | Other | **add** | Adopted: audit the storyboard for repetition (same transition, same layout twice) before building, not after. |
| [Finderchangchang/promo-video-skill](https://github.com/Finderchangchang/brewreel) | 145 | Apache-2.0 | later | Runs ad-law checks on the copy. Needs a claims list per market before it can rule on anything. |
| [bestagentkits/motion-video-skill](https://github.com/bestagentkits/motion-video-skill) | 117 | MIT | link | Independent confirmation of our numbers: EBU R128 ≈ −14 LUFS and SFX 4–6 dB under speech. |
| [leosssvip-dot/remotion-ad-video-skill](https://github.com/leosssvip-dot/remotion-ad-video-skill) | 111 | MIT | link | Picks the renderer (Remotion or HyperFrames) per project. |
| [kangarooking/promo-creator-skills](https://github.com/kangarooking/promo-creator-skills) | 102 | MIT | link | Opens with the right complaint: most AI promos skip product judgement and fix it later with effects. |
| [kingselyjoe/video-shotcraft-dsh](https://github.com/kingselyjoe/video-shotcraft-dsh) | 71 | Apache-2.0 | skip | Fork of video-shotcraft for another harness. |
| [norahe0304-art/30x-video](https://github.com/norahe0304-art/30x-video) | 65 | MIT | link | URL → launch video with an audiomap and a visual-audit script. |
| [trunghaiy/appshot](https://github.com/trunghaiy/appshot) | 47 | MIT | link | Store preview videos generated from a codebase. |
| [BayramAnnakov/remotion-video-director](https://github.com/BayramAnnakov/remotion-video-director) | 42 | **none** | skip | No licence file. |
| [mattivilola/brag-codex](https://github.com/mattivilola/brag-codex) | 34 | MIT | link | Launch-video skill with a structural validator. |
| [new-xp/ultrademo](https://github.com/new-xp/ultrademo) | 32 | Apache-2.0 | link | Captures a demo inside a signed-in browser session, locally. |
| [gorkem-bwl/onboarding-video-generator](https://github.com/gorkem-bwl/onboarding-video-generator) | 31 | MIT | link | Ships a DebugCrosshair component for authoring-time coordinate verification. |
| [Arman-Luthra/aftr](https://github.com/Arman-Luthra/aftr) | 23 | MIT | link | After Effects controller with an automated render-review-revise loop. |
| [AmazingAng/ccvideo](https://github.com/AmazingAng/ccvideo) | 20 | MIT | later | verify-props rebuilds props from the raw artifacts and fails on any mismatch. Needs a props/asset manifest pipeline to hang on. |
| [derrickgong87/demo-video-creation-skill](https://github.com/derrickgong87/demo-video-creation-skill) | 20 | MIT | link | URL + screenshots → SaaS demo, with quality-check scripts. |
| [memex-lab/product-launch-video-skill](https://github.com/memex-lab/product-launch-video-skill) | 18 | MIT | link | Brief → storyboard → Remotion launch film. |
| [smit-vanani/claude-promo-video](https://github.com/smit-vanani/claude-promo-video) | 16 | MIT | link | Extracts exact-frame stills specifically to verify the render. |
| [dlazy-ai/ai-product-video](https://github.com/dlazy-ai/ai-product-video) | 15 | Apache-2.0 | skip | Copy of the shotcraft recipe. |
| [kiki-lgtm-dot/cinematic-product-promo-skill](https://github.com/kiki-lgtm-dot/cinematic-product-promo-skill) | 14 | Apache-2.0 | skip | Copy of the shotcraft recipe with a triple-gate label. |
| [iart-ai/ad-video-skills](https://github.com/iart-ai/ad-video-skills) | 13 | MIT | link | One motion template → many branded variants. |
| [opus-pro/opus-video-studio](https://github.com/opus-pro/opusclip-video-tools) | 12 | **none** | skip | No licence file at the repo root. |
| [mrieck/demoday-claude-plugin](https://github.com/mrieck/demoday-claude-plugin) | 7 | MIT | link | Drives the app on screen, writes the script, adds voiceover. |
| [ChenShuo2004/cs-shotcraft-skill](https://github.com/ChenShuo2004/cs-shotcraft-skill) | 6 | Apache-2.0 | skip | Fork of video-shotcraft for Codex. |

#### Scriptwriting & Film Study (10)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [jtydhr88/screenwriting-skills](https://github.com/jtydhr88/screenwriting-skills) | 1.6k | MIT | link | 26 screenwriting skills. Out of production scope — we cut, we do not draft features. |
| [eternityspring/reelbench-skills](https://github.com/eternityspring/reelbench-skills) | 877 | Apache-2.0 | link | Shot-by-shot analysis, synced storyboard videos, metadata cleaning. |
| [gnipbao/minimax-h3-video-reverse-skill](https://github.com/gnipbao/minimax-h3-video-reverse-skill) | 229 | MIT | link | Reverse-engineers a reference video into per-shot generation prompts, confirming its reading with the user first. |
| [wyuzhi/qisi-video-remix](https://github.com/wyuzhi/qisi-video-remix) | 171 | MIT | link | Reference video → new story, script and storyboard; honest that prompt success must be tested in the target tool. |
| [adityaarsharma/youtube-marketing-skills](https://github.com/adityaarsharma/youtube-marketing-skills) | 54 | MIT | skip | Channel growth and publishing analytics, not video production. |
| [wocha-xiaoli/video-shot-analysis-feishu](https://github.com/wocha-xiaoli/video-shot-analysis-feishu) | 39 | MIT | link | Extracts frames, builds a shot database; its README names OpenCode as a supported host. |
| [liuliu-66-create/ll-video-decomposer](https://github.com/liuliu-66-create/ll-video-decomposer) | 24 | MIT | link | Five-layer decomposition (transcript, visuals, shots, captions, audio). |
| [erduo1998-cell/video-script-builder](https://github.com/erduo1998-cell/video-script-builder) | 11 | MIT | link | Transcript → framework-specific storyboard spec. |
| [chenmisss/laoxu-video-script](https://github.com/chenmisss/laoxu-video-script) | 9 | MIT | skip | Account positioning and topic selection — marketing, not production. |
| [sharon-laicc/viral-video-decomposer](https://github.com/sharon-laicc/viral-video-decomposer) | 7 | MIT | link | Viral short → shot structure + mechanism + production brief. |

#### Short-form & Talking-head (19)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [Yuuhann1999/codex-storyboard](https://github.com/Yuuhann1999/agent-storyboard) | 358 | MIT | link | Local-first storyboard table the human inspects and approves — same hold as our G1. |
| [hassancs91/claude-faceless-shorts-creator](https://github.com/hassancs91/claude-faceless-shorts-creator) | 271 | MIT | link | Frame-by-frame QA at phone scale, plus a self-growing SFX library. |
| [jaxxchen003/book-video-factory](https://github.com/jaxxchen003/book-video-factory) | 105 | MIT | link | Rights-aware workflow with auditable evidence and approvals; bundles an OFL fallback font. |
| [Maartenlouis/remotion-ads](https://github.com/Maartenlouis/remotion-ads) | 61 | MIT | link | Validates generated-audio timing against the captions. |
| [pyang5166/gbro-collage-info](https://github.com/pyang5166/gbro-collage-info) | 51 | MIT | link | Three confirmation gates, then local HTML/CSS/GSAP render with a foley track. |
| [liangdabiao/story-handdrawn-video](https://github.com/liangdabiao/story-handdrawn-video) | 49 | **none** | skip | No licence file. |
| [yuwenbin121/book-video-production-skill](https://github.com/yuwenbin121/book-video-production-skill) | 17 | MIT | link | Fact-checked book shorts with a named validation step. |
| [intelligent-iterations/ii-content-engine](https://github.com/intelligent-iterations/ii-content-engine) | 15 | MIT | skip | Generation plus scheduling engine; we produce, we do not schedule. |
| [iart-ai/tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) | 14 | MIT | link | Hook and retention structure as separate skills. |
| [adriiita/vertical-video-editing-skill](https://github.com/adriiita/vertical-video-editing-skill) | 10 | MIT | link | Nearest neighbour on our exact axis: a bundled verify-render.mjs gate that asserts 9:16 dimensions. 19 check mentions, MIT, 10★. |
| [Samin12/samin-reel-engine-plugin](https://github.com/Samin12/samin-reel-engine-plugin) | 9 | Other | link | Documents its own verification limits instead of claiming a clean pass. |
| [riffkit/skill](https://github.com/riffkit/skill) | 7 | MIT | skip | Paid restyling service behind a skill. |
| [zoglmk/codex-video-pipeline](https://github.com/zoglmk/codex-video-pipeline) | 7 | MIT | link | Topic → MP4 + covers + publishing package + source record. Very close to our shape. |
| [icytear-svg/podcast-to-video](https://github.com/icytear-svg/podcast-to-video) | 5 | **none** | link | Podcast audio + cover + subtitles → waveform video. Our unexercised podcast mode; no licence file. |
| [inematds/skill-video-plan-editor](https://github.com/inematds/skill-video-plan-editor) | 5 | **none** | link | Produces a renderer-agnostic edit-plan JSON and validates it with `vpe validate`. No licence file. |
| [liangdabiao/wechat-article-remotion](https://github.com/liangdabiao/wechat-article-remotion) | 5 | **none** | skip | No licence file. |
| [marketcalls/story-telling](https://github.com/marketcalls/story-telling) | 5 | MIT | link | Context → narrated story video with a first-run key verification step. |
| [ninestonelee/youtube-shorts-factory](https://github.com/ninestonelee/youtube-shorts-factory) | 5 | MIT | skip | Clones a viral formula; the ethics are not ours to police, but it teaches nothing we can use. |
| [wendymardigian-prog/Editor-IA-Pro](https://github.com/wendymardigian-prog/Editor-IA-Pro) | 5 | Other | skip | Remotion + Whisper editor scaffold; overlaps what our renderer already does, with less gate coverage. |

#### Story & Animation (13)

| repo | ★ | licence | verdict | note |
|---|---:|---|---|---|
| [gnipbao/story-to-handdrawn-video](https://github.com/gnipbao/story-to-handdrawn-video) | 2.2k | MIT | link | check:storyboard plus per-render asset validation before every render. |
| [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) | 1.6k | Other | link | Already assessed: MIT code, CC BY 4.0 films. Ten of its styles were restated in our grammar in styles/pack.json. |
| [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase) | 985 | MIT | link | p5.js + p5.brush hand-painted character rig. |
| [aaronyi97/image-story-video-wizard](https://github.com/aaronyi97/image-story-video-wizard) | 356 | MIT | link | Audio-first image story with a validation section. |
| [liyue-aigc/xianxia-cinematic-video-director](https://github.com/liyue-aigc/xianxia-cinematic-video-director) | 269 | **none** | skip | Outputs prompts only, and has no licence file. |
| [LetMeHappyCode/auto-video-agent](https://github.com/LetMeHappyCode/auto-video-agent) | 218 | **none** | skip | No licence file. |
| [tuzhechen2005/opus-video-skills](https://github.com/tuzhechen2005/opus-video-skills) | 144 | Other | link | One skill per visual style, headless Chrome + ffmpeg. |
| [Mr-funny/hbg-life-simulation](https://github.com/Mr-funny/hbg-life-simulation) | 141 | MIT | **add** | Normalises to −22.8 LUFS, close to the −23 broadcast reference, and runs a QA pass. Feeds the platform table. |
| [liangdabiao/story-handdrawn-remotion](https://github.com/liangdabiao/story-handdrawn-remotion) | 37 | **none** | skip | No licence file. |
| [JimLiu/taohuayuan](https://github.com/JimLiu/taohuayuan) | 31 | **none** | skip | Interactive three.js scroll, not a video. |
| [AsadMoulviDev/reel-video](https://github.com/AsadMoulviDev/reel-video) | 29 | MIT | link | Local CLI plus a browser review board for storyboard and keyframes. |
| [AllenAI2014/remotion-guofeng-starter](https://github.com/AllenAI2014/remotion-guofeng-starter) | 28 | Other | link | Chinese paper-collage asset library with a one-command render. |
| [taylorzhou16/video-gen](https://github.com/taylorzhou16/video-gen) | 9 | **none** | skip | No licence file. |

### Caveat that stays attached

This is a README-level audit of 184 repos, not a code review. "Checks the render" is the author's description of
their own engine; none of it was executed here. Three repos could not be read at all. Descriptions also lie by
omission — a repo can have excellent gates and never mention them.

