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

    # سكلات شقيقة
    need = {
        "video-ad-editor/scripts/04_render_frames.js": "المحرّك",
        "video-ad-editor/motion/engine.js": "فيلم الموشن",
        "montage-video": "مونتاج",
        "podcast-video": "بودكاست",
        "motion-video": "موشن",
        "thumbnail-video": "ثمبنيل",
    }
    for rel, label in need.items():
        p = os.path.join(SKILLS, rel)
        row(label, "pass" if os.path.exists(p) else "warn", p, "ثبّت السكل الشقيق في مجلد skills")

    fonts = os.path.join(SKILLS, "video-ad-editor", "motion", "fonts", "Cairo-VF.ttf")
    row("خط Cairo", "pass" if os.path.exists(fonts) else "warn", fonts, "ييجي مع video-ad-editor")

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
    if "--json" in sys.argv:
        print(json.dumps({"system": SYS, "blocked": BLOCK, "rows": ROWS}, ensure_ascii=False, indent=1))
    return 1 if BLOCK else 0


if __name__ == "__main__":
    sys.exit(main())
