import subprocess, re, json, numpy as np, wave, sys
SR=44100
TEMPO=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
TAKES=['Recording.wav','Recording_2.wav','Recording_3.wav','Recording_4.wav','Recording_5.wav','Recording_6.wav','Recording_7.wav','Recording_9.wav','Recording_11.wav','Recording_13.wav','Recording_14.wav','Recording_16.wav']
import os
for k,v in [(a.split('=')[0],a.split('=')[1]) for a in sys.argv[2:]]: TAKES[int(k)]=v
files=['voice2/'+t for t in TAKES]
def load(p):
    raw=subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).copy()
def segs(p,noise=-40,d=0.12):
    r=subprocess.run(['ffmpeg','-i',p,'-af',f'silencedetect=noise={noise}dB:d={d}','-f','null','-'],capture_output=True,text=True).stderr
    tot=len(load(p))/SR; ev=re.findall(r'silence_(start|end): ([\d.]+)',r)
    sil=[]; cur=None
    for k,v in ev:
        if k=='start': cur=float(v)
        else: sil.append([cur if cur is not None else 0.0, float(v)]); cur=None
    if cur is not None: sil.append([cur,tot])
    out=[]; t=0
    for s_,e_ in sil:
        if s_-t>0.08: out.append([t,s_])
        t=e_
    if tot-t>0.08: out.append([t,tot])
    return out
# per-line list of (file, [segments], custom gaps)
plan=[]
for i,f in enumerate(files):
    sg=segs(f); plan.append((f,sg))
lines=[]   # each: list of (audio chunk, gap_before)
def chunk(a,s,e,pre=0.05,post=0.09):
    return a[int(max(0,s-pre)*SR):int((e+post)*SR)]
out_lines=[]
for i,(f,sg) in enumerate(plan):
    a=load(f)
    pieces=[chunk(a,s,e) for s,e in sg]
    gaps=[min(sg[k+1][0]-sg[k][1]-0.14,0.15) for k in range(len(sg)-1)]
    gaps=[max(0.04,g) for g in gaps]
    if i==0: print('L1 segs',[[round(a,2),round(b,2)] for a,b in sg]); gaps[-1]=0.6
    if i==11: gaps[-1]=0.55          # armoury ... on fire
    if False:
        # split: L10 = up to 4.2 s, L11 = rest
        k=max(j for j,(s,e) in enumerate(sg) if e<4.3)
        L10=(pieces[:k+1],gaps[:k]); rest=(pieces[k+1:],gaps[k+1:])
        rest[1][-1]=0.55                          # beat before "Kuyili"
        out_lines.append(L10); out_lines.append(rest); continue
    out_lines.append((pieces,gaps))
LINE_GAP=[0.28]*len(out_lines); LINE_GAP[1]=0.4; LINE_GAP[9]=0.85; LINE_GAP[10]=0.45; LINE_GAP[11]=0.4
buf=[np.zeros(int(0.25*SR),np.float32)]; t=0.25; lt=[]; groups=[]
def fade(x):
    n=min(len(x)//4,int(0.012*SR)); x=x.copy(); x[:n]*=np.linspace(0,1,n); x[-n:]*=np.linspace(1,0,n); return x
for li,(pieces,gaps) in enumerate(out_lines):
    if li>0: buf.append(np.zeros(int(LINE_GAP[li]*SR),np.float32)); t+=LINE_GAP[li]
    g=[]
    for k,p in enumerate(pieces):
        if k>0: buf.append(np.zeros(int(gaps[k-1]*SR),np.float32)); t+=gaps[k-1]
        g.append([t+0.05, t+len(p)/SR-0.09]); buf.append(fade(p)); t+=len(p)/SR
    groups.append(g); lt.append([g[0][0],g[-1][1]])
buf.append(np.zeros(int(0.3*SR),np.float32))
v=np.concatenate(buf); v=v/np.abs(v).max()*0.7
with wave.open('_work/voice_raw.wav','wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((v*32767).astype(np.int16).tobytes())
# scale times for tempo
groups=[[[a/TEMPO,b/TEMPO] for a,b in g] for g in groups]; lt=[[a/TEMPO,b/TEMPO] for a,b in lt]
json.dump({'lt':lt,'groups':groups},open('_work/line_times.json','w'))
print('raw length %.2f s -> %.2f s at tempo %.2f'%(len(v)/SR,len(v)/SR/TEMPO,TEMPO))
for i,(a,b) in enumerate(lt): print(f'  L{i+1:2d} {a:6.2f}-{b:6.2f}')
# enhancement chain
af=(f"atempo={TEMPO}," if abs(TEMPO-1)>0.005 else "")+("highpass=f=80,afftdn=nr=6:nf=-55,"
    "equalizer=f=300:t=q:w=1.0:g=-2.5,equalizer=f=4000:t=q:w=1.2:g=2,equalizer=f=9000:t=q:w=1.0:g=1.5,"
    "deesser=i=0.25,"
    "acompressor=threshold=-20dB:ratio=3:attack=4:release=90:makeup=2,"
    "loudnorm=I=-14:TP=-1.5:LRA=8")
subprocess.run(['ffmpeg','-y','-v','error','-i','_work/voice_raw.wav','-af',af,'-ar',str(SR),'-ac','1','_work/voice_clean.wav'],check=True)
print('ok')
