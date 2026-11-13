# Third-party notices

This repository is MIT licensed (see [LICENSE](LICENSE)). The components below are
separate works with their own copyright and licence, and are **not** vendored here.

## Skills this orchestrator calls (`video-ad-editor` and siblings)

`video-reel-studio` is an orchestrator. It does not reimplement the production skills it
drives — cutting, captions, frame rendering, safe-zone checks, and the product-review lane. Those come from
[majedphotos/video-ad-editor](https://github.com/majedphotos/video-ad-editor), also
released under the MIT License. Their code is not included in this repository; it is
installed separately (see `install.ps1` / `install.sh`) and retains its own copyright
and licence.

The orchestrator is tested against upstream **6.6.0**. `preflight.py` checks for the
capabilities it depends on (`review/review.py`, `depth.js`, `44_matte.py`, `43_textbox.py`,
`sfx/bank.npz`, `32_midframes.py --story`, `35_moves.py inspire`, `_compat.sh` colour filters).

## Sound effects

Upstream ships `sfx/bank.npz` — 46 CC0 1.0 recordings cut from the OpenGameArt packs
[100 CC0 SFX](https://opengameart.org/content/100-cc0-sfx),
[100 CC0 SFX #2](https://opengameart.org/content/100-cc0-sfx-2) and the
[Swishes Sound Pack](https://opengameart.org/content/swishes-sound-pack), plus two
code-generated sounds (`pen`, `whip`). CC0 requires no attribution; credit is recorded
here anyway. The bank is **not** redistributed in this repository.

## Art-direction styles

`skill/video-reel-studio/styles/pack.json` contains ten styles **written from scratch**
in this project's own grammar (palette, type, motion verbs, sound, scene seeds). They are
*inspired by* the style catalogue of
[lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) (MIT code, CC BY 4.0
films). No film, frame or `STYLE.md` from that project is copied here. Any future use of
their footage requires credit to **LemoLab**, a link, and a statement of changes.

## Render engine

Videos are rendered with [HyperFrames](https://github.com/heygen-com/hyperframes)
(Apache-2.0). It is installed as a dependency, not redistributed.

## Fonts

The orchestrator bundles **no** font files. It names the fonts the upstream engine loads
from its own `motion/fonts/` folder — Cairo (SIL OFL), Lalezar (SIL OFL) and, from 6.5,
Aref Ruqaa (SIL OFL) for the reveal-list move and the storyboard page. Each retains its
own licence and is installed with the production skills.

## Sample output

The demo videos under `assets/` were produced by this skill. The footage in them is the
author's own; the projects that produced them are not part of this repository.
