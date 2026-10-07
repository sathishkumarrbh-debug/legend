import re,sys
P='tpl/x/word/document.xml'; d=open(P,encoding='utf-8').read()
paras=re.findall(r'<w:p>.*?</w:p>',d,re.S)
txt=lambda p:''.join(re.findall(r'<w:t[^>]*>([^<]*)',p))
F='<w:rFonts w:cs="Times New Roman" w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
def run(t,sz=None,b=False,i=False,u=False,sup=False):
    rp=F+('<w:b/><w:bCs/>' if b else '')+('<w:i/><w:iCs/>' if i else '')+(f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>' if sz else '')+('<w:u w:val="single"/>' if u else '')+('<w:vertAlign w:val="superscript"/>' if sup else '')
    t=t.replace('&','&amp;')
    return f'<w:r><w:rPr>{rp}</w:rPr><w:t xml:space="preserve">{t}</w:t></w:r>'
def setruns(p,runs):
    ppr=re.search(r'<w:pPr>.*?</w:pPr>',p,re.S).group(0)
    return '<w:p>'+ppr+''.join(runs)+'</w:p>'
TITLE='Material Selection for a Quadcopter Drone Arm Using Beam Theory and TOPSIS Method'
ABS=open('abs.txt').read().strip()
new=[]
for p in paras:
    t=txt(p)
    if t.startswith('Title ('): p=setruns(p,[run(TITLE,28,b=True)])
    elif t.startswith('Presenting Author'):
        p=setruns(p,[run('[Student 1]',24,b=True,u=True),run('1',24,b=True,u=True,sup=True),run(', [Student 2]',24),run('1',24,sup=True),run(', [Student 3]',24),run('1',24,sup=True),run(', [Student 4]',24),run('1',24,sup=True),run(', [Staff Name]',24),run('2',24,sup=True),run(', Dr. S. R. Sathishkumar',24),run('2,*',24,sup=True)])
    elif t.startswith('Department, Organisation'):
        p=setruns(p,[run('1',22,i=True,sup=True),run('UG Student, ',22,i=True),run('2',22,i=True,sup=True),run('Assistant Professor, Department of Mechanical Engineering, St. Joseph’s College of Engineering and Technology, Thanjavur – 613 403, Tamil Nadu, India',22,i=True)])
    elif t.startswith('*Corresponding'): p=setruns(p,[run('*Corresponding Author E-mail: [email address]',20)])
    elif t.startswith('ABSTRACT'): p=setruns(p,[run('ABSTRACT',22,b=True,u=True)])
    elif t.startswith('You are invited'): p=setruns(p,[run(ABS,22)])
    elif t.startswith('Keywords'): p=setruns(p,[run('Keywords:',22,b=True),run(' Quadcopter drone arm; Material selection; Cantilever beam; TOPSIS',22)])
    new.append(p)
for o,n in zip(paras,new): d=d.replace(o,n,1)
open(P,'w',encoding='utf-8').write(d)
print([txt(p)[:60] for p in new if txt(p)])
