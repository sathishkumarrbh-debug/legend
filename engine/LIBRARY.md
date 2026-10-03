# Audio library (reuse before downloading anything new)

Everything here is already licensed and prepared. Check this list first; download only what is missing,
then add it here. Kept in the engine (`sfx/`, `music/`) and in `shorts_audio_library.zip` in Downloads.

## Music (`music/`)
| File | Source / licence | Mood | Used in |
|---|---|---|---|
| ancient_civilisations.mp3 | YouTube Audio Library, no attribution needed, monetisable | mysterious, epic build | EP1 (start at 9 s) |

## Sound effects (`sfx/`, ready to use; hit point is at 0 s unless noted)
All prepared by `sfx/prep_library.py`: trimmed to the hit, faded, and "phone-translated" (harmonics + mid boost)
so they are heard on phone speakers. The editor also levels every effect to the same phone loudness, so `db`
in scenes.json means "how loud it is heard" (0 = about voice level, -6 normal, -10 subtle).

| Name | Source / licence | Sounds like | Good for |
|---|---|---|---|
| hit_big | Pixabay "Cinematic Hit" (lordsonny 159487), Pixabay licence | big trailer hit with tail | hook frame, final line |
| hit | Pixabay "Cinematic Impact Hit" (universfield 352702) | tight low impact (weak on phones) | layer only |
| braam | Pixabay "Critical Tension Cinematic Braam Impact" (184273) | deep brass braam | twists ("But here's the twist") |
| rise | Pixabay "Cinematic Riser 03" (414575), cut at its peak | tension swell that ENDS on the cut | `"at": "before"` a reveal |
| tom | Pixabay "Drum Huge Cinematic Tom Hit" (283585) | single huge drum | punch words ("fall", "never") |
| taiko | Pixabay "Taiko Drum" (soundreality 367656), first 2.6 s | drum phrase | proud/ending lines |
| anvil | Pixabay "Anvil noise" (385920) | metal clang | iron, forging, hammer words |
| cannon | Pixabay "Cannon shot" (352459) | cannon blast | battles, cannonball |
| metal_ring | synthesized (numpy) | bell-like metal ring | metal, pillars |
| shimmer | synthesized (numpy) | sparkle | science reveal, "secret" |

Pixabay Content Licence: free for commercial use including monetised YouTube, no attribution required.
Raw downloads are the `px_*.mp3` files. Retired in `sfx/old/`: whoosh and riser (hissy "suuu" noise),
and boom and heartbeat (sub-bass only, silent on phones). The ElevenLabs free-plan effects (hammer, cannon)
were also retired because the free plan is not licensed for commercial use.

## Music added
| triumphant_valor.mp3 | Pixabay "Triumphant Valor" (149014), supplied by Legend, Pixabay licence | motivational, fast | Udal Uzhavan default bed |
