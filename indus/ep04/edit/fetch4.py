import time, hashlib, urllib.request, urllib.parse
UA = "JambudvipaFilesResearch/1.0 (https://youtube.com/@JambudvipaFiles; sathishkumarrbh@gmail.com)"
def get(url):
    for k in range(30):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        except Exception as e: print("retry", k, str(e)[:50], flush=True); time.sleep(120)
def thumb(name, w, out):
    n = name.replace(" ", "_"); h = hashlib.md5(n.encode()).hexdigest(); q = urllib.parse.quote(n)
    data = get(f"https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{w}px-{q}")
    open(out, "wb").write(data); print("saved", out, len(data), flush=True)
thumb("Priest King (Sculpture) of Mohenjo-daro.jpg", 960, "images/pk_ganesh.jpg"); time.sleep(60)
thumb("Priest King.jpg", 1920, "images/pk_soban.jpg")
print("DONE", flush=True)
