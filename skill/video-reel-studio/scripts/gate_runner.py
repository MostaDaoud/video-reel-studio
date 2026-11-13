# -*- coding: utf-8 -*-
"""gate_runner.py — بوابات الجودة الآلية لسكل video-reel-studio.

يقرأ مجلد عمل ويطبع جدول PASS/FAIL مع الدليل، ويكتب gates.json + gates.md.
كل بوابة إمّا blocker (توقف التسليم) أو warn (تنبيه).

  python gate_runner.py <work> [--safe] [--maxmb 29] [--kind reel|motion|web|montage|review] [--json gates.json]

12 بوابة للريل (G-2 · G-1 · G1 · G2 · G3 · G4 · G4c · G4d · G5 · G5b · G6 · G7)،
و14 في وضع review (بزيادة G3r وG8r). G7 بيتغيّر شكله حسب النوع.

لا يعتمد إلا على ffmpeg/ffprobe + ملفات المشروع (caps.json, cut.json, theme.json).
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

OK, BAD, WARN, NA = "pass", "fail", "warn", "na"


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries",
             "format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate,channels,"
             "pix_fmt,color_range,color_space,color_primaries,color_transfer",
             "-of", "json", path])
    if r.returncode != 0:
        return None
    try:
        d = json.loads(r.stdout)
    except Exception:
        return None
    d["_path"] = path
    return d


def dur_of(p):
    d = probe(p)
    try:
        return float(d["format"]["duration"])
    except Exception:
        return 0.0


class Gate:
    def __init__(self, gid, title, level="blocker"):
        self.id, self.title, self.level = gid, title, level
        self.items = []

    def add(self, state, msg, fix=""):
        self.items.append({"state": state, "msg": msg, "fix": fix})

    def result(self):
        states = [i["state"] for i in self.items]
        if BAD in states:
            return BAD
        if WARN in states:
            return WARN
        return OK

    def skip(self, why):
        """مش مطلوب لنوع المشروع ده — مش فشل، ومش تجاهل صامت."""
        self.items.append({"state": NA, "msg": why, "fix": ""})


def g_env():
    g = Gate("G-2", "البيئة")
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preflight.py")
    if not os.path.exists(script):
        g.add(WARN, "preflight.py غير موجود")
        return g
    r = run([sys.executable, script])
    lines = [l for l in (r.stdout or "").strip().splitlines() if l.strip()]
    g.add(OK if r.returncode == 0 else BAD, lines[-1] if lines else "بلا مخرج",
          "شغّل preflight.py وشوف سطر الإصلاح")
    return g


def g_theme(w):
    g = Gate("G-1", "الهوية والألوان")
    p = os.path.join(w, "theme.json")
    if not os.path.exists(p):
        g.add(WARN, "لا theme.json — الافتراضي مستخدم", "شغّل onboard.py apply <work> <slug>")
        return g
    try:
        t = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        g.add(BAD, "theme.json غير صالح: %s" % e)
        return g

    def lum(h):
        h = h.lstrip("#")
        c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
        c = [(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4) for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

    def cr(a, b):
        la, lb = lum(a), lum(b)
        return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)

    for fg, bg, hard in (("ink", "bg", 4.5), ("acc", "bg", 3.0), ("onAcc", "acc", 4.5), ("mut", "bg", 3.0)):
        if fg in t and bg in t:
            c = cr(t[fg], t[bg])
            g.add(OK if c >= hard else BAD, "تباين %s/%s = %.2f" % (fg, bg, c), "عدّل اللون أو شغّل onboard.py new")
    g.add(OK if t.get("font") else WARN, "الخط: %s" % t.get("font", "غير محدد"))
    g.add(OK if t.get("capStyle") else WARN, "نمط الكابشن: %s" % t.get("capStyle", "غير محدد"))
    return g


def g_source(w, kind="reel"):
    g = Gate("G1", "المصدر والوسائط")
    if kind != "reel":
        g.skip("مش مطلوب لنوع %s — مفيش src.mov" % kind)
        return g
    src = os.path.join(w, "src.mov")
    if not os.path.exists(src):
        g.add(BAD, "src.mov غير موجود", "انسخ الفيديو إلى <work>/src.mov")
        return g
    p = probe(src)
    if not p:
        g.add(BAD, "ffprobe فشل على src.mov", "أعد نسخ الملف")
        return g
    d = float(p["format"]["duration"])
    v = [s for s in p["streams"] if s["codec_type"] == "video"]
    a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    g.add(OK if v else BAD, "فيديو: %dx%d" % (v[0]["width"], v[0]["height"]) if v else "لا يوجد مسار فيديو")
    g.add(OK if a else BAD, "صوت: %d قناة" % a[0].get("channels", 0) if a else "لا يوجد مسار صوت — الكابشن بلا كلام")
    g.add(OK if d > 1 else BAD, "المدة %.1f ث" % d)
    return g


def g_cut(w, kind="reel"):
    g = Gate("G2", "خطة القص")
    if kind != "reel":
        g.skip("مش مطلوب لنوع %s — مفيش cut.json" % kind)
        return g
    cut = os.path.join(w, "cut.json")
    cutz = os.path.join(w, "cutz.mp4")
    if not os.path.exists(cut):
        g.add(BAD, "cut.json غير موجود", "شغّل 01_cut_plan.py ثم 03_cut_zoom.py")
        return g
    try:
        c = json.load(open(cut, encoding="utf-8"))
    except Exception as e:
        g.add(BAD, "cut.json غير صالح: %s" % e)
        return g
    segs = c.get("keep") or c.get("segments") or []
    g.add(OK if segs else BAD, "عدد المقاطع: %d" % len(segs), "حدّد keep في cut.json")
    if not os.path.exists(cutz):
        g.add(BAD, "cutz.mp4 غير موجود", "شغّل 03_cut_zoom.py")
        return g
    d = dur_of(cutz)
    g.add(OK if d > 1 else BAD, "مدة القص %.1f ث" % d)
    return g


def g_captions(w, cut_dur, kind="reel"):
    g = Gate("G3", "الكابشن")
    p = os.path.join(w, "caps.json")
    if not os.path.exists(p):
        if kind != "reel":
            g.skip("مفيش caps.json — نوع %s من غير كابشن محروق" % kind)
            return g
        g.add(BAD, "caps.json غير موجود", "شغّل 02_captions.py")
        return g
    try:
        c = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        g.add(BAD, "caps.json غير صالح: %s" % e)
        return g
    cards = c.get("cards") or []
    if not cards:
        g.add(BAD, "لا كروت كابشن")
        return g
    first = float(cards[0].get("s", 99))
    g.add(OK if first <= 1.2 else BAD, "أول كابشن عند %.2f ث" % first, "أول نص لازم يبان بأول ثانية")
    empties = sum(1 for x in cards if not any((w_.get("t") or "").strip() for w_ in x.get("w", [])))
    g.add(OK if empties == 0 else BAD, "كروت فاضية: %d" % empties)
    longest = max((float(x["e"]) - float(x["s"]) for x in cards), default=0)
    g.add(OK if longest <= 8 else WARN, "أطول كرت %.1f ث" % longest, "قسّم الجملة الطويلة")
    fat = sum(1 for x in cards if len(x.get("w", [])) > 9)
    g.add(OK if fat == 0 else WARN, "كروت أكثر من 9 كلمات: %d" % fat)
    if cut_dur:
        last = float(cards[-1]["e"])
        g.add(OK if last <= cut_dur + 1.5 else BAD, "آخر كابشن %.1f / مدة الفيديو %.1f" % (last, cut_dur),
              "شغّل 02_captions.py بعد أي تغيير في القص")
        total = float(c.get("total") or 0)
        g.add(OK if abs(total - cut_dur) < 1.5 else WARN, "caps.total %.1f مقابل %.1f" % (total, cut_dur))
    return g


def g_frames(w, cut_dur, kind="reel"):
    g = Gate("G4", "رسم الفريمات")
    if kind != "reel":
        g.skip("مش مطلوب لنوع %s — الريل هو اللي بيرسم out/*.jpg" % kind)
        return g
    out = os.path.join(w, "out")
    if not os.path.isdir(out):
        g.add(BAD, "مجلد out غير موجود", "شغّل 04_render_frames.js all")
        return g
    n = len([f for f in os.listdir(out) if f.lower().endswith(".jpg")])
    want = int(round(cut_dur * 30)) if cut_dur else 0
    if not want:
        g.add(WARN, "تعذّر حساب عدد الفريمات")
    else:
        g.add(OK if abs(n - want) <= 2 else BAD, "فريمات %d / متوقع %d" % (n, want),
              "أعد 04_render_frames.js all --force")
    return g


def loudness(path):
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        return None
    try:
        j = json.loads(m.group(0))
        return float(j["input_i"]), float(j["input_tp"])
    except Exception:
        return None


# أهداف العلو حسب المنصة. القيم من مستودعات قاس عليها أصحابها، مش قانون منزّل:
#   ig/tiktok −14 (كذلك EBU R128 في bestagentkits/motion-video-skill)
#   bilibili −16 (sukai213/bilibili-ai-video، وcclank/lanshu-create-ai-presenter-video)
#   douyin  −20.5 (Mr-funny/hbg-douyin-code-explainer-video)
#   cinema  −23  (مرجع EBU R128 للبث؛ Mr-funny/hbg-life-simulation بيعمل −22.8 قريب منه)
LOUD = {
    "ig": -14.0, "tiktok": -14.0, "reels": -14.0, "shorts": -14.0,
    "bilibili": -16.0, "douyin": -20.5, "cinema": -23.0,
}


def g_open(final):
    """G4d — الافتتاحية: لازم الصورة تتحرك في أول ثانيتين.

    متوسط |Δ| لكل فريم من tblend+signalstats، معوّض على 30 فريم/ث.
    العتبات من قياس على 4 ملفات حقيقية عندنا (0.00 / 0.15 / 0.83 / never).
    الفكرة من sarpstar/cinecode (scripts/qc.py: hook)، والأرقام قسناها هنا.
    """
    g = Gate("G4d", "الافتتاحية")
    if not final:
        g.add(WARN, "لا ملف نهائي — تخطّي")
        return g
    p = probe(final)
    fps = 30.0
    try:
        v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
        num, _, den = (v.get("r_frame_rate") or "30/1").partition("/")
        fps = float(num) / float(den or 1) or 30.0
    except Exception:
        pass
    thr = 1.0 * (30.0 / fps)
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-t", "3", "-i", final, "-an",
             "-vf", "tblend=all_mode=difference,signalstats,"
                    "metadata=print:key=lavfi.signalstats.YAVG",
             "-f", "null", "-"])
    vals = [float(x) for x in re.findall(r"lavfi\.signalstats\.YAVG=([\d.]+)", r.stderr or "")]
    if not vals:
        g.add(WARN, "تعذّر قياس الحركة")
        return g
    i = next((k for k, x in enumerate(vals) if x >= thr), None)
    if i is None:
        g.add(BAD, "الصورة ثابتة أول 3 ثواني", "حرّك أول مشهد أو قصّ ثانية من البداية")
        return g
    t = i / fps
    msg = "أول حركة عند %.2f ث" % t
    if t > 2.0:
        g.add(BAD, msg, "أول ثانيتين هما اللي يقرر المشاهد يكمل — حرّك من الفريم الأول")
    elif t > 0.8:
        g.add(WARN, msg, "حرّك قبل 0.8 ث لو تقدر")
    else:
        g.add(OK, msg)
    return g


def review_plan(w):
    """خطة ريل المراجعة (plan.json) — من references/pipeline.md §8."""
    p = os.path.join(w, "plan.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


def review_out(plan, w):
    """مجلد الناتج. upstream بيحل المسار النسبي من مكان التشغيل، وإحنا من مجلد الشغل —
    فبنجرّب الاتنين ونسيب اللي موجود."""
    out = (plan or {}).get("out")
    if not out:
        return os.path.join(w, "out")
    if os.path.isabs(out):
        return out
    a, b = os.path.join(w, out), os.path.abspath(out)
    return a if os.path.isdir(a) else b


def review_final(w):
    pl = review_plan(w)
    if not pl:
        return None
    f = os.path.join(review_out(pl, w), (pl.get("name") or "review") + "-final.mp4")
    return f if os.path.exists(f) else None


def review_cover(w):
    pl = review_plan(w)
    if not pl:
        return None
    c = os.path.join(review_out(pl, w), (pl.get("name") or "review") + "-cover-9x16.png")
    return c if os.path.exists(c) else None


def g_review_plan(w):
    """G3r — خطة المراجعة: كل لقطة مصدرها وتوقيتها، والمادة موجودة على الجهاز."""
    g = Gate("G3r", "خطة المراجعة")
    pl = review_plan(w)
    if not pl:
        g.add(BAD, "plan.json غير موجود أو غير صالح", "اكتب الخطة — الشكل بـreferences/pipeline.md §8")
        return g
    shots = pl.get("shots") or []
    g.add(OK if shots else BAD, "اللقطات: %d" % len(shots), "كل جملة لازم لقطة")
    base = pl.get("materials") or w
    base = base if os.path.isabs(base) else os.path.join(w, base)
    miss = [s.get("src") for s in shots
            if s.get("src") and not os.path.exists(os.path.join(base, str(s["src"])))]
    g.add(OK if not miss else BAD, "مواد ناقصة: %s" % ", ".join(map(str, miss[:4])) if miss else "كل المصادر موجودة",
          "صحّح materials أو src في plan.json")
    bad_t = [s.get("id", "?") for s in shots
             if not (isinstance(s.get("t0"), (int, float)) and isinstance(s.get("t1"), (int, float))
                     and float(s["t1"]) > float(s["t0"]))]
    g.add(OK if not bad_t else BAD, "لقطات بلا مدة: %s" % ", ".join(map(str, bad_t[:4])) if bad_t else "كل لقطة لها مدة",
          "t1 لازم أكبر من t0")
    caps = pl.get("captions") or []
    g.add(OK if caps else WARN, "كروت الكابشن: %d" % len(caps), "اكتب captions بكلمات موقوتة")
    last = max((float(c.get("t1", 0)) for c in caps), default=0.0)
    tot = max((float(s.get("t1", 0)) for s in shots), default=0.0)
    if caps and tot:
        g.add(OK if last <= tot + 0.6 else WARN,
              "آخر كابشن %.2f / آخر لقطة %.2f" % (last, tot), "مدّ اللقطة أو قصّر الجملة")
    return g


def g_review_sync(w, final):
    """G8r — المزامنة: عدد فريمات النهائي = مدة الصوت × 30 (نفس فحص review.py finish)."""
    g = Gate("G8r", "المزامنة")
    vj = os.path.join(w, "voice.json")
    if not final or not os.path.exists(vj):
        g.skip("مفيش ملف نهائي أو voice.json — تخطّي")
        return g
    try:
        dur = float(json.load(open(vj, encoding="utf-8"))["dur"])
    except Exception as e:
        g.add(WARN, "voice.json غير مقروء: %s" % e)
        return g
    r = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
             "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", final])
    try:
        n = int((r.stdout or "0").strip().split(",")[0])
    except Exception:
        n = 0
    want = int(round(dur * 30))
    if not n:
        g.add(WARN, "تعذّر عدّ الفريمات")
    else:
        g.add(OK if abs(n - want) <= 1 else BAD, "فريمات %d / متوقع %d" % (n, want),
              "أعد review.py render (الصوت والصورة لازم نفس المدة)")
    return g


def g_audio(w, platform="ig", kind="reel"):
    g = Gate("G5", "الصوت والتسليم")
    cand = [os.path.join(w, "ad-master-cover.mp4"), os.path.join(w, "ad-master.mp4"), os.path.join(w, "ad-final.mp4")]
    if kind == "review":
        cand = [p for p in (review_final(w),) if p]
    f = next((p for p in cand if os.path.exists(p)), None)
    if not f:
        what = "<name>-final.mp4" if kind == "review" else "ad-master / ad-master-cover"
        g.add(BAD, "لا ملف نهائي (%s)" % what,
              "شغّل review.py finish" if kind == "review" else "شغّل 06b_master.sh")
        return g, None
    target = LOUD.get(platform, -14.0)
    l = loudness(f)
    if not l:
        g.add(WARN, "تعذّر قياس العلو")
    else:
        i, tp = l
        g.add(OK if abs(i - target) <= 1.2 else WARN,
              "علو %.1f LUFS (هدف %s %.1f ±1.2)" % (i, platform, target),
              "شغّل 06b_master.sh أو 06c_loudfix.sh")
        g.add(OK if tp <= -1.0 else BAD, "الذروة %.1f dBTP" % tp, "اخفض الذروة (06c_loudfix.sh)")
    return g, f


COLR_TYPES = ("prof", "nclx", "nclc")


def colr_box(path):
    """نوع ملف ألوان الحاوية داخل mp4: prof = ملف sRGB (اللي يفهمه مشغّل أبل) · nclx/nclc = وسوم · فاضي = ما فيه.

    البوكس: [4 بايت حجم][colr][4 بايت نوع]. نتحقق من الحجم والنوع عشان ما نلقى الاسم جوه الـmdat بالغلط.
    """
    try:
        data = open(path, "rb").read()
    except Exception:
        return ""
    i = data.find(b"colr")
    while i > 4:
        if i + 8 <= len(data):
            size = int.from_bytes(data[i - 4:i], "big")
            kind = data[i + 4:i + 8].decode("latin1", "replace")
            if 10 <= size <= 8192 and kind in COLR_TYPES:
                return kind
        i = data.find(b"colr", i + 4)
    return ""


def g_color(final, kind="reel"):
    """G5b — لون التصوير (6.5.2): الريل لازم يطلع بنفس ألوان الآيفون.

    ثلاث علامات مقاسة من الملف النهائي:
      1. مدى اللون — `yuvj*` (full) يعني الخط أخذ مسار ترميز يدوي وقصّ الأحمر ~2٪  ← blocker.
      2. وسوم bt709/tv — ناقصة يعني المشغّل بيخمّن (غالبًا بيظبط، بس مش مضمون)  ← warn.
      3. ملف ألوان الحاوية (colr) — `prof` هو اللي يخلي مشغّل أبل يعرضه زي التصوير؛
         nclx/ما فيه = أفتح ~9 من 255 على أبل  ← warn (عين المستخدم على آيفون).
    الفكرة والأرقام من color-check.sh عند upstream (ريل «عيون»: الأحمر كان ناقص 5 من 255).
    """
    g = Gate("G5b", "لون التصوير")
    if not final:
        g.add(WARN, "لا ملف نهائي — تخطّي")
        return g
    st = ((probe(final) or {}).get("streams") or [])
    v = [s for s in st if s.get("codec_type") == "video"]
    if not v:
        g.add(WARN, "تعذّر قراءة مسار الفيديو")
        return g
    v = v[0]
    pf = (v.get("pix_fmt") or "").lower()
    hard = kind in ("reel", "review")   # وعد اللون عن تصوير الآيفون — الفيلم الموشن والكولاج بلا تصوير
    lvl = BAD if hard else WARN
    if pf.startswith("yuvj"):
        g.add(lvl, "مدى كامل (pix_fmt %s) — الأحمر ينقص ~2٪" % pf,
              "أعد الترميز بـ06_encode.sh (VF_ENCODE يخرج tv) — لا تكتب أمر ffmpeg من عندك")
    else:
        g.add(OK, "المدى %s · %s" % (v.get("color_range") or "—", pf or "—"))
    want = (("color_primaries", "bt709"), ("color_transfer", "bt709"),
            ("color_space", "bt709"), ("color_range", "tv"))
    miss = [k for k, val in want if (v.get(k) or "").lower() != val]
    c = colr_box(final)
    if miss:
        g.add(WARN, "وسوم bt709 ناقصة: %s" % ", ".join(miss),
              "06_encode.sh 6.5.2 يكتبها بـh264_metadata — أعد الترميز")
    else:
        g.add(OK, "وسوم bt709 كاملة")
    if c == "prof":
        g.add(OK, "ملف ألوان الحاوية prof (sRGB) — مشغّل أبل بيعرضه زي التصوير")
    elif c:
        g.add(WARN, "ملف ألوان الحاوية %s مش prof — أبل بيعرضه أفتح ~9 من 255" % c,
              "أعد الترميز بـ06_encode.sh 6.5.2 (+prefer_icc) — الفحص: tools/color-check.sh عند upstream")
    elif miss:
        g.add(lvl, "مفيش وسوم ولا ملف ألوان — اللون بلا مرجع",
              "شغّل 06_encode.sh من نسخة 6.5.2 أو أحدث")
    else:
        g.add(WARN, "مفيش ملف ألوان حاوية — أبل بيعرضه أفتح ~9 من 255",
              "06_encode.sh 6.5.2 يكتب +prefer_icc")
    return g


def g_black(final):
    """G4c — فريمات سوداء / بداية سوداء.

    من aijiduonadegou/Paper-Cut: افحص أول وآخر فريم وحول الانتقالات، ونزّل blackdetect
    على الملف النهائي. أشهر عيب في الرندر أنه يبدأ قبل ما الأصول تحمّل.
    """
    g = Gate("G4c", "الفريم الأسود")
    if not final:
        g.add(WARN, "لا ملف نهائي — تخطّي")
        return g
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", final, "-an",
             "-vf", "blackdetect=d=0.12:pix_th=0.02", "-f", "null", "-"])
    runs = [(float(a), float(b)) for a, b in
            re.findall(r"black_start:([\d.]+)\s+black_end:([\d.]+)", r.stderr or "")]
    if not runs:
        g.add(OK, "لا فريمات سوداء")
        return g
    worst = max(runs, key=lambda t: t[1] - t[0])
    lead = [t for t in runs if t[0] < 0.6]
    if lead:
        g.add(BAD, "الفيديو يبدأ أسود عند %.2f ث (%.2f ث)" % (lead[0][0], lead[0][1] - lead[0][0]),
              "أجّل أول مشهد أو حمّل الأصول قبل الرندر")
    if worst[1] - worst[0] >= 0.6:
        g.add(BAD, "أسود %.2f ث عند %.2f" % (worst[1] - worst[0], worst[0]),
              "افتح sheet.jpg حوالين اللحظة وصلّح المشهد")
    elif worst[1] - worst[0] >= 0.25:
        g.add(WARN, "أسود %.2f ث عند %.2f" % (worst[1] - worst[0], worst[0]))
    return g



def g_package(w, final, maxmb, kind="reel"):
    g = Gate("G6", "حزمة النشر")
    if final:
        size = os.path.getsize(final) / 1048576.0
        g.add(OK if size <= maxmb else WARN, "الحجم %.1f ميقا (الحد %.0f)" % (size, maxmb),
              "28_cover.py --first يضغط تلقائياً" if kind != "review" else "review.py finish بيعمل نسخة خفيفة — سلّمها لو الأصل فوق الحد")
    if kind == "review":
        cov = review_cover(w)
        if not cov:
            g.add(BAD, "كفر المنتج غير موجود", "شغّل review.py cover")
        else:
            p = probe(cov) or {}
            v = [s for s in p.get("streams", []) if s["codec_type"] == "video"]
            g.add(OK if v and v[0]["width"] == 1080 and v[0]["height"] == 1920 else WARN,
                  "الكفر %dx%d" % (v[0]["width"], v[0]["height"]) if v else "تعذّر قراءة الكفر")
            d = os.path.dirname(cov)
            base = os.path.basename(cov).replace("-9x16.png", "")
            g.add(OK if os.path.exists(os.path.join(d, base + "-3x4.png")) and
                  os.path.exists(os.path.join(d, base + "-1x1.png")) else WARN,
                  "كفر 3:4 و1:1 جنب 9:16")
        mob = review_final(w) or ""
        mob = mob.replace("-final.mp4", "-mobile.mp4")
        g.add(OK if os.path.exists(mob) else WARN, "نسخة الجوال: %s" % (os.path.basename(mob) if os.path.exists(mob) else "مفيش"),
              "review.py finish بيعملها")
        g.add(OK if os.path.exists(os.path.join(w, "qa.jpg")) else BAD,
              "qa.jpg (12–17 فريم للمراجعة)", "شغّل review.py finish")
        g.skip("مفيش .srt في وضع المراجعة — الكابشن محروق")
        return g

    cover = os.path.join(w, "cover.jpg")
    if not os.path.exists(cover):
        g.add(BAD, "cover.jpg غير موجود", "شغّل 28_cover.py")
    else:
        p = probe(cover)
        v = [s for s in (p or {}).get("streams", []) if s["codec_type"] == "video"]
        g.add(OK if v and v[0]["width"] == 1080 and v[0]["height"] == 1920 else WARN,
              "الكفر %dx%d" % (v[0]["width"], v[0]["height"]) if v else "تعذّر قراءة الكفر")
        g.add(OK if os.path.exists(os.path.join(w, "cover_grid.jpg")) else WARN, "cover_grid.jpg (9:16 · 4:5 · 1:1)")
        g.add(OK if os.path.exists(os.path.join(w, "cover_phone.jpg")) else WARN,
              "cover_phone.jpg", "شغّل 34_phone_preview.py cover.jpg")
    srt = [f for f in os.listdir(w) if f.endswith(".srt")]
    g.add(OK if srt else WARN, "ملفات الترجمة: %s" % (", ".join(srt) if srt else "لا يوجد"), "شغّل 09_srt.py")
    return g


def g_safe(w):
    g = Gate("G7", "المنطقة الآمنة")
    script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "08_safe_check.js")
    script = script.replace(os.sep + "video-reel-studio" + os.sep, os.sep + "video-ad-editor" + os.sep)
    if not os.path.exists(script):
        g.add(WARN, "08_safe_check.js غير موجود — تخطّي", "ثبّت video-ad-editor")
        return g
    r = run(["node", script, w], cwd=os.path.dirname(os.path.dirname(script)))
    tail = "\n".join((r.stdout or "").strip().splitlines()[-3:])
    g.add(OK if r.returncode == 0 else BAD, tail or "لا مخرج", "افتح safe.jpg وصلّح العنصر")
    return g


BANDS = [
    ("فوق (y 0–150)", "crop=1080:150:0:0"),
    ("تحت (y 1620–1920)", "crop=1080:300:0:1620"),
    ("يمين (x 950، y 1100–1750)", "crop=130:650:950:1100"),
]


def g_safe_film(final, dur, bg="#0B0C0C"):
    """G7 لفيلم موشن: 08_safe_check.js بيقرا compose.html وsfx.json بتوع الريل،
    فبنفحص الفيلم نفسه: بناخد شرايح من المناطق الممنوعة ونقيس أعلى لومة فيها.
    خط على خلفية غامقة = YMAX عالي؛ خلفية فاضية = قريب من لومة الخلفية."""
    g = Gate("G7", "المنطقة الآمنة")
    if not final:
        g.add(WARN, "لا ملف نهائي — تخطّي")
        return g
    h = bg.lstrip("#")
    bg_y = 0.2126 * int(h[0:2], 16) + 0.7152 * int(h[2:4], 16) + 0.0722 * int(h[4:6], 16)
    step = max(1.0, (dur or 40.0) / 10.0)
    ts = [round(0.4 + i * step, 2) for i in range(10)]
    for name, crop in BANDS:
        worst, at = 0.0, 0.0
        for t in ts:
            if t >= (dur or 40.0):
                break
            r = run(["ffmpeg", "-hide_banner", "-nostats", "-ss", "%.2f" % t, "-i", final,
                     "-frames:v", "1", "-vf", crop + ",signalstats,"
                     "metadata=print:key=lavfi.signalstats.YMAX", "-f", "null", "-"])
            m = re.search(r"YMAX=([\d.]+)", r.stderr or "")
            if m and float(m.group(1)) > worst:
                worst, at = float(m.group(1)), t
        lim = bg_y + 60      # الحبيبات بتوصل ~34؛ أي نص حقيقي بيكسر 200
        g.add(OK if worst <= lim else BAD,
              "%s: أعلى لومة %.0f (الحد %.0f)" % (name, worst, lim),
              "عنصر داخل على %.1f ث — حرّكه جوّه" % at if worst > lim else "")
    return g


def g_review_safe(w):
    """G7 لوضع المراجعة: فحص بنيوي من plan.json.

    فحص الشرايح باللومة (g_safe_film) ما ينفعش على تصوير حقيقي — منتج لامع أو شباك بيطلع «نص».
    فبنفحص مكان الكابشن والشارات في الخطة نفسها، ونقول بالسطر إنه فحص بنيوي مش بكسل.
    """
    g = Gate("G7", "المنطقة الآمنة")
    pl = review_plan(w)
    if not pl:
        g.skip("مفيش plan.json — تخطّي")
        return g

    def num(v, d):
        try:
            return float(v)
        except (TypeError, ValueError):
            return float(d)

    caps = pl.get("captions") or []
    bad = [c for c in caps if not (200 <= num(c.get("y", 1548), 1548) <= 1680)]
    g.add(OK if not bad else BAD, "كابشن برّا النص الآمن: %d" % len(bad), "خلّ y بين 200 و1680")
    for key in ("pills", "tags"):
        for it in pl.get(key) or []:
            y = num(it.get("y"), 0)
            if y and (y < 150 or y > 1620):
                g.add(WARN, "%s عند y %.0f" % (key, y), "جوّه كروم انستقرام — حرّكه")
    g.skip("فحص بنيوي من plan.json — الصورة تصوير حقيقي، فحص اللومة بيغلط")
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("work")
    ap.add_argument("--safe", action="store_true", help="يشغّل 08_safe_check.js (أبطأ)")
    ap.add_argument("--maxmb", type=float, default=29)
    ap.add_argument("--platform", default="ig", choices=sorted(LOUD),
                    help="هدف العلو: ig/tiktok/reels/shorts −14 · bilibili −16 · douyin −20.5 · cinema −23")
    ap.add_argument("--kind", default="reel", choices=["reel", "motion", "web", "montage", "review"],
                    help="نوع المشروع: reel · motion · web · montage · review (ريل مراجعة منتج)")
    ap.add_argument("--json", default="gates.json")
    a = ap.parse_args()
    w = os.path.abspath(a.work)

    g_env_r = g_env()
    g0 = g_theme(w)
    g1 = g_source(w, a.kind)
    g2 = g_cut(w, a.kind)
    cut_dur = dur_of(os.path.join(w, "cutz.mp4"))
    g3 = g_captions(w, cut_dur, a.kind)
    g4 = g_frames(w, cut_dur, a.kind)
    g5, final = g_audio(w, a.platform, a.kind)
    g4c = g_black(final)
    g4d = g_open(final)
    g5b = g_color(final, a.kind)
    g6 = g_package(w, final, a.maxmb, a.kind)
    if a.kind == "review":
        g3r = [g_review_plan(w)]
        g7 = [g_review_safe(w)]
        g8r = [g_review_sync(w, final)]
    else:
        g3r, g8r = [], []
        g7 = [g_safe(w)] if (a.kind == "reel" and a.safe) else (
            [] if a.kind == "reel" else [g_safe_film(final, dur_of(final))])
    gates = [g_env_r, g0, g1, g2, g3] + g3r + [g4, g4c, g4d, g5, g5b, g6] + g7 + g8r

    rows, blocked = [], 0
    for g in gates:
        st = g.result()
        if st == BAD:
            blocked += 1
        rows.append({"id": g.id, "title": g.title, "level": g.level, "result": st, "items": g.items})

    out = {"work": w, "kind": a.kind, "blocked": blocked, "results": rows}
    with open(os.path.join(w, a.json), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    md = ["# تقرير البوابات — %s" % os.path.basename(w), ""]
    for r in rows:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}[r["result"]]
        md.append("%s **%s %s** — %s" % (icon, r["id"], r["title"], r["result"]))
        for it in r["items"]:
            if it["state"] == OK:
                continue
            if it["state"] == NA:
                md.append("   - — %s" % it["msg"])
                continue
            md.append("   - %s %s%s" % ("❌" if it["state"] == BAD else "⚠️", it["msg"],
                                        (" · " + it["fix"]) if it["fix"] else ""))
        md.append("")
    with open(os.path.join(w, "gates.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("\n".join(md))
    print("blocked:", blocked)
    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()
