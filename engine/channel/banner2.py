from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/home/claude/shorts/fonts/Cinzel-Bold.ttf'
GOLD=(236,190,84); WHITE=(245,238,225); SAF=(255,153,51); GRN=(19,136,8)
im=Image.open('/mnt/user-data/uploads/Downloads/jf_banner_raw.png').convert('RGB').resize((2560,1440),Image.LANCZOS)
d=ImageDraw.Draw(im)
def ctext(y,s,size,fill):
    f=ImageFont.truetype(F,size); w=d.textlength(s,font=f)
    x=(2560-w)/2
    sh=Image.new('RGBA',im.size,(0,0,0,0)); sd=ImageDraw.Draw(sh); sd.text((x,y+6),s,font=f,fill=(0,0,0,200))
    im.paste(Image.alpha_composite(im.convert('RGBA'),sh.filter(ImageFilter.GaussianBlur(8))).convert('RGB'))
    ImageDraw.Draw(im).text((x,y),s,font=f,fill=fill)
ctext(565,'JAMBUDVIPA FILES',140,GOLD)
d=ImageDraw.Draw(im); L=640; s=L/3
for i,c in enumerate([SAF,WHITE,GRN]): d.rectangle([1280-L/2+i*s,745,1280-L/2+(i+1)*s,755],fill=c)
ctext(778,'Forgotten stories from every corner of India',50,WHITE)
im.save('jf_banner.png'); im.convert('RGB').save('jf_banner.jpg',quality=92)
