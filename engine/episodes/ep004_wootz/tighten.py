import subprocess,re,numpy as np,wave,sys
SR=44100
src,dst=sys.argv[1],sys.argv[2]; cap=float(sys.argv[3]) if len(sys.argv)>3 else 0.28
keep={}  # gap index -> seconds
for a in sys.argv[4:]: k,v=a.split('='); keep[int(k)]=float(v)
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
r=subprocess.run(['ffmpeg','-i',src,'-af','silencedetect=noise=-42dB:d=0.12','-f','null','-'],capture_output=True,text=True).stderr
ev=re.findall(r'silence_(start|end): ([\d.]+)',r); tot=len(a)/SR; sil=[]; cur=None
for k,v in ev:
    if k=='start': cur=float(v)
    else: sil.append([cur if cur is not None else 0.0,float(v)]); cur=None
if cur is not None: sil.append([cur,tot])
segs=[];t=0
for s,e in sil:
    if s-t>0.06: segs.append([t,s])
    t=e
if tot-t>0.06: segs.append([t,tot])
out=[np.zeros(int(0.08*SR),np.float32)]
for i,(s,e) in enumerate(segs):
    p=a[int(max(0,s-0.04)*SR):int((e+0.07)*SR)]
    out.append(p)
    if i<len(segs)-1:
        g=segs[i+1][0]-e-0.11
        g=keep.get(i,min(max(g,0.05),cap))
        out.append(np.zeros(int(g*SR),np.float32))
out.append(np.zeros(int(0.2*SR),np.float32))
v=np.concatenate(out)
with wave.open(dst,'wb') as w: w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((np.clip(v,-1,1)*32767).astype(np.int16).tobytes())
print(len(segs),'segments', round(tot,2),'->',round(len(v)/SR,2)); print([round(s,2) for s,e in segs])
