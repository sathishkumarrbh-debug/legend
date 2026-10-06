import json, time, hashlib, urllib.request, urllib.parse, re
UA = "JambudvipaFilesResearch/1.0 (https://youtube.com/@JambudvipaFiles; sathishkumarrbh@gmail.com)"
def get(url):
    for k in range(30):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e: print("retry", k, str(e)[:50], flush=True); time.sleep(120)
def thumb(name, w, out):
    n = name.replace(" ", "_"); h = hashlib.md5(n.encode()).hexdigest(); q = urllib.parse.quote(n)
    data = get(f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{w}px-{q}")
    open(out, "wb").write(data); print("saved", out, len(data), flush=True)
thumb("Stamp seal and modern impression- unicorn and incense burner (?) MET DP23101.jpg", 1280, "images/unicorn_met.jpg"); time.sleep(60)
API = "https://commons.wikimedia.org/w/api.php?"
fs = ["Priest King (Sculpture) of Mohenjo-daro.jpg", "The Priest King of Moenjo Daro.jpg", "The Priest King.jpg", "Priest King.jpg"]
d = json.loads(get(API + urllib.parse.urlencode({"action": "query", "prop": "imageinfo", "iiprop": "size|extmetadata", "format": "json", "titles": "|".join("File:" + f for f in fs)})))
for p in d["query"]["pages"].values():
    if "imageinfo" not in p: continue
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    print("PK", p["title"], ii["width"], ii["height"], m.get("LicenseShortName", {}).get("value"), re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", ""))[:50], flush=True)
print("DONE", flush=True)
