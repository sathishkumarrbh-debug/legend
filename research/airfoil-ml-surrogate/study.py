import numpy as np, time, json
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score, mean_absolute_error
rng=np.random.default_rng(42)

def naca4(m,p,t,n=80):
    b=np.linspace(0,np.pi,n+1); x=0.5*(1-np.cos(b))
    yt=5*t*(0.2969*np.sqrt(x)-0.1260*x-0.3516*x**2+0.2843*x**3-0.1036*x**4)  # closed TE
    if m==0: yc=np.zeros_like(x); dy=np.zeros_like(x)
    else:
        yc=np.where(x<p, m/p**2*(2*p*x-x**2), m/(1-p)**2*((1-2*p)+2*p*x-x**2))
        dy=np.where(x<p, 2*m/p**2*(p-x), 2*m/(1-p)**2*(p-x))
    th=np.arctan(dy)
    xu,yu=x-yt*np.sin(th),yc+yt*np.cos(th); xl,yl=x+yt*np.sin(th),yc-yt*np.cos(th)
    X=np.concatenate([xl[::-1],xu[1:]]); Y=np.concatenate([yl[::-1],yu[1:]])  # TE lower -> LE -> TE upper (clockwise)
    return X,Y

def hess_smith(X,Y,alpha_deg):
    a=np.radians(alpha_deg); N=len(X)-1
    xm=(X[:-1]+X[1:])/2; ym=(Y[:-1]+Y[1:])/2
    dx=np.diff(X); dy=np.diff(Y); L=np.hypot(dx,dy)
    tx,ty=dx/L,dy/L; nx,ny=-ty,tx            # outward normal for clockwise ordering
    # relative position of each control point i to panel j start, in panel-j local frame
    PX=xm[:,None]-X[None,:-1]; PY=ym[:,None]-Y[None,:-1]
    xl=PX*tx[None,:]+PY*ty[None,:]; yl=PX*nx[None,:]+PY*ny[None,:]
    r1=np.hypot(xl,yl); r2=np.hypot(xl-L[None,:],yl)
    beta=np.arctan2(yl,xl-L[None,:])-np.arctan2(yl,xl)
    lnr=np.log(r1/r2)
    I=np.arange(N); beta[I,I]=np.pi; lnr[I,I]=0.0
    us,vs=lnr/(2*np.pi),beta/(2*np.pi)          # unit source, local
    uv,vv=-beta/(2*np.pi),lnr/(2*np.pi)        # unit vortex, local
    # to global
    Usx=us*tx[None,:]+vs*nx[None,:]; Usy=us*ty[None,:]+vs*ny[None,:]
    Uvx=(uv*tx[None,:]+vv*nx[None,:]).sum(1); Uvy=(uv*ty[None,:]+vv*ny[None,:]).sum(1)
    An=Usx*nx[:,None]+Usy*ny[:,None]; Avn=Uvx*nx+Uvy*ny
    At=Usx*tx[:,None]+Usy*ty[:,None]; Avt=Uvx*tx+Uvy*ty
    Vx,Vy=np.cos(a),np.sin(a)
    A=np.zeros((N+1,N+1)); B=np.zeros(N+1)
    A[:N,:N]=An; A[:N,N]=Avn; B[:N]=-(Vx*nx+Vy*ny)
    A[N,:N]=At[0]+At[N-1]; A[N,N]=Avt[0]+Avt[N-1]; B[N]=-(Vx*tx[0]+Vy*ty[0]+Vx*tx[N-1]+Vy*ty[N-1])
    sol=np.linalg.solve(A,B); q,g=sol[:N],sol[N]
    Vt=At@q+Avt*g+Vx*tx+Vy*ty
    Cp=1-Vt**2
    Fx=-(Cp*nx*L).sum(); Fy=-(Cp*ny*L).sum()
    return -Fx*np.sin(a)+Fy*np.cos(a), Cp.min()

# ---- validation: NACA 0012 vs thin airfoil theory, NACA 2412 alpha_L0 ----
X,Y=naca4(0,0.4,0.12)
al=np.arange(-4,13,2); cl12=[hess_smith(X,Y,a)[0] for a in al]
X2,Y2=naca4(0.02,0.4,0.12); cl2412=[hess_smith(X2,Y2,a)[0] for a in al]
val={'alpha':al.tolist(),'cl0012':np.round(cl12,4).tolist(),'thin':np.round(2*np.pi*np.radians(al),4).tolist(),'cl2412':np.round(cl2412,4).tolist()}
# zero-lift angle of 2412 from linear fit
k,c0=np.polyfit(al,cl2412,1); val['aL0_2412']=round(-c0/k,2); val['slope_0012_perdeg']=round(np.polyfit(al,cl12,1)[0],4)

# ---- dataset ----
N=3000
m=rng.uniform(0,0.06,N); p=rng.uniform(0.2,0.6,N); t=rng.uniform(0.08,0.18,N); a=rng.uniform(-4,12,N)
t0=time.time(); CC=np.array([hess_smith(*naca4(m[i],p[i],t[i]),a[i]) for i in range(N)]); cl=CC[:,0]; cpm=CC[:,1]; t_panel=(time.time()-t0)/N
Xd=np.c_[m*100,p*10,t*100,a]; 
idx=np.arange(N); itr,ite=train_test_split(idx,test_size=0.2,random_state=1)
def mk():
    return {'Linear Regression':LinearRegression(),
        'Random Forest':RandomForestRegressor(n_estimators=300,random_state=1),
        'ANN (MLP)':make_pipeline(StandardScaler(),MLPRegressor(hidden_layer_sizes=(64,64),max_iter=8000,random_state=1,learning_rate_init=0.002))}
res={};preds={}
for tgt,yy in [('CL',cl),('CPmin',cpm)]:
    res[tgt]={}
    for name,mod in mk().items():
        mod.fit(Xd[itr],yy[itr]); t0=time.time(); pr=mod.predict(Xd[ite]); tp=(time.time()-t0)/len(ite)
        res[tgt][name]={'R2':round(r2_score(yy[ite],pr),4),'MAE':round(mean_absolute_error(yy[ite],pr),4),'t_ms':round(tp*1000,5),'speedup':int(t_panel/tp)}
        preds[(tgt,name)]=pr
        if name=='Random Forest' and tgt=='CL': imp=mod.feature_importances_
out={'val':val,'N':N,'t_panel_ms':round(t_panel*1000,2),'res':res,'cl_range':[round(cl.min(),3),round(cl.max(),3)],'cpm_range':[round(cpm.min(),3),round(cpm.max(),3)],
     'rf_importance_CL':dict(zip(['camber','camber_pos','thickness','alpha'],np.round(imp,3).tolist()))}
json.dump(out,open('results.json','w'),indent=1); print(json.dumps(out,indent=1))
yte=cl[ite]; best='ANN (MLP)'
# ---- figures ----
P='#4a1d8c';G='#e2a614';D='#2a0d5c'
plt.rcParams.update({'font.family':'serif','font.serif':['Liberation Serif'],'font.size':13})
fig,ax=plt.subplots(figsize=(6,2.4));
for (mm,pp,tt),c,lab in [((0,0.4,0.12),P,'NACA 0012'),((0.04,0.4,0.12),G,'NACA 4412')]:
    x,y=naca4(mm,pp,tt); ax.plot(x,y,c,lw=2.2,label=lab)
ax.set_aspect('equal'); ax.axis('off'); ax.legend(frameon=False,loc='upper right'); plt.tight_layout(); plt.savefig('fig_airfoils.png',dpi=200,transparent=True)
fig,ax=plt.subplots(figsize=(6,4.2))
ax.plot(al,2*np.pi*np.radians(al),'--',c='grey',lw=2,label='Thin airfoil theory (2πα)')
ax.plot(al,cl12,'o-',c=P,lw=2,label='Panel method – NACA 0012')
ax.plot(al,cl2412,'s-',c=G,lw=2,label='Panel method – NACA 2412')
ax.set_xlabel('Angle of attack α (deg)'); ax.set_ylabel('Lift coefficient $C_L$'); ax.grid(alpha=.3); ax.legend(frameon=False); plt.tight_layout(); plt.savefig('fig_validation.png',dpi=200)
fig,ax=plt.subplots(figsize=(5.6,5))
plt.close('all')
fig,axs=plt.subplots(1,2,figsize=(10,4.6))
for ax,(tgt,lab,yy) in zip(axs,[('CL','$C_L$',cl),('CPmin','$C_{p,min}$',cpm)]):
    for name,c,mk_ in [('Linear Regression','#bbbbbb','x'),('ANN (MLP)',P,'o')]:
        ax.scatter(yy[ite],preds[(tgt,name)],s=14,c=c,marker=mk_,alpha=.75,label=f"{name} (R² = {res[tgt][name]['R2']:.3f})")
    lim=[yy.min(),yy.max()]; ax.plot(lim,lim,'--',c=G,lw=2)
    ax.set_xlabel(lab+' from panel method'); ax.set_ylabel(lab+' predicted'); ax.grid(alpha=.3); ax.legend(frameon=False,fontsize=11,loc='upper left' if tgt=='CL' else 'lower right')
plt.tight_layout(); plt.savefig('fig_parity.png',dpi=200)
x,y=naca4(0.02,0.4,0.12); r=hess_smith(x,y,6)

