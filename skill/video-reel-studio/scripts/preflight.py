# -*- coding: utf-8 -*-
"""preflight.py — هل السكل يشتغل على الجهاز ده؟ (ويندوز / ماك / لينكس)

  python preflight.py [--json]

يطبع جدول: الأداة · الحالة · الإصلاح. يخرج بـ1 لو فيه blocker.
لا يعدّل أي شيء — فحص فقط.
"""
import json
import os
import platform
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SYS = platform.system()          # Windows | Darwin | Linux
IS_WIN = SYS == "Windows"
IS_MAC = SYS == "Darwin"
HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SKILLS = os.path.dirname(SKILL)
ROWS = []
BLOCK = 0


def row(name, state, detail="", fix=""):
    global BLOCK
    ROWS.append({"name": name, "state": state, "detail": detail, "fix": fix})
    if state == "fail":
        BLOCK += 1


def has(exe):
    return shutil.which(exe)


def py_cmd():
    for c in (["python"], ["python3"], ["py", "-3"]):
        try:
            r = subprocess.run(c + ["-c", "import sys;print(sys.version_info[:2])"], capture_output=True, text=True)
            if r.returncode == 0:
                return c, r.stdout.strip()
        except Exception:
            pass
    return None, ""


def chrome_path():
    cands = []
    if IS_WIN:
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)"),
                     os.environ.get("LOCALAPPDATA", "")):
            if base:
                cands.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
    elif IS_MAC:
        cands += ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")]
    else:
        cands += ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]
    return next((p for p in cands if p and os.path.isfile(p)), "")


def bash_path():
    if IS_WIN:
        for p in (r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files (x86)\Git\bin\bash.exe"):
            if os.path.isfile(p):
                return p
        return ""
    return shutil.which("bash") or ""


def python_deps(cmd):
    r = subprocess.run(cmd + ["-c", "import numpy,scipy;print('ok')"], capture_output=True, text=True)
    return r.returncode == 0, (r.stdout or r.stderr).strip()[:80]


def py_has(cmd, mods):
    r = subprocess.run(cmd + ["-c", "import " + ",".join(mods)], capture_output=True)
    return r.returncode == 0


def read_text(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def main():
    print("== البيئة ==")
    print("النظام: %s %s · %s" % (SYS, platform.release(), platform.machine()))
    print("بايثون السكل: %s" % sys.version.split()[0])

    cmd, ver = py_cmd()
    row("python", "pass" if cmd else "fail", " ".join(cmd or []) + " · " + ver,
        "ثبّت Python 3.10+" if not cmd else "")

    for exe, hint in (("ffmpeg", "winget install Gyan.FFmpeg" if IS_WIN else "brew install ffmpeg"),
                      ("ffprobe", "ييجي مع ffmpeg"),
                      ("node", "winget install OpenJS.NodeJS" if IS_WIN else "brew install node")):
        p = has(exe)
        row(exe, "pass" if p else "fail", p or "غير موجود", hint)

    # ffmpeg 7+ بيكتب ملف ألوان الحاوية (colr prof) — بلاه مشغّل أبل يعرض الريل أفتح 9 من 255.
    # 6.0 بيقرا الـICC من الـJPEG بس ما يوصّله للموكسر، فـprefer_icc بيطلع nclx أو لا شي (قاسها هنا 13 نوفمبر).
    if has("ffmpeg"):
        r = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        v = (r.stdout or "").split("\n")[0].strip()
        mj = __import__("re").search(r"ffmpeg version (\d+)\.", v)
        ng = __import__("re").search(r"N-\d+-g[0-9a-f]+-(\d{8})", v)
        ok = (int(mj.group(1)) >= 7) if mj else bool(ng and ng.group(1) >= "20250101")
        row("ffmpeg 7+", "pass" if ok else "warn", v[:64] or "نسخة غير معروفة",
            "" if ok else "نسخة 7+ بتكتب colr prof — G5b بتحذّر بدونه (أبل بيعرض أفتح)")

    b = bash_path()
    row("bash", "pass" if b else ("warn" if IS_WIN else "fail"), b or "غير موجود",
        "ثبّت Git for Windows" if IS_WIN else "bash موجود افتراضيًا")

    c = chrome_path()
    row("chrome", "pass" if c else "fail", c or "غير موجود",
        "ثبّت Google Chrome (الرسم والكفر يعتمد عليه)")

    if cmd:
        ok, msg = python_deps(cmd)
        row("numpy+scipy", "pass" if ok else "warn", msg,
            "pip install numpy scipy (فيلم الموشن يحتاجهم)")
        for mods, label, why in (
            (["cv2", "PIL"], "opencv+Pillow", "وضع مراجعة المنتج والكفر يحتاجوهم"),
            (["rembg", "pymatting"], "قصّ الشعر الناعم", "اختياري — يحسّن حواف القصّ حوالين الشخص"),
            (["torch", "transformers"], "بحث بالمعنى", "اختياري — 26_find_shots.py"),
        ):
            has_it = py_has(cmd, mods)
            row(label, "pass" if has_it else "warn", "موجود" if has_it else "ناقص — اختياري",
                "" if has_it else why + " — 00_setup.sh --extras")

    # سكلات شقيقة
    need = {
        "video-ad-editor/scripts/04_render_frames.js": "المحرّك",
        "video-ad-editor/motion/engine.js": "فيلم الموشن",
        "montage-video": "مونتاج",
        "podcast-video": "بودكاست",
        "motion-video": "موشن",
        "thumbnail-video": "ثمبنيل",
        "review-video": "مراجعة منتج",
    }
    for rel, label in need.items():
        p = os.path.join(SKILLS, rel)
        row(label, "pass" if os.path.exists(p) else "warn", p, "ثبّت السكل الشقيق في مجلد skills")

    # قدرات upstream 6.4–6.6 — السكل بيدّي أوامر ما كانتش موجودة في نسخة أقدم.
    # فحص الملف وعلامة جوّاه أرخص من إصدار رقمي، وبيقول للمستخدم بالضبط ينزّل إيه.
    caps = [
        ("video-ad-editor/scripts/review/review.py", "قدرة: ريل مراجعة منتج", None),
        ("video-ad-editor/scripts/depth.js", "قدرة: العمق والطبقات", "DEPTH"),
        ("video-ad-editor/scripts/44_matte.py", "قدرة: قصّ الشعر الناعم", "rembg"),
        ("video-ad-editor/scripts/43_textbox.py", "قدرة: مربع على المكتوب", "textfind"),
        ("video-ad-editor/sfx/bank.npz", "قدرة: بنك المؤثرات CC0", None),
        ("video-ad-editor/scripts/32_midframes.py", "قدرة: ستوري بورد --story", "--story"),
        ("video-ad-editor/scripts/35_moves.py", "قدرة: حركة 101/102 + inspire", "inspire"),
        ("video-ad-editor/scripts/_compat.sh", "قدرة: ألوان مطابقة VF_FRAMES", "VF_FRAMES"),
    ]
    stale = []
    for rel, label, marker in caps:
        p = os.path.join(SKILLS, rel)
        ok = os.path.exists(p) and (not marker or marker in read_text(p))
        row(label, "pass" if ok else "warn", "موجود" if ok else "ناقص",
            "" if ok else "git -C \"%s\" pull — السكل مُختبَر على 6.6.0" % os.path.join(SKILLS, "video-ad-editor"))
        if not ok:
            stale.append(label)
    vf = os.path.join(SKILLS, "video-ad-editor", "VERSION")
    if os.path.exists(vf):
        v = read_text(vf).strip()
        row("نسخة upstream", "pass" if v.startswith("6.6") else "warn", v or "فاضي",
            "السكل مُختبَر على 6.6.0 — %s" % ("تمام" if v.startswith("6.6") else "حدّث video-ad-editor"))

    fonts = os.path.join(SKILLS, "video-ad-editor", "motion", "fonts", "Cairo-VF.ttf")
    row("خط Cairo", "pass" if os.path.exists(fonts) else "warn", fonts, "ييجي مع video-ad-editor")
    ruqaa = os.path.join(SKILLS, "video-ad-editor", "motion", "fonts", "ArefRuqaa-Bold.ttf")
    row("خط الرقعة", "pass" if os.path.exists(ruqaa) else "warn", "Aref Ruqaa",
        "حركة 101 والكفر بيستخدموه — ييجي مع 6.5+")

    brands = os.path.join(os.path.expanduser("~"), ".config", "opencode", "brands")
    try:
        os.makedirs(brands, exist_ok=True)
        probe = os.path.join(brands, ".write-test")
        open(probe, "w").write("1")
        os.remove(probe)
        row("مجلد الهويات", "pass", brands, "")
    except Exception as e:
        row("مجلد الهويات", "fail", str(e)[:60], "صلّح صلاحيات المجلد أو استخدم --dir")

    # وكيل المشروع (من علامة المجلد) + مطابقته لـai.json
    markers = {".opencode": "opencode", ".claude": "claude-code", ".codex": "codex",
               ".cursor": "cursor", ".gemini": "gemini-cli"}
    cwd = os.getcwd()
    found = [v for k, v in markers.items() if os.path.exists(os.path.join(cwd, k))]
    row("وكيل المشروع", "pass" if found else "warn",
        found[0] if found else "مش معروف من المجلد", "شغّل من جذر المشروع")
    aij = os.path.join(cwd, "ai.json")
    if found and os.path.exists(aij):
        try:
            ai = json.load(open(aij, encoding="utf-8"))
            if ai.get("host") and ai["host"] != found[0]:
                row("ملاءمة ai.json", "warn",
                    "ai.json بيقول %s والمشروع %s" % (ai["host"], found[0]),
                    "عدّل ai.json أو انقل المشروع")
            else:
                row("ملاءمة ai.json", "pass", ai.get("host", ""), "")
        except Exception:
            row("ملاءمة ai.json", "warn", "ملف غير صالح", "أعد onboard.py apply")

    print()
    icons = {"pass": "✅", "warn": "⚠️", "fail": "❌"}
    for r in ROWS:
        line = "%s %-14s %s" % (icons[r["state"]], r["name"], r["detail"])
        if r["state"] != "pass" and r["fix"]:
            line += "  ← " + r["fix"]
        print(line)

    print()
    print(("❌ فيه %d مشكلة تمنع الشغل" % BLOCK) if BLOCK else "✅ كل الأدوات موجودة — السكل جاهز")
    if stale:
        print("⚠️ السكل مُختبَر على upstream 6.6.0 — الناقص: %s" % " · ".join(stale))
    if "--json" in sys.argv:
        print(json.dumps({"system": SYS, "blocked": BLOCK, "rows": ROWS}, ensure_ascii=False, indent=1))
    return 1 if BLOCK else 0


if __name__ == "__main__":
    sys.exit(main())
