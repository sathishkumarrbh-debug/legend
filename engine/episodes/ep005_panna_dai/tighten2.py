"""Natural pause tightening: each pause = clamp(orig*k, lo, hi), 12 ms fades at every cut, longer holds on chosen gaps."""
import subprocess,re,numpy as np,wave,sys,json
SR=44100
src,dst=sys.argv[1],sys.argv[2]; k=float(sys.argv[3]); lo=float(sys.argv[4]); hi=float(sys.argv[5])
keep={int(a.split('=')[0]):float(a.split('=')[1]) for a in sys.argv[6:]}
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
r=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-42dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
ev=re.findall(r'silence_(start|end): ([\d.]+)',r); tot=len(a)/SR; sil=[]; cur=None
for kk,v in ev:
    if kk=='start': cur=float(v)
    else: sil.append([cur if cur is not None else 0.0,float(v)]); cur=None
if cur is not None: sil.append([cur,tot])
segs=[];t=0
for s,e in sil:
    if s-t>0.06: segs.append([t,s])
    t=e
if tot-t>0.06: segs.append([t,tot])
PRE,POST=0.05,0.10; F=int(0.012*SR)
def piece(s,e):
    p=a[int(max(0,s-PRE)*SR):int(min(tot,e+POST)*SR)].copy()
    r=np.linspace(0,1,F); p[:F]*=r; p[-F:]*=r[::-1]; return p
out=[np.zeros(int(0.06*SR),np.float32)]; gaps=[]
for i,(s,e) in enumerate(segs):
    out.append(piece(s,e))
    if i<len(segs)-1:
        og=segs[i+1][0]-e
        g=keep.get(i, min(max(og*k,lo),hi)); gaps.append((i,round(og,2),round(g,2)))
        out.append(np.zeros(int(max(0,g-PRE-POST)*SR),np.float32))
out.append(np.zeros(int(0.25*SR),np.float32))
v=np.concatenate(out)
with wave.open(dst,'wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(v,-1,1)*32767).astype(np.int16).tobytes())
print(len(segs),'segments',round(tot,2),'->',round(len(v)/SR,2)); print(gaps)
