# Indus Files #1: prompts for you to run

## A. ChatGPT images (6 images, one chat)

Send the style message first, then each image prompt one at a time. Save them as `ai1.png` … `ai6.png` in the same order.

**Style message (send first):**
> I'm making a vertical YouTube Short about the 1800s discovery of Harappa. For every image I ask for in this chat: vertical 9:16, photorealistic cinematic still, natural film grain, period-accurate clothing and tools, warm dusty Punjab light, shallow depth of field. No text, no letters, no logos, no watermarks. Reply only with the image.

**AI-1 (hook, frame 1, must be bright):**
> A 19th-century steam locomotive crossing a flat Punjab plain on a new railway line. The ballast under the rails is clearly made of broken, old red bricks. Behind the train rises a large eroded mound of ancient brick ruins. Golden morning sun, dust in the air, low camera angle near the rails.

**AI-2:**
> 1860s British India. A British railway engineer in a pith helmet and a pale linen coat stands with Punjabi workers in turbans on a bare dusty plain, looking along an unfinished railway embankment that stretches to the horizon. Wooden sleepers stacked, no rails laid yet. Wide shot.

**AI-3:**
> Punjabi labourers in the 1860s break old red fired bricks into pieces with hammers and load them into woven baskets. A huge mound of ancient brick ruins behind them, partly dug away. Brick dust in the sunlight. Medium shot, hands and hammers in the foreground.

**AI-4:**
> Close-up of a weathered hand of a Victorian archaeologist (white cuffs, tweed sleeve) holding a tiny square dark stone seal, about 3 cm wide, freshly brushed from the soil. Soft late-afternoon light, ancient brick mound blurred behind. The seal shows a carved bull; keep any signs on it blurred and unreadable.

**AI-5:**
> 1924. A wooden desk in a dim study lit by a window: a folded broadsheet newspaper with large photographs of carved stone seals, a magnifying glass, a fountain pen and an open handwritten letter. All text blurred and unreadable. Moody, documentary tone.

**AI-6 (final shot, the goosebump):**
> Dusk. A railway track runs straight across the flat Punjab plain toward the horizon. In the sky above the horizon, like a faint golden memory, rises the reconstructed ancient Indus city of Harappa: flat-roofed baked-brick houses, straight streets, a brick citadel. Deep blue sky, last orange light on the rails. Epic, quiet, awe-inspiring.

**Check each image before saving:**
- no text or modern objects;
- no Mughal domes or temples in the Indus city in AI-6 (Indus cities had flat-roofed brick buildings);
- the train in AI-1 is steam-era.

If anything is wrong, reply "Same exact style again, fix: …".

## B. ElevenLabs voice

**Voice:** Yash – Mystery Documentary Narrator.
**Model:** Eleven v3 (it supports the [tags] below). If the tags get spoken aloud, switch to Multilingual v2, delete the tags, and use the same settings.
**Settings:** Stability 45% (Natural) · Similarity 75% · Style 30% · Speaker boost ON · Speed 1.05.
Generate **once** (you get 2 takes). If one line is wrong, regenerate only that line.

Paste exactly this:

```
[mysterious] In the eighteen hundreds, the British built a railway... with bricks from a lost civilisation.
They were laying a line from Lahore to Multan, and they needed broken brick to hold the tracks.
Near a village called Harappa, they found mounds full of it.
Red. Fired. Perfectly shaped bricks.
[serious] So they smashed them. Enough, an archaeologist later wrote, for about a hundred miles of track.
[softly] In that same mound, he found something tiny.
[whispering] A stone seal. A bull... and six signs no one could read.
He decided it must have come from somewhere else... and moved on.
[long pause] [tense] Nineteen twenty-four. The ruins are finally announced to the world. But no one knows how old they are.
One week later, a professor writes in. These seals match finds from ancient Persia and Mesopotamia.
[dramatic] Over four thousand years old.
In one week, India's known history went back two thousand years.
[reverently] That bull was never foreign. It belonged to a civilisation as old as the pyramids...
[long pause] The Indus Valley Civilisation.
```

Download both takes as `ep01_take1.mp3` and `ep01_take2.mp3`.

## C. What to send me
Put these in **one Google Drive folder named `indus_ep01`**:
- `ai1.png` … `ai6.png`
- `ep01_take1.mp3`, `ep01_take2.mp3`
- `history_shorts_engine.zip` and `shorts_audio_library.zip`, from your Downloads. These are the same editor and music/sound library your current videos use, so the edit matches your existing style.

Then tell me "uploaded". I'll pick the best take for each line, build the timeline, map and timeline graphics, edit, check every frame, and send you the MP4 plus the upload details. If you can, run one Gemini review on the cut (I'll give you the exact prompt).
