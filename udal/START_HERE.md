# Udal Uzhavan (@Udaluzhavan): session starter

Read this file first in any new Udal Uzhavan session. It holds the channel analysis (Oct 2026), the tools already built, and the rules.
Jambudvipa Files work lives in `indus/` and is handled in a separate session: do not touch it from here.

## 1. Channel facts (vidIQ, 3 Oct 2026)
- 3,610 subs, about 965k lifetime views, 93 videos. Subs flat since June 2026 (3,620 → 3,610). Back catalogue earns about 100 views a day.
- Audience: Tamil, mostly women 35 to 54.

### What worked (Jul to Aug 2025)
| Series | Result |
|---|---|
| 7-Day Weight Loss Yoga Challenge (one per day, on schedule) | Announcement 8.6k (213 comments), Day 1 **26.7k** (1,353 likes), Day 2 13.8k, Day 5 8.9k |
| 14-Day HIIT Challenge | Announcement **54k (1,125 comments)**, Day 1 16.2k, Day 2 14.9k |
| Single tips | "HIIT Exercise for Full Body Fat Burn" 51k, "வாக்கிங் போனா எடை குறையுமா?" 16.9k, "Thigh and butt fat" 12.3k |
- Winners were 21 to 31 s long, follow-along and challenge-based, with like rates of 2.5 to 5%.

### What went wrong
1. The "14-day" HIIT challenge took 6 weeks to post (8-day gap between Day 9 and Day 10). Views fell from 15k to 2k, and 1,125 people who had committed were let down.
2. Near silence from Oct 2025 to Sep 2026 (about 6 uploads), with topic drift: English motivation quotes, hair oil, a 2-minute long-form video that got 99 views.
3. The new உண்மையா பொய்யா myth Shorts get reach but not connection:
   - Jaggery: 1.8k views, 2× the channel's normal pace, but a **0.8% like rate** and 1 comment.
   - Lemon water: 1.4k views, 4× normal pace.
   They inform, but don't give people a reason to subscribe.
4. Videos of 52 to 56 s ("10,000 steps", "Knee Part 4") got about 400 views. Titles starting with "Part 4 |" lose cold viewers.

### Plan agreed with Legend
- Relaunch the challenge as **"14 நாள் சவால் 2.0"**. Make all 14 videos BEFORE posting Day 1, then post one a day at a fixed time. Re-use the "comment to join" announcement and pin a playlist.
- Use myth-busting Shorts as the funnel into the challenge. End each one with: myth → "இதை நம்பாதீங்க, இந்த exercise பண்ணுங்க" → Day 1 link.
- Keep Shorts to 25 to 32 s. Stick to three pillars: weight loss, blood sugar, joint/knee pain. No motivation quotes, hair or skin topics.
- Post 1 Short a day, Mon to Sat. Never leave a gap of more than 3 days.

## 2. Tools in this repo (`engine/`)
- `make_short.py`, `make_short2.py`, `tighten2.py`: the editor, timeline editor and pause tightener. Setup: `pip install sherpa-onnx numpy pillow fonttools opencv-python --break-system-packages`.
- **`fxkit.py`: code-built effects.** See the docstring at the top and shorts-studio section 4b. For this channel:
  - `fx.stamp(still, out, "பொய்!", border=False, f=TAMIL_FONT, color=(220,40,40))`: verdict slam (red). Use "உண்மை!" in green (40,170,90) and "பாதி உண்மை" in amber. Start the shot at `word@-t_stamp` so the slam lands on the verdict word, and add the `stamp` sound.
  - `fx.counter(bg, out, 38, prefix="", suffix="%", top="<Tamil label>", f_top=TAMIL_FONT, bar=False)`: stat count-up that holds its final value. Add `count_tick`.
  - `fx.punch_hook(food_still, out, focus, chips_from=<crumbly area>)`: aggressive frame 1. Frame 1 stays crisp for the thumbnail.
  - `fx.ending(...)`: cliffhanger question for two-part topics.
  - `fx.make_sfx("sfx")`: phone-audible stamp, count_tick, heartbeat_phone, clock_tick, paper, stone_tap.
  - RULE: a clip's `dur` must be longer than its shot, or it loops back to frame 0.
- `engine/sfx/*.wav`: synthesized sounds, licence-free.
- **Not in the repo (Legend must upload):**
  - `render_uu.py` and the Udal engine files;
  - a Tamil font (Baloo Thambi 2 800, or `NotoSansTamilLatin-800.ttf`) for `engine/fonts/`;
  - Pixabay/YouTube library music and sounds (not stored in git because of licence redistribution rules). The music used on this channel is "Triumphant Valor" for workouts and warm flute/tabla documentary music for informational videos.

## 3. How files move (cloud session, no Chrome)
- Claude writes prompts (ChatGPT images, ElevenLabs voice text and settings). Legend generates the files and puts them in one Google Drive folder (for example `uu_epXX`).
- The Drive connector only downloads files under 10 MB, so upload files individually, never as one big zip. Decode the saved tool-result JSON with base64.
- Claude cannot hear audio: Legend checks it on a phone. Gemini reviews the cut, and Claude verifies each claim Gemini makes before applying it.
- Deliver the MP4 under 30 MB at about 3.2 Mbps, plus a Tamil SRT, thumbnail and upload_details.md.

## 4. Channel rules (summary; full rules are in the udal-uzhavan-shorts skill)
- Health claims need WHO, NIH or peer-reviewed sources. No dosing or treatment advice. Put a "not medical advice" line in the description.
- Voice: ElevenLabs Meera Conversational Tamil (v3), stability 50%, tempo 1.3. Write numbers as Tamil words in the TTS text and keep digits on screen. Check for repeated words with an RMS envelope, not Gemini.
- Text: no boxes, pills or panels. Baloo Thambi 2 for Tamil, Montserrat Black for English. Slide-up entrance. Captions only for key facts.
- Stock clips: modest and relatable (Pexels/Pixabay). AI people must be fictional. No AI video.
