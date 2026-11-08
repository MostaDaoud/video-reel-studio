# -*- coding: utf-8 -*-
"""onboard.py — هوية العميل مرة واحدة، وتُعاد لكل فيديو.

  python onboard.py list
  python onboard.py new   <slug> --name "..." [--handle @x] [--audience "..."] [--tone "..."]
                                 [--bg "#0B0C0C"] [--ink "#F4F2EE"] [--acc "#19C3AE"]
                                 [--clay "#0F766E"] [--font Cairo] [--capstyle chunk]
                                 [--cta "..."] [--avoid "..." ] [--logo path.png]
  python onboard.py apply <work> <slug>        # يكتب theme.json + brand.md في مجلد العمل
  python onboard.py card  <slug> [--out x.svg] # بطاقة هوية تُعرض للمستخدم
  python onboard.py check <slug>               # تباين وألوان فقط

التباين: ink/bg ≥ 7 مثالي، ≥ 4.5 مقبول، أقل = فشل.
"""
import argparse
import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
FONTS = ["Cairo", "IBM Plex Sans Arabic", "Noto Kufi Arabic", "Lalezar", "Readex Pro", "Tajawal", "Aref Ruqaa", "Inter"]
CAPSTYLES = ["chunk", "line", "word", "boxed", "karaoke"]


def brand_dir():
    d = os.path.join(os.path.expanduser("~"), ".config", "opencode", "brands")
    os.makedirs(d, exist_ok=True)
    return d


def path_of(slug):
    return os.path.join(brand_dir(), slug + ".json")


def lum(hexcolor):
    h = hexcolor.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    c = [(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4) for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def checks(br):
    out = []
    pairs = [("ink", "bg", 4.5, 7.0), ("acc", "bg", 3.0, 4.5), ("onAcc", "acc", 4.5, 7.0), ("mut", "bg", 3.0, 4.5)]
    for fg, bg, hard, soft in pairs:
        if fg not in br or bg not in br:
            continue
        c = contrast(br[fg], br[bg])
        level = "pass" if c >= soft else ("warn" if c >= hard else "fail")
        out.append((fg, bg, round(c, 2), level))
    for k in ("bg", "ink", "acc", "clay", "mut", "onAcc"):
        if k in br and not HEX.match(br[k] or ""):
            out.append((k, "-", 0, "fail"))
    if br.get("font") and br["font"] not in FONTS:
        out.append(("font", "-", 0, "warn"))
    if br.get("capstyle") and br["capstyle"] not in CAPSTYLES:
        out.append(("capstyle", "-", 0, "warn"))
    return out


def smart_onacc(acc):
    return "#062B27" if lum(acc) > 0.35 else "#FFFFFF"


def cmd_new(a):
    slug = re.sub(r"[^a-z0-9\-]", "-", a.slug.lower()).strip("-")
    br = {
        "slug": slug,
        "name": a.name,
        "handle": a.handle or "",
        "audience": a.audience or "",
        "tone": a.tone or "",
        "cta": a.cta or "",
        "avoid": a.avoid or "",
        "logo": a.logo or "",
        "bg": a.bg, "ink": a.ink, "acc": a.acc, "clay": a.clay or a.acc,
        "mut": a.mut, "onAcc": a.onacc or smart_onacc(a.acc),
        "font": a.font, "capstyle": a.capstyle,
        "created": a.created or "",
    }
    res = checks(br)
    bad = [r for r in res if r[3] == "fail"]
    for fg, bg, c, lvl in res:
        print("%-6s / %-6s  %5.2f  %s" % (fg, bg, c, lvl))
    if bad:
        print("❌ تباين ضعيف — عدّل الألوان قبل الحفظ")
        return 3
    json.dump(br, open(path_of(slug), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("✅ الهوية محفوظة:", path_of(slug))
    return 0


def load(slug):
    p = path_of(slug)
    if not os.path.exists(p):
        print("ما فيه هوية بهذا الاسم:", slug)
        sys.exit(2)
    return json.load(open(p, encoding="utf-8"))


def cmd_list(_a):
    d = brand_dir()
    items = [f for f in os.listdir(d) if f.endswith(".json")]
    if not items:
        print("(ما فيه هويات محفوظة)")
        return
    for f in sorted(items):
        try:
            b = json.load(open(os.path.join(d, f), encoding="utf-8"))
            print("- %-14s %s · %s · %s" % (b.get("slug"), b.get("name"), b.get("font"), b.get("acc")))
        except Exception:
            print("-", f, "(تالف)")


def cmd_apply(a):
    br = load(a.slug)
    w = os.path.abspath(a.work)
    os.makedirs(w, exist_ok=True)
    theme = {
        "bg": br["bg"], "ink": br["ink"], "acc": br["acc"], "clay": br["clay"],
        "mut": br["mut"], "onAcc": br["onAcc"], "font": br["font"],
        "handle": br.get("handle", ""), "capStyle": br.get("capstyle", "chunk"),
        "grid": False, "bar": True,
    }
    json.dump(theme, open(os.path.join(w, "theme.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# هوية %s" % br.get("name", a.slug), "",
          "- الهاندل: %s" % br.get("handle", "—"),
          "- الجمهور: %s" % br.get("audience", "—"),
          "- النبرة: %s" % br.get("tone", "—"),
          "- النداء: %s" % br.get("cta", "—"),
          "- ممنوع: %s" % br.get("avoid", "—"),
          "- الألوان: bg %s · ink %s · acc %s · clay %s" % (br["bg"], br["ink"], br["acc"], br["clay"]),
          "- الخط: %s · نمط الكابشن: %s" % (br["font"], br.get("capstyle", "chunk")), ""]
    open(os.path.join(w, "brand.md"), "w", encoding="utf-8").write("\n".join(md))
    print("✅ theme.json + brand.md →", w)
    return 0


def cmd_card(a):
    br = load(a.slug)
    W, H = 1080, 1350
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
           '<rect width="%d" height="%d" fill="%s"/>' % (W, H, br["bg"]),
           '<text x="60" y="120" fill="%s" font-family="Cairo, sans-serif" font-size="54" font-weight="900">%s</text>' % (br["ink"], br.get("name", "")),
           '<text x="60" y="170" fill="%s" font-family="Cairo, sans-serif" font-size="28">%s</text>' % (br["mut"], br.get("handle", "")),
           '<rect x="60" y="230" width="960" height="150" rx="24" fill="%s"/>' % br["acc"],
           '<text x="90" y="325" fill="%s" font-family="Cairo, sans-serif" font-size="46" font-weight="900">الكابشن بيبان كده</text>' % br["onAcc"]]
    sw = [("الخلفية", br["bg"], br["ink"]), ("النص", br["ink"], br["bg"]),
          ("الأكسنت", br["acc"], br["onAcc"]), ("الطيني", br["clay"], br["ink"]),
          ("الخافت", br["mut"], br["bg"])]
    x = 60
    for label, col, fg in sw:
        svg.append('<rect x="%d" y="440" width="180" height="180" rx="18" fill="%s" stroke="rgba(255,255,255,.15)"/>' % (x, col))
        svg.append('<text x="%d" y="660" fill="%s" font-family="Cairo, sans-serif" font-size="24">%s</text>' % (x, br["ink"], label))
        svg.append('<text x="%d" y="692" fill="%s" font-family="Inter, monospace" font-size="20">%s</text>' % (x, br["mut"], col))
        x += 196
    rows = [("الجمهور", br.get("audience")), ("النبرة", br.get("tone")), ("النداء", br.get("cta")),
            ("ممنوع", br.get("avoid")), ("الخط", br.get("font")), ("نمط الكابشن", br.get("capstyle"))]
    y = 780
    for k, v in rows:
        if not v:
            continue
        svg.append('<text x="60" y="%d" fill="%s" font-family="Cairo, sans-serif" font-size="26">%s</text>' % (y, br["mut"], k))
        svg.append('<text x="300" y="%d" fill="%s" font-family="Cairo, sans-serif" font-size="30" font-weight="700">%s</text>' % (y, br["ink"], v))
        y += 62
    svg.append('</svg>')
    out = a.out or os.path.join(brand_dir(), br["slug"] + "-card.svg")
    open(out, "w", encoding="utf-8").write("\n".join(svg))
    print("✅ بطاقة الهوية:", out)
    return 0


def cmd_check(a):
    br = load(a.slug)
    res = checks(br)
    bad = 0
    for fg, bg, c, lvl in res:
        print("%-6s / %-6s  %5.2f  %s" % (fg, bg, c, lvl))
        bad += (lvl == "fail")
    print("❌" if bad else "✅", "مشاكل:", bad)
    return 3 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    n = sub.add_parser("new")
    n.add_argument("slug")
    n.add_argument("--name", required=True)
    n.add_argument("--handle", default="")
    n.add_argument("--audience", default="")
    n.add_argument("--tone", default="")
    n.add_argument("--cta", default="")
    n.add_argument("--avoid", default="")
    n.add_argument("--logo", default="")
    n.add_argument("--bg", default="#0B0C0C")
    n.add_argument("--ink", default="#F4F2EE")
    n.add_argument("--acc", default="#19C3AE")
    n.add_argument("--clay", default="")
    n.add_argument("--mut", default="#9AA5A2")
    n.add_argument("--onacc", default="")
    n.add_argument("--font", default="Cairo")
    n.add_argument("--capstyle", default="chunk")
    n.add_argument("--created", default="")
    ap_ = sub.add_parser("apply"); ap_.add_argument("work"); ap_.add_argument("slug")
    c = sub.add_parser("card"); c.add_argument("slug"); c.add_argument("--out", default="")
    k = sub.add_parser("check"); k.add_argument("slug")
    a = ap.parse_args()
    return {"list": cmd_list, "new": cmd_new, "apply": cmd_apply, "card": cmd_card, "check": cmd_check}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
