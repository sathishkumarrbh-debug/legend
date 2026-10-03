---
name: "udal-uzhavan-shorts"
description: "Udal Uzhavan (Tamil health) Shorts only: the உண்மையா பொய்யா series rules, text style, voice, music, render_uu.py, checks and delivery. Use with shorts-studio for this channel only."
---

# Udal Uzhavan Shorts (channel-specific rules)

Applies ONLY to உடல் உழவன் / Udal Uzhavan (@Udaluzhavan). Follow shorts-studio for the general workflow; where this file differs, this file wins for this channel. Never apply these rules to Jambudvipa Files or any other channel.

## Channel
- Tamil health, audience mostly women 35 to 54, 3.6k subs, goal 10k.
- Main series since UU005: **"உண்மையா பொய்யா"**, honest food/kitchen myth-vs-fact Shorts, about 30 s, each built on one cited study. Scripts live in the Project doc `claude/UU_Unmaiya_Poiya_final_scripts.md`. Exercise videos stalled (no good exercise stock).
- Health claims need medical sources (WHO, NIH, peer-reviewed); no dosing or treatment advice; "not medical advice" line in the description.

## Script and voice
- Hook line names the food in plain Tamil words people search for (e.g. "எலுமிச்சை சாறு கலந்த வெந்நீர் குடிச்சா…"). Narration runs without interruption.
- Be honest: if there is no good proof, say so, then give what IS proven. Don't open with one food and switch to another without saying why.
- ElevenLabs Meera Conversational Tamil (Eleven v3), stability 50%, then tempo 1.3. Numbers as Tamil words in the TTS text.
- "Restore all" in History also restores the OLD text: clear the box (click, ctrl+a, Delete) and check the character counter equals the new script length before generating.

## Repeat and pronunciation check
- Gemini checks pronunciation: attach the voice as **.m4a** (MP4 attachments spin forever; MP3 is not heard). Never click Gemini's own Upload menu.
- Gemini is NOT reliable for repeats: on UU005 it scored 9.5/10 while "அதனால" was spoken twice (Legend caught it). Always print an RMS energy envelope (25 ms bins) of every phrase between pauses and compare each block's length with its expected syllables. A short phrase taking twice its time, or two near-identical blocks, is a repeat. Cut it with `voice_cuts` and shift later times.
- Gemini's timestamps are wrong; time scenes and captions from `silencedetect` pauses on `_work/voice_clean.wav`.

## Music
- Informational videos: warm Indian documentary music (flute, tabla), kept low (`music_gap_db` about 9). Legend picked flute for EP1. Workout videos: Triumphant Valor. Never pop.

## Visuals
- Pexels/Pixabay stock suited to the audience (modest, relatable). Shortlist from poster images (previews don't play in a background tab), then check every downloaded clip with an ffmpeg contact sheet.
- AI people: fictional, foreign-looking, aged 25 to 30 (must not resemble a real person). Muscle diagrams: male. No Veo/AI video ("feels too AI").

## Text (Legend-approved; keep improving)
- NO boxes, pills, panels or 3D cards. Text drawn straight on the video: thin dark outline plus small tight shadow. Baloo Thambi 2 (800) for Tamil, Montserrat Black for English. Slide-up entrance.
- Captions only for key facts, each shown only while it is spoken: hook question, study name + country, the number, verdict, comment ask. Never "Part" text; never cover faces. Avoid glyphs ✓ ✗ → (render as boxes).
- Upload a Tamil SRT for full subtitles.

## Code-built effects (fxkit.py, see shorts-studio 4b)
Use them inside this channel's text rules (no boxes or panels, Baloo Thambi 2 / Montserrat Black, slide-up text):
- Verdict moment of உண்மையா பொய்யா: `fx.stamp(food_still, out, "பொய்!", border=False, f=<Baloo Thambi 2 path>, color=(220,40,40))` or "உண்மை!" in green (40,170,90), anchored so it slams on the verdict word, with the `stamp` sound. For "partly true" use amber and the text "பாதி உண்மை".
- Stat number: `fx.counter(bg, out, 38, suffix="%", prefix="", top="நீரிழிவு அபாயம்", f_top=<Tamil font>, bar=False)` timed to land on the spoken number (numbers stay digits on screen, words in the TTS text). Add `count_tick`.
- Frame-1 hook on a food still: `fx.punch_hook(still, out, focus, chips_from=<a crumbly food area>, steam=True)` for hot food; it keeps frame 1 crisp for the thumbnail.
- Ending question for a two-part topic: `fx.ending(...)` with Tamil lines (no boxes are drawn).
- Sounds: `fx.make_sfx()` gives phone-audible heartbeat_phone, clock_tick, stamp, count_tick, paper: use them on exact words instead of generic whooshes.
- Ask Gemini for a retention review after every cut (hook score, swipe moments, audibility of every effect on a phone, repeated phrases); apply what is accurate, verify the rest.

## Thumbnail
1080x1920 frame of the strongest food shot, 2 to 3 big Tamil lines (white + yellow) on top with a soft top darkening, series tag "உண்மையா? பொய்யா?" in green near the bottom.

## Render: render_uu.py
`python3 render_uu.py <episode>` reads `<episode>/plan.json`: voice, tempo, voice_trim_start, `voice_cuts` [[a,b]] (seconds after tempo), tail, music (file must be in `~/shorts/music`), music_gap_db, output; scenes [{at, src, start, move, focus_y, reps+transitions+blend}]; overlays [{type clean|title|statA|statB, lines [[text,size,[r,g,b],'ta'|'en']], t0, t1, y}]; sfx [{t,name,db}]. Make 2 to 3 music versions when the music is new, and let Legend pick by ear.

## Deliver
- SendUserFile the MP4 (under 30 MB), SRT, thumbnail and upload_details.md.
- To his PC: `zip -0`, `split -b 14000000`, commit the parts to `Downloads\uu0XX`, then `cat` + `unzip` on the device and compare md5. Deletes are not allowed and unzip cannot overwrite: move old files to `Downloads\uu004_unused\...` first, or `unzip -p file > name`.
- Ask Legend before clicking Schedule/Publish. Avoid heavy em dash use in anything written for him.