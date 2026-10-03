# History Shorts engine

make_short.py turns your voice recording + a scene plan into a finished 1080x1920 Short with
captions, music, sound effects, AI or real images, video clips, maps and red annotations.

Per episode folder: script.md, scenes.json, images/ (photos, AI images or .mp4 clips).
Shared: sfx/ (ElevenLabs effects), music/ (YouTube Audio Library), fonts/, STYLE.md (the channel playbook).

Run:  python3 make_short.py ep002_roopkund --voice my_recording.mp3 [--tempo 1.1]
Needs: Python 3 (numpy, Pillow, sherpa-onnx for word-accurate sync) and FFmpeg.

Keep this zip. In a new chat, attach it with your voice file and Claude continues from here.
