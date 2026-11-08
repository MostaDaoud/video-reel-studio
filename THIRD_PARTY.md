# Third-party notices

This repository is MIT licensed (see [LICENSE](LICENSE)). The components below are
separate works with their own copyright and licence, and are **not** vendored here.

## Skills this orchestrator calls (`video-ad-editor` and siblings)

`video-reel-studio` is an orchestrator. It does not reimplement the production skills it
drives — cutting, captions, frame rendering, safe-zone checks. Those come from
[majedphotos/video-ad-editor](https://github.com/majedphotos/video-ad-editor), also
released under the MIT License. Their code is not included in this repository; it is
installed separately (see `install.ps1` / `install.sh`) and retains its own copyright
and licence.

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

## Sample output

The demo videos under `assets/` were produced by this skill. The footage in them is the
author's own; the projects that produced them are not part of this repository.
