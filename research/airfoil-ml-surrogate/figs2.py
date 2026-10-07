import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
exec(open('study.py').read().split('# ---- validation')[0])
P='#4a1d8c';G='#e2a614'
plt.rcParams.update({'font.family':'serif','font.serif':['Liberation Serif'],'font.size':13})
fig,ax=plt.subplots(figsize=(6,2.6))
for (mm,pp,tt),c,lab in [((0,0.4,0.12),P,'NACA 0012 (symmetric)'),((0.04,0.4,0.12),G,'NACA 4412 (cambered)')]:
    x,y=naca4(mm,pp,tt); ax.plot(x,y,c,lw=2.4,label=lab)
ax.set_aspect('equal'); ax.axis('off'); ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(0.5,-0.02),ncol=2,fontsize=12); plt.tight_layout(); plt.savefig('fig_airfoils.png',dpi=200,transparent=True,bbox_inches='tight',pad_inches=0.05)
# Cp distribution NACA 2412 @ 6 deg
x,y=naca4(0.02,0.4,0.12); a=6
# recompute Cp per panel
import types
src=open('study.py').read(); 
X,Y=x,y; N=len(X)-1
def cp_dist(X,Y,alpha):
    s=open('study.py').read().split('def hess_smith')[1].split('# ---- validation')[0]
    s='def hs2'+s.replace("return -Fx*np.sin(a)+Fy*np.cos(a), Cp.min()","return xm,Cp")
    ns={'np':np}; exec(s,ns); return ns['hs2'](X,Y,alpha)
xm,Cp=cp_dist(X,Y,a)
half=len(xm)//2
fig,ax=plt.subplots(figsize=(6,4.2))
ax.plot(xm[half:],Cp[half:],c=P,lw=2.2,label='Upper surface'); ax.plot(xm[:half],Cp[:half],c=G,lw=2.2,label='Lower surface')
ax.invert_yaxis(); ax.set_xlabel('x / c'); ax.set_ylabel('Pressure coefficient $C_p$'); ax.grid(alpha=.3); ax.legend(frameon=False)
ax.annotate('Suction peak\n($C_{p,min}$)',xy=(xm[half:][np.argmin(Cp[half:])],Cp.min()),xytext=(0.3,Cp.min()*0.75),arrowprops=dict(arrowstyle='->',color='k'),fontsize=12)
ax.set_title('NACA 2412 at α = 6°',fontsize=13); plt.tight_layout(); plt.savefig('fig_cp.png',dpi=200)
print('cpmin',Cp.min())
