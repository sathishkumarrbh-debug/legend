import math, json
D,d,L,F=12.0,10.0,200.0,20.0   # mm, mm, mm, N (motor max thrust 10 N x safety factor 2)
I=math.pi*(D**4-d**4)/64; Z=I/(D/2); A=math.pi*(D**2-d**2)/4; M=F*L; s=M/Z
mats=[ # name, density kg/m3, E GPa, yield/strength MPa, approx cost INR/kg
 ('Steel AISI 4130',7850,205,460,250),
 ('Aluminium 6061-T6',2700,69,276,350),
 ('Titanium Ti-6Al-4V',4430,114,880,3500),
 ('GFRP (glass/epoxy)',1900,25,350,700),
 ('CFRP (carbon/epoxy)',1600,70,600,3000)]
rows=[]
for n,rho,E,Sy,c in mats:
    m=rho*1e-9*A*L*1000      # g
    defl=F*L**3/(3*E*1000*I) # mm
    fos=Sy/s; cost=m/1000*c
    rows.append(dict(name=n,rho=rho,E=E,Sy=Sy,ckg=c,mass=m,defl=defl,fos=fos,cost=cost))
# TOPSIS: mass(-) defl(-) fos(+) cost(-)
crit=[('mass',-1,0.35),('defl',-1,0.25),('fos',1,0.20),('cost',-1,0.20)]
for k,sg,w in crit:
    nrm=math.sqrt(sum(r[k]**2 for r in rows))
    for r in rows: r['v_'+k]=w*r[k]/nrm
best={k:(max if sg>0 else min)(r['v_'+k] for r in rows) for k,sg,w in crit}
worst={k:(min if sg>0 else max)(r['v_'+k] for r in rows) for k,sg,w in crit}
for r in rows:
    dp=math.sqrt(sum((r['v_'+k]-best[k])**2 for k,_,_ in crit)); dn=math.sqrt(sum((r['v_'+k]-worst[k])**2 for k,_,_ in crit))
    r['Dp'],r['Dn']=dp,dn; r['C']=dn/(dp+dn)
for i,r in enumerate(sorted(rows,key=lambda r:-r['C'])): r['rank']=i+1
print(f"I={I:.2f} mm4 Z={Z:.2f} mm3 A={A:.2f} mm2 M={M:.0f} Nmm sigma={s:.2f} MPa")
for r in rows: print(f"{r['name']:22s} m={r['mass']:6.2f} g  defl={r['defl']:5.2f} mm  FoS={r['fos']:5.2f}  cost=Rs{r['cost']:6.1f}  C={r['C']:.3f} rank {r['rank']}")
# sensitivity: equal weights, and stiffness-heavy
def topsis(W):
    rr=[dict(r) for r in rows]
    for (k,sg,_),w in zip(crit,W):
        nrm=math.sqrt(sum(r[k]**2 for r in rr))
        for r in rr: r['v_'+k]=w*r[k]/nrm
    b={k:(max if sg>0 else min)(r['v_'+k] for r in rr) for k,sg,_ in crit}; wo={k:(min if sg>0 else max)(r['v_'+k] for r in rr) for k,sg,_ in crit}
    out=[]
    for r in rr:
        dp=math.sqrt(sum((r['v_'+k]-b[k])**2 for k,_,_ in crit)); dn=math.sqrt(sum((r['v_'+k]-wo[k])**2 for k,_,_ in crit)); out.append((r['name'],round(dn/(dp+dn),3)))
    return sorted(out,key=lambda x:-x[1])
print('equal',topsis([.25,.25,.25,.25])); print('perf',topsis([.4,.3,.2,.1])); print('cost',topsis([.25,.15,.15,.45]))
json.dump(dict(I=I,Z=Z,A=A,M=M,sigma=s,rows=rows,eq=topsis([.25]*4),cost=topsis([.25,.15,.15,.45])),open('res.json','w'),indent=1)
