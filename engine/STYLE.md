# Channel playbook (every episode)

## What the top Indian history Shorts do (studied Sept 2026)
Studied: Keerthi History (face, 32M views, "Mysterious Indian Mummy"), World's Mysterious Facts (17.5M, 21 s visual puzzle),
Stay4ever "Closed Files" series (46M, map + evidence board), Keerthi "How Mughal Emperors Died" (5.9M, numbered list),
Omar Agamy "What India invented" (18.6M, comment-reply format), S H A B A Y "Rajendra Chola" (8.8M, film clips + captions).

1. **Hook contrasts something famous with something unknown in the first 2 seconds.**
   "When we hear mummy we think Egypt... but did you know India has its own?"
2. **A concrete discovery moment early**: a date, a place, a person who found it ("In 1975 an earthquake... a soldier struck a skull").
3. **Question titles with one emoji**: "How is it possible? 🤯", "How Mughal Emperors Died?", "Why so much hype for...?"
4. **Formats that break out**: unsolved mysteries, "how X died" numbered lists, comparisons, rare photos, "what if", how people lived or dressed.
5. **Length**: the big hits are 20 to 60 seconds. Recent 1.5 to 3 minute uploads get a fraction of the views. Stay under 55 s.
6. **Visuals never sit still**: satellite map zoom-ins, red arrows and circles pointing at the detail, evidence boards with photos and red string,
   Mughal miniature paintings, short centred captions of 3 to 5 words.
7. **Series branding** ("CF-EP-1 Closed Files") makes people follow for the next episode.
8. **Avoid**: political or communal comparison topics (they spike but invite strikes and fights), film clips (copyright claims).

## Script rules
- Line 1 = hook (famous vs unknown, or impossible-sounding fact), strongest image, boom.
- Open a question by line 2 or 3 and answer it only near the end.
- A twist every 5 to 8 seconds: "Wrong.", "But here's the twist", "Nobody knows".
- 12 to 14 short spoken lines, 45 to 55 seconds, one picture per line.
- Last line trails off or loops into line 1.
- Real facts only. Disputed claims get "historians believe". No myths presented as fact.
- Real photos for real objects; AI images only for scenes nobody photographed, labelled "Artist's impression".

## Sound rules (automatic in the editor)
- Music: YouTube Audio Library "Ancient Civilisations" (free, no attribution), starts 9 s in, ducks under the voice.
- Whoosh on every cut, boom + shake + flash on twist lines, riser before reveals, heartbeat under mystery lines,
  story sounds on the exact word (cannon on "cannonball", hammer on "forged").

## Edit upgrades for EP2 onward (after EP1)
- More motion: 3 to 4 AI video clips per Short (hook, twist, climax, ending), not 1. Stills only between them.
- Cut every 2.5 to 3.5 s; split long lines across two visuals.
- First frame = thumbnail: strongest image + 2 to 4 word hook text that is readable when paused.
- Vary sound design: a signature channel sting in the first second, fewer generic whooshes, one silence beat before the twist.
- Map or arrow graphic whenever a place is named (Udayagiri deserved one).
- Captions: keep, but move slightly above the YouTube UI safe zone and never cover faces or the subject.

## Retention data (Studio, 30 Sept 2026) and the rules that follow
| Short | Stayed to watch | Avg view | Opening |
|---|---|---|---|
| EP1 Iron Pillar (53 s) | 61.0% | 0:36 (68%) | bright real photo of the pillar, voice in the first second |
| EP3 Kuyili (59 s) | 43.8% | 0:52 (88%) | 0.8 s of pure black, tiny flame, footsteps, then a dark image |
Lesson: Kuyili's story held almost everyone who stayed (88%), but the dark opening lost more than half in the first second.
1. Frame 1 must be the most striking, BRIGHT, readable image already moving. Never open on black or a near-black frame.
2. Put a 3 to 5 word text hook on screen from 0.0 s (big, centre-top), e.g. "SHE WALKED IN ON FIRE". Captions alone are not enough.
3. First spoken words = the shock or the question, not a date. Dates go second ("She walked into an armoury on fire. 1780.").
4. Save darkness and suspense beats for after second 3, once the viewer has committed.
5. Keep the proven parts: fast cuts, honest tradition labels, big explosion, real memorial photo at the end.
Viewer request (Iron Pillar comments): "Damascus sword" -> make the Wootz steel episode next.

## Lessons from EP5 Panna Dai (Oct 2026)
- Never show a big headline that repeats the narration; captions already show those words (Legend: "captions repeating"). Headlines only for words NOT spoken (e.g. a name at the end), small labels for context ("UDAIPUR TODAY", "AS TOLD IN TRADITION").
- No on-screen text may cover a face. Run `python3 make_short2.py <ep> --facecheck` (YuNet face detector, models/yunet.onnx) before every render; fix with per-shot `cap_y`, headline_y, or hook "y". Hook text can sit low (y 0.60) when the face is in the upper half.
- Use each AI image once (the hook image may return only as the final loop shot). Gemini flagged every repeat as a swipe point. Order one extra image per long line.
- Hook motion: use "punch" (instant 18% push) plus glint and embers on frame 1; the slow 1.0 to 1.12 zoom read as "static" (hook 4/10 -> 6/10).
- SFX must be within about 6 dB of the voice in the phone band or reviewers say "no sound effects"; but stacked hits at -1 dB risk distortion. Story sounds (distant shouting, footsteps, door burst) beat generic hits.
- Animate maps (route line drawing, pulsing pin) instead of a static map; real photos need z [1.05, 1.3] movement.
- Gemini may return an empty answer the first time for sensitive stories (child death); wait and read again, it often answers late.
- TTS voice prep: use `tighten2.py src dst 0.72 0.22 0.72 [gap=sec ...]` (keeps natural, varied pauses, 12 ms fades, longer holds on emotional beats). The old fixed-cap tighten.py made every pause identical with hard cuts (Legend heard "stutter").
- Do NOT run make_short.clean_voice (afftdn + compressor) on ElevenLabs takes: it pops on every speech onset after digital silence. Use `highpass=f=80,volume=7dB,alimiter=limit=0.8:attack=7:release=120:level=disabled` and write _work/voice_clean.wav yourself.
- Captions are timed by the SPOKEN text and snapped to pauses (make_short2 word_times_snap + caption_times): a written "1536" takes the time of "fifteen thirty-six". Before, captions ran ahead of the voice.
- Images must match the exact moment: no character doing an action before the narration says it (EP5: Panna was already pointing when Banvir burst in).

## Indus Files #1 (day 1, 3 Oct 2026): code-built hook works
| Short | Stayed to watch | Avg view | Likes | Opening |
|---|---|---|---|---|
| Indus Files #1 "They Smashed a 4,500-Year-Old City for a Railway" (57 s) | 62.1% | 0:39 (69.6%) | 23 on 625 views (3.7%) | fx.punch_hook: crisp frame 1, push-in, shake, flying brick chips, steam |
- Ties the channel best (Iron Pillar 61%) and beats Kuyili (43.8%) by 18 points. Like rate 3.7% is healthy; comments are weak (1).
- Keep: aggressive code-built hook, word-anchored animations, cliffhanger ending.
- Next: get comments with a debate question in the pinned comment and in replies, not in the video ending (the ending stays the Part 2 cliffhanger). Post Part 2 within about 48 h while the topic is fresh.

## Indus Files #2 (first 4 h): hook fine, middle leaked
Stayed to watch 66.8% but AVD 0:25 of 0:55 (46%) vs Part 1 AVD 0:54 of 0:57.
Cause: 0:10-0:25 stacked three unfamiliar names + a date (Sargon, Akkad, Meluhha, 2300 BC) and a list of facts with no question; the best twist (the interpreter) came at 0:30.
Rules: one thread; at most one new proper noun per 10 s; first twist by about 0:20, second by 0:25; replace fact lists with a relatable analogy ("learning English from car number plates"); talk to "you".
- Legend (Part 3): clever analogies and jargon (bilingual, Rosetta, number plates) made the script HARDER. Write like telling a friend: short sentences, everyday words, one idea per line; names go on screen, not in the voice.
