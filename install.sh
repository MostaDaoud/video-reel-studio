#!/usr/bin/env bash
# install.sh — install video-reel-studio for OpenCode
#   bash install.sh            → ./.opencode/skills (project)
#   bash install.sh --global   → ~/.config/opencode/skills
set -euo pipefail

GLOBAL=0
[ "${1:-}" = "--global" ] && GLOBAL=1

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$HERE/skill/video-reel-studio"

if [ "$GLOBAL" = "1" ]; then
  DEST="$HOME/.config/opencode/skills"
else
  DEST="$(pwd)/.opencode/skills"
fi

echo "→ installing into $DEST"
mkdir -p "$DEST"
rm -rf "$DEST/video-reel-studio"
cp -r "$SRC" "$DEST/"
echo "  ✓ video-reel-studio"

# dependency check
missing=0
for s in video-ad-editor montage-video motion-video podcast-video thumbnail-video review-video; do
  if [ -d "$DEST/$s" ] || [ -d "$HOME/.config/opencode/skills/$s" ]; then
    echo "  ✓ $s"
  else
    echo "  ✗ $s  (missing — see README step 2)"
    missing=1
  fi
done

if [ "$missing" = "1" ]; then
  echo
  echo "Install the production skills first:"
  echo "  git clone https://github.com/majedphotos/video-ad-editor /tmp/vae"
  echo "  cp -r /tmp/vae/{video-ad-editor,montage-video,motion-video,podcast-video,thumbnail-video,review-video} \"$DEST/\""
fi

PY=python3
command -v python3 >/dev/null 2>&1 || PY=python
echo
echo "→ environment check"
"$PY" "$DEST/video-reel-studio/scripts/preflight.py" || true

echo
echo "Done. Open OpenCode and say: «منتج الفيديو ده»"
