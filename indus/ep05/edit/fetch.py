import json, time, urllib.request, urllib.parse, re, sys
UA = "JambudvipaFilesResearch/1.0 (https://youtube.com/@JambudvipaFiles; sathishkumarrbh@gmail.com)"
def get(url):
    for k in range(30):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e: print("retry", k, str(e)[:50], flush=True); time.sleep(120)
API = "https://commons.wikimedia.org/w/api.php?"
for q in ["unicorn figurine Harappa terracotta", "Indus terracotta bull figurine one horn", "Rhinoceros unicornis Kaziranga"]:
    s = json.loads(get(API + urllib.parse.urlencode({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 12,
                                                     "prop": "imageinfo", "iiprop": "size|extmetadata", "format": "json"})))
    print("==", q, flush=True)
    for p in s.get("query", {}).get("pages", {}).values():
        ii = p["imageinfo"][0]; m = ii["extmetadata"]
        print(" ", p["title"][5:], ii["width"], ii["height"], "|", m.get("LicenseShortName", {}).get("value"), "|", re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", ""))[:40], flush=True)
    time.sleep(90)
print("DONE", flush=True)
