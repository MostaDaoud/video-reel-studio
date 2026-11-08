# خط الإنتاج — من جملة واحدة إلى ملف جاهز

كل الأوامر تُشغّل من جذر المشروع. `S` = `.opencode/skills/video-ad-editor/scripts`، `W` = مجلد العمل،
`S2` = `.opencode/skills/video-reel-studio/scripts`.

```bash
# ويندوز
PY=python
BASH='C:\Program Files\Git\bin\bash.exe'     # ⛔ مش bash العادي (WSL)
# ماك / لينكس
PY=python3
BASH=bash
```

الأوامر تحت مكتوبة بـ`$PY` و`$BASH` — نفسها على النظامين.

## 0) Brief — إلزامي قبل أي سكربت

المشرف يكتب `W/brief.json`:

```json
{
  "ask": "منتج الفيديو ده",
  "mode": "talking-reel",
  "source": "C:/Users/.../file.mp4",
  "promise": "جملة واحدة: ماذا يفهم المشاهد بعد 3 ثواني",
  "audience": "من",
  "length_s": [45, 75],
  "tone": "خبير هادي",
  "cta": "الورشة",
  "must_keep": ["اسم", "رقم"],
  "offer": "ما يطلبه في النهاية"
}
```

`mode` واحد من: `talking-reel` · `montage` · `podcast` · `motion` · `web-demo` · `cover-only`.
البوابة G0: `promise` موجود؟ `source` موجود؟ الطول معقول؟ لو لأ — سؤال واحد للمستخدم، ومفيش تخمين.

## 1) تجهيز المصدر (G1)

```bash
# نسخ
cp "<source>" "W/src.mov"
# فريمات ساقطة؟
ffprobe -v error -select_streams v -show_entries frame=pts_time -of csv=p=0 "W/src.mov" | $PY -c "import sys;t=[float(x) for x in sys.stdin if x.strip()];g=[(round(a,2),round(b-a,2)) for a,b in zip(t,t[1:]) if b-a>0.07];print(len(g),'gaps',g[:6])"
# إضاءة (بلا تعديل — للمعلومة فقط)
$PY S/25_scopes.py "W"
```

## 2) التفريغ والقص (G2, G3)

```bash
$PY S/01_cut_plan.py "W"
$PY S/_fwadapter.py "W/a.wav" --model medium --language ar --output_dir "W" --output_name a
$PY S/02a_whisper_check.py "W"          # 0 = نظيف
# fixes.json بعدد كلمات مطابق
$PY S/02_captions.py "W"
$PY S/03_cut_zoom.py "W"
```

فيديو طويل (أكثر من ~4 دقائق): `18_long_transcribe.py` ← اختر المقاطع ← `spec.json` ← `20_episode_cuts.py`.

**بوابة G3b (العربية):** وكيل نظيف يقرأ 33 كرتًا ويحكم. أي تصحيح **بعدد كلمات ثابت**.

## 3) التصميم (G4b)

```bash
$PY S/35_moves.py plan --title "…"      # بانك الحركات
$PY S/11_behind_text.js "W" build 9 35 38
node S/04_render_frames.js "W" preview 1.5 12 28 41
$BASH S/07_contact_sheet.sh "W" "W/sheet.jpg" 1.5 12 28 41
```

اقرا `sheet.jpg` لوحدها. مش 6 صور لوحدهم. صلّح وبعدين أعد.

## 4) الرسم (G4)

```bash
node S/04_render_frames.js "W" all --force
```

عدد الفريمات لازم = المدة × 30.

## 5) التجميع والماستر (G5)

```bash
$BASH S/06_encode.sh "W" "W/ad-final.mp4"
$BASH S/06b_master.sh "W" "W/ad-final.mp4" "W/ad-master.mp4"
$PY S/09_srt.py "W" ad-master
```

## 6) الحزمة (G6, G6b)

```bash
$PY S/28_cover.py "W" "سطر|*أكسنت*" "سطر صغير" --t 6 --first "W/ad-master.mp4"
$PY S/34_phone_preview.py "W/cover.jpg"
$PY S/33_thumb.py "W" "عنوان|*أكسنت*" --video "W/cutz.mp4" --t 20   # ثمبنيل يوتيوب
```

`28_cover --first` يضغط تلقائيًا لـ29 ميقا ويضيف `alimiter` — لا تضغط مرتين.

## 7) البوابات والتسليم

```bash
$PY S2/gate_runner.py "W" --safe      # S2 = مجلد هذا السكل/scripts
```

كل حاجة pass؟ سلّم. فيه blocker؟ صلّح وأعد **البوابة بس**.

## أوضاع أخرى (نفس البوابات، سكربتات مختلفة)

| الوضع | المسار |
|---|---|
| `montage` | `12_montage.py scan/plan/build` (يحتاج 10–20 مقطعًا + مسار صوتي) |
| `podcast` | `15_podcast.py` / `22_hook.py` / `24_podcast_wide.py` (كاميرتان) |
| `motion` | `motion/voice.py` (أو `--own`) ← `timeline.py` ← `render.js all` ← `audio.py` |
| `web-demo` | `27_web_capture.js` ← `30_demo.js` أو `31_device3d.js` |
| `cover-only` | `28_cover.py` + `33_thumb.py` |

`motion` بلا تعليق: `audio.py --no-bed --lufs -20`.
3D على هذا الجهاز: `GL=gpu` و`CHROME` مضبوط.


## ملاحظات منصّة

- **كروم:** لو مش في المسار الافتراضي، مرّر `CHROME=/path/to/chrome` قبل أمر الرسم أو الكفر.
- **3D:** ويندوز/لينكس `GL=gpu` (ANGLE)؛ ماك Metal تلقائي.
- **الحروف:** الخطوط في `video-ad-editor/motion/fonts/` — تُحمّل من الملف مش من النظام، فالشكل واحد على النظامين.
- **المسارات:** ماك حساس لحالة الأحرف — `Work` ≠ `work`. خُد المسار من `pwd` مش من الذاكرة.
- **صلاحيات:** أول تشغيل على ماك ممكن يطلب إذن الكاميرا/الشاشة لو استخدمت التقاط الشاشة.
