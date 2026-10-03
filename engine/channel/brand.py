from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
F='/home/claude/shorts/fonts/Cinzel-Bold.ttf'
GOLD=(232,184,74); SAF=(255,153,51); GRN=(19,136,8); WHITE=(245,240,230)
def bg(w,h):
    y,x=np.mgrid[0:h,0:w]; cx,cy=w/2,h*0.45
    d=np.sqrt(((x-cx)/w)**2+((y-cy)/h)**2)
    base=np.array([70,18,14]); dark=np.array([18,6,6])
    t=np.clip(d*1.6,0,1)[...,None]
    return Image.fromarray((base*(1-t)+dark*t).astype('uint8'))
def ctext(d,y,s,size,fill,w):
    f=ImageFont.truetype(F,size); bw=d.textlength(s,font=f); d.text(((w-bw)/2,y),s,font=f,fill=fill)
def tricolour(d,cx,y,L,th):
    s=L/3
    for i,c in enumerate([SAF,WHITE,GRN]): d.rectangle([cx-L/2+i*s,y,cx-L/2+(i+1)*s,y+th],fill=c)
# profile 800x800
im=bg(800,800); d=ImageDraw.Draw(im)
d.ellipse([40,40,760,760],outline=GOLD,width=10)
ctext(d,215,'PRIDE',150,GOLD,800); ctext(d,385,'OF INDIA',92,WHITE,800)
tricolour(d,400,520,330,14)
im.save('profile.png')
# banner 2560x1440, safe area 1546x423 centred
im=bg(2560,1440); d=ImageDraw.Draw(im)
ctext(d,560,'PRIDE OF INDIA',150,GOLD,2560)
tricolour(d,1280,740,700,12)
ctext(d,785,'Forgotten stories from every corner of India',52,WHITE,2560)
im.save('banner.png')
