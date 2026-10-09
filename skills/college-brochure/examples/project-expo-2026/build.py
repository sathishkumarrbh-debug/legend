L=open('template.html',encoding='utf-8').read().split('\n')
head='\n'.join(L[:68]).replace('<title>FDP Brochure</title>','<title>Project Expo 2026</title>')
script='\n'.join(L[128:])
bulb="""
 // light bulb (idea) instead of AI label
 const bx=26,by=22;
 el('circle',{cx:bx,cy:by-1.2,r:4.2,fill:'#ffd666',stroke:'#ffffff','stroke-width':.6});
 el('rect',{x:bx-1.9,y:by+2.6,width:3.8,height:2.6,rx:.5,fill:'#ffffff'});
 el('line',{x1:bx-1.9,y1:by+3.9,x2:bx+1.9,y2:by+3.9,stroke:'#7b4fd0','stroke-width':.4});
 [[0,-8.2],[-6,-5.6],[6,-5.6],[-7.6,0],[7.6,0]].forEach(([dx,dy])=>el('line',{x1:bx+dx*.78,y1:by-1.2+dy*.78,x2:bx+dx,y2:by-1.2+dy,stroke:'#ffd666','stroke-width':.8,'stroke-linecap':'round'}));
"""
script=script.replace("gear(26,22,9,10,'#ffffff','AI');","gear(26,22,9,10,'#ffffff');").replace(" gear(14,56,5,8,'#7b4fd0');"," gear(14,56,5,8,'#7b4fd0');"+bulb)
DATE='12 October 2026 (Monday)'; TIME='10.30 AM – 12.30 PM'; VENUE='Department of Mechanical Engineering, SJCET'
body=f'''
<div class="pan p1">
 <div class="dots deco" style="left:0;top:0;width:30mm;height:30mm;opacity:.6"></div>
 <svg class="shard" style="left:0;top:0" width="40mm" height="24mm" viewBox="0 0 40 24"><polygon points="0,0 22,0 0,16" fill="#4a1d8c"/><polygon points="0,16 22,0 27,0 0,20" fill="#e2a614"/></svg>
 <div class="title">
  <div class="t" style="font-size:30px;letter-spacing:1px">PROJECT EXPO<br>2026</div>
  <div class="divider"><b></b></div>
  <div class="s">Innovate · Design · Build · Showcase</div>
 </div>
 <div class="bandwrap"><div class="band"><div class="f" style="font-size:20px">MECHANICAL<br>ENGINEERING<br>PROJECT EXHIBITION</div><div class="d">12 October 2026</div><div class="m" style="font-size:13px;margin-top:.6mm">10.30 AM – 12.30 PM</div></div></div>
 <svg class="illus" id="illus" viewBox="0 0 99 80" preserveAspectRatio="none"></svg>
 <div class="logo"><img src="assets/header.webp" alt="College logo"></div>
 <div class="org">
  <div class="lab">Organised by</div>
  <div class="dep">Department of Mechanical Engineering</div>
  <div class="cn">ST. JOSEPH’S COLLEGE OF<br>ENGINEERING AND TECHNOLOGY</div>
  <div class="ad">A.S. Nagar, Elupatti, Thanjavur – 613 403</div>
  <div class="ad">Approved by AICTE, New Delhi · Affiliated to Anna University, Chennai</div>
  <div class="acc"><img src="assets/header.webp" alt="NAAC, Anna University, AICTE"></div>
 </div>
 <svg class="shard" style="left:0;bottom:0" width="34mm" height="20mm" viewBox="0 0 34 20"><polygon points="0,4 30,20 0,20" fill="#4a1d8c"/><polygon points="0,0 34,20 30,20 0,4" fill="#e2a614"/></svg>
</div>

<div class="pan p2">
 <div class="sec"><h3><span>About the Project Expo</span></h3>
 <p>The Project Expo is a platform for Mechanical Engineering students to exhibit their innovative ideas, working models and design projects. It encourages creativity, hands-on skills and teamwork, and gives students the opportunity to present their work to faculty members and interact with peers.</p></div>
 <div class="sec"><h3><span>Department of<br>Mechanical Engineering</span></h3>
 <p style="margin-bottom:3mm">The Department of Mechanical Engineering offers the B.E. Mechanical Engineering programme with well-equipped laboratories and experienced faculty members, and regularly organises industrial visits, seminars, workshops and faculty development programmes.</p></div>
 <div class="sec"><h3><span>Organising Committee</span></h3>
 <div class="cm">
  <div><b>Rev. Sr. P. Mariya Alangaram, DMI</b>Chief Patron &amp; Administrator</div>
  <div><b>Prof. Dr. R. Ravikumar</b>Patron &amp; Principal (i/c)</div>
  <div><b>Mr. M. Sureshkumar</b>Convener &amp; Head of the Department, Mechanical</div>
 </div></div>
 <div class="sec"><h3><span>Coordinators</span></h3>
 <div class="cm" style="display:grid;grid-template-columns:1fr 1fr;column-gap:3mm">
  <div><b>Mr. M. Pradeep</b>AP / Mechanical</div>
  <div><b>Mr. R. Jeevanesan</b>AP / Mechanical</div>
  <div><b>Mr. B. Nagendran</b>AP / Mechanical</div>
  <div><b>Dr. S. R. Sathishkumar</b>AP / Mechanical</div>
 </div></div>
 <div class="sec"><h3><span>Why Participate?</span></h3>
 <div class="why"><div><b>Showcase</b>your ideas and skills</div><div><b>Learn</b>from faculty feedback</div><div><b>Teamwork</b>&amp; communication</div><div><b>Build</b>your project portfolio</div></div></div>
</div>

<div class="pan p3">
 <div class="dots deco" style="right:0;top:0;width:34mm;height:26mm;opacity:.55"></div>
 <h3><span>Expo Themes</span></h3>
 <ul class="themes" style="columns:2;column-gap:4mm;margin-bottom:3mm">
  <li>Design &amp; Fabrication</li><li>Automobile Engineering</li><li>Thermal &amp; Renewable Energy</li><li>Manufacturing &amp; Automation</li><li>Robotics, IoT &amp; Mechatronics</li><li>Sustainable &amp; Low-cost Innovations</li>
 </ul>
 <h3><span>Evaluation Criteria</span></h3>
 <div class="crit">
  <div><b>Innovation</b>&amp; originality</div><div><b>Technical</b>content</div><div><b>Working</b>model / demo</div><div><b>Presentation</b>&amp; Q&amp;A</div>
 </div>
 <h3><span>Guidelines</span></h3>
 <ul>
  <li>Open to Mechanical Engineering students; teams of up to 4 members.</li>
  <li>Bring the working model or prototype with a poster / chart explaining the project.</li>
  <li>Each team gets 5 minutes to demonstrate, followed by questions from the judges.</li>
  <li>Report to the venue by 10.00 AM to set up the stall.</li>
 </ul>
 <div class="box"><b>Event at a Glance</b><br>Date: {DATE}<br>Time: {TIME}<br>Venue: {VENUE}</div>
 <svg class="shard" style="right:0;bottom:0" width="44mm" height="26mm" viewBox="0 0 44 26"><polygon points="44,4 44,26 10,26" fill="#4a1d8c"/><polygon points="44,0 44,4 10,26 5,26" fill="#e2a614"/><polygon points="44,12 44,26 26,26" fill="#2a0d5c"/></svg>
</div>
</div>
'''
extra='''<style>
.crit{display:grid;grid-template-columns:1fr 1fr;gap:2mm;margin-bottom:3.5mm}
.crit div{background:#fff;border:1.2px solid #ddd0f2;border-radius:2mm;padding:1.6mm 2.5mm;font-size:11px;line-height:1.25;color:#333;box-shadow:0 1px 3px rgba(42,13,92,.08)}
.crit b{display:block;color:#4a1d8c;font-size:12.4px}
.p3 ul li{margin-bottom:1.1mm}
.themes li{text-align:left;break-inside:avoid}
.why{display:grid;grid-template-columns:1fr 1fr;gap:2mm}
.why div{background:linear-gradient(135deg,#4a1d8c,#5b2aa6);color:#fff;border-radius:2mm;padding:2mm 2.5mm;font-size:11px;line-height:1.25}
.why b{display:block;color:#ffd666;font-size:12.4px}
</style>'''
open('expo_trifold.html','w',encoding='utf-8').write(head.replace('</head>',extra+'</head>')+body+script)
