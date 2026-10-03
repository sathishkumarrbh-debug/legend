import subprocess,numpy as np,sys
f=sys.argv[1]; th=float(sys.argv[2]) if len(sys.argv)>2 else -35
a=np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True).stdout,np.int16)/32768
b=int(16000*0.025); n=len(a)//b; r=np.sqrt((a[:n*b].reshape(n,b)**2).mean(1)+1e-12); db=20*np.log10(r)
sp=db>th
# merge gaps < 0.15s, drop blocks < 0.08
blocks=[];i=0
while i<n:
    if sp[i]:
        j=i
        while j<n and sp[j]: j+=1
        blocks.append([i,j]); i=j
    else: i+=1
m=[]
for s,e in blocks:
    if m and s-m[-1][1]< 6: m[-1][1]=e
    else: m.append([s,e])
for s,e in m:
    if e-s<3: continue
    seg=db[s:e]; 
    env=''.join(" .:-=+*#%@"[min(9,max(0,int((x+50)/4)))] for x in seg)
    print(f"{s*.025:6.2f}-{e*.025:6.2f} {((e-s)*.025):5.2f}s {env}")
