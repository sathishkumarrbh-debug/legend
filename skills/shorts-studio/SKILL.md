---
name: "shorts-studio"
description: "Produce a finished YouTube Short for any of Legend's channels (Indian history, health, others): research, AI-reviewed script, images and AI video clips, music, SFX, edit, AI video review, upload."
---

# Shorts Studio: end-to-end Shorts production for any channel

Legend runs faceless YouTube Shorts channels and may start more. Everything is automated, including the YouTube Studio upload (he watches and confirms the final Schedule/Publish click). Every Short must grab in 2 seconds, hold to the end, be accurate, and leave the viewer with a feeling (pride, wonder, motivation, care), not just information. Legend's standing complaint: accurate, well-edited videos that "don't connect emotionally". Section 3a is the fix.

## Channel profiles
Pick the profile first and read `channels/<name>.md` in the engine. If the channel is new, ask Legend for: name, language, audience, tone, series name, and save a profile.
- **Jambudvipa Files** (@JambudvipaFiles, channel UCRipuuoN8sQeUUhRIKsTiPw, English, Indian history across all regions; Brand Account under sathishkumarrbh@gmail.com). Voice ElevenLabs Yash. No fixed closing slogan (Legend dropped "That's the pride of India"), no on-screen series badge or end card. Exception Legend approved: multi-part series (e.g. **Indus Files**) end on a cliffhanger question animation (`fx.ending`: name reveal, then "BUT WHO WERE THEY?" + "INDUS FILES #2"); each episode still answers its own hook first. Object/mystery topics beat biographies on this channel (Iron Pillar 1.4k vs Panna Dai 166 in week 1). Vary regions (not two South topics in a row). Real photos for real objects, AI images or clips for unrecorded scenes labelled "Artist's impression". Avoid political/communal comparison topics. Branding files in `channel/`. The same Google account also owns the unrelated anime channel Animaezom: always check the channel name in Studio before uploading.
- **உடல் உழவன் / Udal Uzhavan** (@Udaluzhavan, Tamil health and fitness, audience mostly women 35 to 54). Profile in `channels/udal_uzhavan.md`: ElevenLabs Meera Conversational Tamil (Eleven v3) at `--tempo 1.3`, music Triumphant Valor, Pexels/Pixabay stock clips suited to the audience (modest, relatable), ChatGPT 3D stat cards, boxed Tamil captions plus a Tamil SRT. Health claims need medical sources (WHO, NIH, peer-reviewed); no dosing or treatment advice; "not medical advice" line in the description.
- New channels: check the name is unused (YouTube channel search in-page: `/results?search_query=...&sp=EgIQAg%3D%3D`, parse channelRenderer titles) and the handle shows a green tick. Claude may fill the create-channel form, but Legend clicks "Create channel" himself (it creates a Google Brand Account). Then Claude sets banner, picture, description.

## Tools (choose per task, ask Legend if unsure)
ChatGPT Go (best for images and 3D infographic cards), Gemini Pro on the account starting "hari" (`gemini.google.com/u/2/app`; Deep Research, video and audio understanding), Canva Pro, Adobe Express Premium, ElevenLabs (free plan, voice only, see Voice), Pexels and Pixabay (free stock video and sound effects), YouTube Studio Audio Library (claim-safe music, see 5). All via Claude in Chrome on his PC; files pass through his Downloads folder via the device bridge. Ask before every download (what, source, size); he usually approves per episode in one batch. Name downloads yourself: his Downloads listing is huge, so never list the whole folder.
- Typing long prompts into ChatGPT/Gemini: JS `el.focus(); document.execCommand('insertText', false, text)` on `#prompt-textarea` (ChatGPT, then click `[data-testid=send-button]`) or `rich-textarea .ql-editor` (Gemini, then `button[aria-label="Send message"]`). The type action breaks on emoji.
- Uploading a file to any page without a visible file input (Gemini, ElevenLabs, a caption loader): inject `<input type=file>` fixed at top-left, file_upload to it (files under /mnt/user-data/uploads only, NOT outputs: commit to Downloads, stage, then upload; under 10 MB per call, and the 10 MB limit counts across one browser_batch, so upload big parts in separate calls), then paste it: `new DataTransfer()`, `dt.items.add(file)`, dispatch `new ClipboardEvent('paste', {clipboardData: dt, bubbles: true})` on the editor, or assign `dt.files` to the page's own input and dispatch `change`.
- ChatGPT/Gemini images: download with fetch(img.src) + blob anchor (images with alt starting "Generated image" and naturalWidth >= 900, dedupe by src, take the last), then stage from Downloads. Scroll the chat to the bottom first (off-screen images are lazy). Drive a queue of prompts with a small send/wait/download state machine polled from the assistant side; page timers stall in background tabs.
- The browser tool truncates JS output around 1,000 characters: store long answers in `window.__x` and read them in slices. Gemini answers can arrive late or look empty: re-read before concluding.
- Gemini defaults to Flash-Lite: switch the model (Pro, or Extended thinking) before a review.
- Long in-page JS loops time out after 45 s: run them async, store results in `window.__x`, read them in a second call.

## 0. Restore the engine and the asset library
`history_shorts_engine.zip` (Downloads) holds `make_short.py`, `make_short2.py` (timeline editor, Jambudvipa Files since EP3), `tighten2.py`, `models/yunet.onnx` (face check), `STYLE.md`, `LIBRARY.md`, `channels/`, `channel/`, `fonts/` (incl. `NotoSansTamilLatin-800.ttf`), each episode's script.md, scenes.json, upload_details.md, and small graphics. `shorts_audio_library.zip` (Downloads) holds `music/` and `sfx/` (prepared, licensed). Stock clips and AI images are left out (size). Stage both zips and unzip to `~/shorts`. Setup if missing: `pip install sherpa-onnx numpy pillow fonttools opencv-python --break-system-packages`; the Whisper small.en model auto-downloads on first sync. ffmpeg is preinstalled. Both channel sessions save this zip: merge, never overwrite blindly.
**Reuse before downloading (Legend's rule):** check LIBRARY.md first; download only what is missing, add it to the library with source and licence, and re-save the library zip to Downloads. Never download the same music or effect twice.

## 1. Topic and trend check
- Search YouTube in Chrome (in-page fetch of result pages, parse ytInitialData incl. shortsLockupViewModel) for outliers: views far above channel size, 20 to 60 s. Open 3 to 6 of them: read transcripts, screenshot frames at 0.3 s, 3 s, middle, end. Note hook, title pattern, visual style, pacing.
- For an existing channel, read its Studio analytics first (top Shorts, retention, swipe rate, audience) and suggest 3 to 4 titles from what already works there. JBV data: a dark first second lost 56% of viewers; bright moving frame + text hook kept 61%.
- Proven formats: mystery, "how did they do this", discovery story, famous vs unknown, numbered "how X..." lists, myth vs fact (health, e.g. "10,000 steps"), rare photos, survival story, what if.

## 2. Research and fact check (non-negotiable)
1. Claude collects facts from primary/reputable sources (WebSearch/WebFetch).
2. Gemini Deep Research answers the same questions independently.
3. Disagreements go back to the source. Only cited claims enter the script. Chatbots are reviewers, never sources; they invent (EP6: Gemini wrote "everyone inside survived", false). Disputed = "historians/scientists believe"; tradition = "tradition says"; unknown = say unknown or hedge ("somewhere in that chaos"). No myths as fact.
4. Keep a fact-check table in `script.md`.

## 3. Script
- 12 to 15 short spoken lines, 45 to 55 s, about 115 to 130 words.
- Line 1 hook over the strongest visual. Open a question by line 2 or 3; pay it off near the end. A twist every 5 to 8 s. Natural, warm storytelling, not a list of facts. End on an emotional line matched to the channel, a simple action (health), or a loop line.
- Precision traps caught in EP1: "didn't crack" (it did fissure), "one single pillar" (forge-welded pieces), "thinner than a hair" (about hair-thick), "scientists from around the world still come" (unprovable), "monsoon rain" (overstated). Prefer exact, slightly modest wording; it still hooks.
- Quotes are verbatim fragments, attributed ("a policeman inside said").
- Per-line delivery notes, 3 titles (question + one emoji), description with sources and credits.
- Review loop: paste into ChatGPT and Gemini as harsh viewer + retention editor + fact-checker (hook score, swipe line, up to 5 rewrites, inaccuracies, music mood and SFX moments, best title). Verify every flagged claim yourself; reject hype. Keep an accepted/rejected table in script.md and show Legend a short before/after.

### 3a. Make the viewer FEEL (Legend's priority)
- Tell it from inside one place and one night: the point of view of the people there, not a wide history summary.
- A human anchor with real words: a named or described eyewitness and a short verbatim quote.
- Sensory detail the sources support (darkness, sound, water). Fear comes from what they heard, not statistics.
- Arc: fear -> terror -> relief -> grief -> awe/pride. Delay the "answer" until the viewer has met the people who needed it.
- Never weigh lives against a building or object ("thousands died but the temple survived" is wrong; "one rock stood between this flood and the people inside" is right). Give the loss its own line and a pause.
- Silence beats: hold 0.8 to 1.2 s after the climax and after the loss line.

## 4. Visuals
- Real material first, only if licensed: Wikimedia Commons API (record author + licence), Government of India photos under GODL-India (credit the ministry), NASA, Pexels/Pixabay. Label real photos on screen ("REAL PHOTO: PLACE, YEAR"). Never news-channel clips (takedown = copyright strike); "Creative Commons" YouTube uploads are mostly re-uploaded news: unsafe. If no licensed footage exists, tell Legend and use photos + stock + AI.
- Stock video (Pexels, Pixabay) for everyday scenes (walking, parks, people): free for commercial use. Check each clip suits the channel's audience; use `"start"` to pick the best seconds of a long clip, and different start offsets to reuse one clip without repeating the same shot.
- AI images for scenes nobody photographed (ChatGPT preferred). Prompt: vertical 9:16, photorealistic cinematic, period-accurate, "no text, no logos". Check each image for accidental meaning (EP1: a "protective layer" image looked like rust) and inaccurate sacred details (crop out). No children in sensitive scenes (guardrail). For real tragedies use a muted documentary grade on AI images (saturation 0.6, cooler, flatter; `*_doc.png`); glossy golden AI reads as insensitive. Only frame 1 stays bright.
- Each image once (repeats are swipe points; only the hook image may return as a deliberate payoff). The image must match the exact words: no one acts before the narration says it.
- Text: big headlines never repeat words the captions show; use them only for unspoken info, small labels for context. No text over a face: `make_short2.py <ep> --facecheck`, fix with per-shot `cap_y`, `focus`, or `fit: fit`. Thumbnail text off faces too.
- **Stat / infographic cards (ChatGPT, Legend's standard since UU001):** one ChatGPT chat, first prompt sets the style: "premium 3D infographic card, glossy dark navy glass panel with rounded corners and a glowing green edge, fully TRANSPARENT background PNG, landscape; Use ONLY these texts exactly: ...; no other words, no logos; leave an empty strip for my caption". Then "Same exact style again. New card: ..." for each stat (hook number, key %, comparison with ≈, two-row stats with icons, TARGET staircase, COMMENT call to action). The PNGs come with real alpha. AI draws numbers and English only; non-Latin labels (Tamil) are drawn in PIL into the empty strip (`overlays_v2.py`: crop to alpha bbox, resize to 900 to 960 px wide). Scene keys: `overlay`, `overlay_delay`, `overlay_y` (centre, fraction of height). Keep cards off faces.
- AI video clips (Veo, Firefly, Canva): only if they look natural. Legend rejected Gemini/Veo clips on Udal Uzhavan ("feels too AI"); prefer stock video there.
- Cut every 2.5 to 3.5 s; split long lines across two visuals. Map graphic (PIL, animated route/pulsing pin as an .mp4) whenever a place matters; avoid disputed borders.
- First frame doubles as the thumbnail: strongest image + a 2 to 4 word hook readable when paused.
- Look at a contact sheet before rendering and after (one frame per line).

## 4b. Code-built visuals and sounds: fxkit.py (both channels)
The engine ships `fxkit.py` (in `history_shorts_engine.zip`). Use it whenever a moment needs more than a still with a zoom: it renders 1080x1920 MP4 clips that scenes.json uses like any shot, and WAV sounds for `sfx/`. Source and a worked example: `indus/ep01/edit/` in the GitHub repo `sathishkumarrbh-debug/legend`.
- `punch_hook(image, out, focus, chips_from)`: aggressive frame-1 hook. Frame 1 stays crisp (thumbnail), then flash, zoom-blur burst, push-in with decaying shake, steam/dust, and debris cut from the image itself flying at the camera. Legend: the plain punch-in "is not aggressive enough to catch viewers".
- `route_map` / `arc_map`: Natural Earth maps (no national borders). Route line draws in under 1 s on the place names, with the `scribble` sound; a second clip drops the pin on the exact word (`at: word:harappa@-0.7`, `pin_t=0.7`). Gemini: slow map draws are swipe points.
- `counter(bg, out, value, ...)`: count-up that HOLDS the final value; time `window` so it lands on the spoken number. Health: "38%" stat count-ups with a Tamil top label.
- `zoom_rings(image, out, wide, tight, rings)`: push into a real photo and draw gold/red rings on the exact detail the narration names.
- `stamp(image, out, text, label, t_stamp)`: an ink stamp slams onto a photo with shake (+ `stamp` sound). Use for a verdict ("FOREIGN?" was Cunningham's 1875 judgement), then `strike_t=` + `stamped_from_start=True` for the payoff ("That bull was never foreign"). Udal Uzhavan: `border=False`, Tamil font, "பொய்!" red / "உண்மை!" green.
- `ending(image, out, title, question, series)`: title reveal, then the screen darkens and the cliffhanger question takes over (+ braam ~2.2 s in).
- `dust(out)` overlay (mode screen), `blur_box(image, out, box)` to hide AI gibberish text (newspaper headers, signs).
- `make_sfx(folder)`: synthesized, phone-audible (150 Hz to 6 kHz) story sounds: train_chug, train_whistle, hammer_brick2 (crunchy smash; layer library `hit` at -8), stone_reveal (resonant reveal of a small object), stamp, strike, scribble, clock_tick ("one week later"), count_tick, heartbeat_phone, paper, stone_tap. Free and licence-safe; prefer them over generic whooshes.
- RULES: every clip's `dur` must be longer than its shot (a short clip loops to frame 0: the "+2,000" counter fell back to "+0"). Anchor clips to words (`word:<w>@-<t>`) so the animation beat lands on the spoken word. Look at a frame of every new clip before rendering the episode (labels cropped by zoom, transparent strokes drawn as white: draw on a separate RGBA layer).

## 4c. Working from a cloud session (no Chrome on Legend's PC)
- Legend generates images (ChatGPT) and voice (ElevenLabs) from prompts Claude writes, then drops files in one Google Drive folder. The Drive connector downloads files only up to 10 MB (and very large base64 replies can drop the connection): ask for individual files, not zips over 10 MB. Results land in tool-results JSON; decode `content` with base64.
- Wikimedia Commons works via API with a descriptive User-Agent and pauses between calls; download thumbnails only at standard widths (960, 1280, 1920) or originals, else HTTP 429/400.
- The network allowlist is per environment: Legend adds hosts (commons.wikimedia.org, upload.wikimedia.org) in the environment settings.
- Never pick music by ear (Claude cannot hear): print a 2 s RMS envelope of each candidate and align its biggest lift to the climax line (`align_src`, `align_line`); give Legend the alternative.

## 8b. Gemini review lessons (Indus Files #1, scored 7.5)
- Accept: speed up maps, make impact sounds crunchier in the mid band, add a resonant sound when a small object is revealed, replace any shot that "lingers" before a reveal with a moving beat (stamp, push, cut), and remove repeated phrases ("One week later" + "In one week").
- Removing words from a TTS take without re-generating: find the word edges with a 20 ms RMS print + `silencedetect d=0.05`, cut with 12 ms fades, re-run tighten2, then confirm with Whisper (sherpa) that the line reads cleanly.
- "Voice slightly rigid": next time write more v3 tags per line ([curious], [tense], [whispering], [awed]) and try Stability 35 to 40%.

## 5. Music and sound (judge everything as a PHONE speaker hears it)
Legend's EP1 feedback: the music was barely heard and the effects were only "suuu" whooshes. The boom and heartbeat were below 150 Hz (silent on phones) and the music sat 11 dB under the voice.
- Music: licensed AND Content-ID safe. Pixabay tracks can be registered (EP5 "Last Sacrifice" got a claim), so prefer YouTube Studio Audio Library: filter menu -> Genre -> Cinematic -> Apply; rows `ytmus-library-row`, button `#download`, pages `#navigate-after`; Chrome blocks a second download per page, so reload before each. Claude cannot hear: send 60 s clips of 3 to 5 candidates to Gemini to describe and rate for the story arc.
- CONTINUOUS bed, no ducking. The editor auto-levels it: `music_gap_db` (default 6) = how far under the voice it sits in the phone band (300 Hz to 6 kHz). Do not hard-code `music_db`. make_short2: align the track's swell to the climax (`align_src`, `align_line`, `align_at`) and shape it with `music_env` (quieter in fear, swell at the climax, about -5 dB for the loss line).
- Effects: use the library (`sfx/`, see LIBRARY.md): hit_big, hit, braam, rise, tom, taiko, anvil, cannon, metal_ring, shimmer. New downloads go through `sfx/prep_library.py`. `db` means perceived loudness: 0 about voice level, -5 strong, -8 normal, -11 subtle. Effects quieter than about 6 dB under the voice read as "no sound effects"; stacked hits near 0 dB distort. Legend dislikes anvil/iron hits, shimmer and generic whooshes.
- Placement: no automatic whoosh on cuts. Hit on the hook frame, braam on the twist (with `rise` `"at": "before"`), story sounds on exact words (`"at": "word:<word>"`, English ASR only), a drum on punch words, taiko or hit on the proud ending. 6 to 9 effects per Short, never over a key word.
- Check: phone-band RMS of voice vs music vs each effect, then Gemini listens (step 8).

## 6. Voice
- Option A, Legend's own voice: pass all takes to `--voice`, the best-take picker keeps the best version of each line. `--tempo 1.1` to 1.2 only if still slow.
- Option B, ElevenLabs (free plan): English "Yash – Mystery Documentary Narrator" (Multilingual v2, speed 1.08; for emotional stories Eleven v4 with audio tags such as [tense], [whispering], [urgent], [somber], [reverently], [softly], [long pause]; Auto-tag suggests them; each generation gives 2 takes, check with ASR that no tag is spoken; ~900 free credits per take); Tamil "Meera - Conversational Tamil Voice" (Eleven v3, then `--tempo 1.3`). Credit "Voice: ElevenLabs (elevenlabs.io)" and move to a paid plan before monetising.
  - Choosing the voice: the picker may not apply; History > Show details > "Restore settings" on an old item of that voice works.
  - Entering text: execCommand does not register; paste it (ClipboardEvent paste with a DataTransfer holding 'text/plain'). In v4's editor clear old text first (click, ctrl+a, Delete) or the paste appends.
  - Downloading: the player / Generation download icon usually works (rename the long filename via the device shell). If it produces nothing: before playing, hook `HTMLMediaElement.prototype.src`; click a history item (it loads into the player as a `data:audio/mpeg;base64` URI), then `fetch(audio.currentSrc)` -> blob -> anchor download. Do not print the src (the tool blocks it). If `currentSrc` is empty, reload and click the item again.
  - Write numbers as words in the TTS text for non-English voices (Tamil: முப்பத்தெட்டு சதவீதம், not "38%"); keep digits in scenes.json so captions show numbers.
  - Fixing one line: regenerate only that line, then splice it into the raw take at its pauses (numpy, match RMS, 10 ms fades, keep natural gaps) and shift later `line_times` by the added length.
- Check AI takes for repeats/glitches: spectral self-similarity (repeat = high-similarity diagonal at a short lag) and Gemini transcription. Ask Gemini in a FRESH chat with a clip of only that line; a chat primed with "is anything repeated?" invents repeats. Cut real repeats with `voice_cuts`.
- TTS pauses: `tighten2.py src dst 0.6 0.22 1.05 [gapIndex=sec ...]` keeps natural, varied pauses with fades; lengthen emotional gaps. Never cut all pauses to one length ("stutter"). Don't run clean_voice (denoise + compressor) on TTS: it pops after silences; set `"voice_light": true`.
- Never help disguise an AI voice from YouTube. Always declare AI content.

## 7. Edit
`python3 make_short.py <episode> --voice take1.mp3 [take2 ...] [--tempo 1.1]` (Udal Uzhavan). Jambudvipa Files uses `make_short2.py <ep> --voice v.wav` (timeline: shots anchored to words, `--frames`, `--facecheck`; captions timed by the spoken text, so a written "1536" takes the time of "fifteen thirty-six"; later runs reuse `_work/line_times.json`).
Run long renders detached (`setsid nohup ... &`), poll the log with short sleeps (under 2 min per Bash call); a Bash call that hits the limit kills a child render. Never `pkill -f make_short.py`; kill by PID.
scenes.json: title/subtitle, optional badge/end_card, `music`, `music_gap_db`, `captions` {font, raqm, upper, size, max_words, max_chars, y, box, box_alpha}, `asr` (false for non-English), `line_times` [[start,end] per line in cleaned-voice seconds], `voice_cuts` [[a,b]]; per scene: image or .mp4, `start`, move (in/out/left/right/up/down/punch), focus, fit, label, overlay, overlay_delay, overlay_y, circle/arrow, shake, flash, sfx.
- Non-English narration: `asr: false`, then set `line_times` from `silencedetect` on `_work/voice_clean.wav` (after tempo).
- Captions: `box: true` puts a dark pill behind the words (readable over busy footage; Legend wants subtitles in Tamil videos). Keep captions above the Shorts UI safe zone and off the cards.
Output 1080x1920, about -14 LUFS. Check a frame at every line, timings, loudness, music balance.

## 8. AI review of the cut
Upload a small review copy to Gemini (432p about 550 kbps, under 5 MB; 8 MB uploads stall), or the audio as MP3. The paste only works while the Gemini tab is in front: screenshot it first, wait for the thumbnail, then type and send. Ask for an emotion score too. For sensitive stories Gemini may answer empty: re-read later or re-ask "editing craft only". Ask it to listen as a phone viewer: music audible throughout, each effect rated, masked words, mispronunciations and repeats with timestamps, a score out of 10, up to 3 fixes; also attention drops and inaccurate claims. Claude cannot hear audio, so this matters; still verify its claims (timestamps are often off). Send Legend the file (under 30 MB, about 3.2 Mbps) before upload.

## 9. Package and upload (YouTube Studio)
1. Ask Gemini (or ChatGPT) for packaging: title score + alternatives under 60 chars, first 2 description lines, hashtags, tags, pinned comment, settings, publish time. Reject hype. Save to upload_details.md with a decisions table.
2. Confirm the Studio channel is the right one (URL channel ID).
3. `studio.youtube.com/channel/<id>/videos/upload?d=ud` opens the upload dialog. For an MP4 over 10 MB: `split -b 8000000` into /mnt/user-data/uploads, inject one file input per part, file_upload each part in its OWN call, then `new File([p0,p1,p2], name, {type:'video/mp4'})`, check the size, assign via DataTransfer to `input[name=Filedata]`, dispatch `change`. Do not fire a second upload.
4. Title/description: execCommand selectAll + insertText on the two `#textbox[contenteditable=true]`. Not made for kids (`VIDEO_MADE_FOR_KIDS_NOT_MFK`); Show more (`#toggle-button`): altered content `VIDEO_HAS_ALTERED_CONTENT_YES`, tags (set the tags input value with trailing comma + Enter), language, category Education. Verify radios via aria-checked.
5. Subtitles (Video elements > Subtitles > Add > Upload file > With timing): build an SRT from `line_times` + scene texts. Before clicking Continue, override `HTMLInputElement.prototype.click` for file inputs (no native dialog), then assign the SRT to `#captions-file-loader` via DataTransfer and dispatch `change`; check timings in the editor, click Done ("subtitles published").
6. Checks (wait for "No issues found"). A Content ID music claim is not a strike (no reach impact; only monetisation). Visibility: Schedule, type the time ("6:00 PM") in the time field, pick Time zone "(GMT+0530) Local Time". Ask Legend before clicking Schedule/Publish.
7. Replacing a video: YouTube cannot swap the file. Upload the fixed version, then set the old one to Private. Never delete; Legend deletes it himself. An upload closed before publishing stays as a Draft (not public).
8. After it goes public: post and pin the comment, heart and reply to early comments.
- Channel branding uses the same file_upload route; banner at least 2048x1152 with text inside the central 1546x423 safe area; logo must read at 48 px; no national emblems.

## 10. Deliver and keep improving
Send Legend the final MP4 and upload_details.md; update the engine zip, the audio library zip and `channels/` profile in Downloads. After each Short, note what worked (Legend's feedback, reviewer catches, analytics once published) and what a better tool, prompt or technique would change. Update STYLE.md or the channel profile and propose an improvement to this skill (propose_skills, kind improvement) without waiting to be asked. Don't only do what was asked: think about what would make the video better and do it.

## Preferences
- Avoid heavy em dash use in anything written for him.