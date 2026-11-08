# -*- coding: utf-8 -*-
"""style_pack.py — ستايلات مقتبسة فكريًا من Lemo، مكتوبة لصيغة محرّكنا.

  python style_pack.py list
  python style_pack.py show <id>
  python style_pack.py apply <work> <id>     # يكتب <work>/style.json (مش theme.json)

الألوان في style.json هي «مزاج الستايل»، والـtheme هو هوية العميل. الاثنان منفصلان:
لو العميل عنده براند، البراند يكسب في اللون، والستايل يحكم الحركة والملمس والإيقاع.
"""
import argparse
import json
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(os.path.dirname(HERE), "styles", "pack.json")


def load():
    with open(PACK, encoding="utf-8") as f:
        return json.load(f)


def cmd_list(a):
    p = load()
    print("%-12s %-16s %s" % ("id", "الاسم", "يستخدم امتى"))
    for s in p["styles"]:
        print("%-12s %-16s %s" % (s["id"], s["name_ar"], s["when"]))
    print("\n%d ستايل · %s" % (len(p["styles"]), p["credit"]))


def cmd_show(a):
    p = load()
    s = next((x for x in p["styles"] if x["id"] == a.id), None)
    if not s:
        print("مفيش ستايل بالاسم ده. جرّب list.")
        return 2
    if a.json:
        print(json.dumps(s, ensure_ascii=False, indent=1))
        return 0
    print("# %s — %s\n" % (s["name_ar"], s["name_en"]))
    print("**إمتى:** %s\n" % s["when"])
    pal = s["palette"]
    print("**اللوحة:** bg `%s` · ink `%s` · acc `%s` · alt `%s`\n" % (pal["bg"], pal["ink"], pal["acc"], pal["alt"]))
    print("**الخط:** %s (عرض) · %s (متن)\n" % (s["type"]["display"], s["type"]["body"]))
    print("**الحركة:** %s\n" % " · ".join(s["motion"]))
    print("**الصوت:** %s\n" % s["sound"])
    print("**مشاهد جاهزة للصياغة:**")
    for sc in s["scenes"]:
        print("- " + sc)
    print("\n%s" % p["credit"])
    return 0


def cmd_apply(a):
    p = load()
    s = next((x for x in p["styles"] if x["id"] == a.id), None)
    if not s:
        print("مفيش ستايل بالاسم ده. جرّب list.")
        return 2
    w = os.path.abspath(a.work)
    os.makedirs(w, exist_ok=True)
    out = {
        "id": s["id"], "name_ar": s["name_ar"], "name_en": s["name_en"],
        "when": s["when"], "palette": s["palette"], "type": s["type"],
        "motion": s["motion"], "sound": s["sound"], "scenes": s["scenes"],
        "credit": p["credit"],
        "rule": "اللون من theme.json لو فيه براند؛ الستايل يحكم الحركة والملمس والإيقاع.",
    }
    path = os.path.join(w, "style.json")
    json.dump(out, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("✅ style.json →", path)
    print("   الستايل: %s · الحركة: %s" % (s["name_ar"], " · ".join(s["motion"])))
    print("   الخطوة: المصمّم يقرا style.json قبل أول مشهد، ويبني المشاهد من %d أفكار." % len(s["scenes"]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    sh = sub.add_parser("show"); sh.add_argument("id"); sh.add_argument("--json", action="store_true")
    ap_ = sub.add_parser("apply"); ap_.add_argument("work"); ap_.add_argument("id")
    a = ap.parse_args()
    return {"list": cmd_list, "show": cmd_show, "apply": cmd_apply}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
