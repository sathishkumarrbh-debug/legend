import json, time, hashlib, urllib.request, urllib.parse
UA = "JambudvipaFilesResearch/1.0 (https://youtube.com/@JambudvipaFiles; sathishkumarrbh@gmail.com)"
def get(url, tries=12):
    for k in range(tries):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e: print("retry", k, str(e)[:50], flush=True); time.sleep(90)
API = "https://commons.wikimedia.org/w/api.php?"
s = json.loads(get(API + urllib.parse.urlencode({"action": "query", "list": "search", "srnamespace": 6, "srlimit": 15, "format": "json", "srsearch": "unicorn seal Indus"})))
cands = [x["title"][5:] for x in s["query"]["search"]]; print("search", cands, flush=True); time.sleep(60)
files = ["Mohenjo-daro Priesterkönig.jpeg"] + cands[:10]
q = API + urllib.parse.urlencode({"action": "query", "prop": "imageinfo", "iiprop": "size|extmetadata", "format": "json", "titles": "|".join("File:" + f for f in files)})
d = json.loads(get(q)); meta = {}
for p in d["query"]["pages"].values():
    if "imageinfo" not in p: continue
    ii = p["imageinfo"][0]; m = ii["extmetadata"]
    meta[p["title"][5:]] = {"w": ii["width"], "h": ii["height"], "lic": m.get("LicenseShortName", {}).get("value"), "artist": m.get("Artist", {}).get("value", "")[:160], "desc": m.get("ImageDescription", {}).get("value", "")[:200]}
json.dump(meta, open("photo_meta.json", "w"), indent=1); print(json.dumps(meta, indent=1), flush=True); print("META DONE", flush=True)
