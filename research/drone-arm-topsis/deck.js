const pptxgen=require('pptxgenjs');const {applyTheme}=require('/root/.claude/skills/synced/45b7e87e-ac83-452a-89b7-74bd0de926e7_3d9968d9-88c4-400f-b210-6b62be8e5894/pptx/scripts/apply_theme.js');
const R=require('./res.json');
const THEME={name:'SJCET Purple Gold',headFontFace:'Times New Roman',bodyFontFace:'Calibri',
 colors:{dk1:'1F1F1F',lt1:'FFFFFF',dk2:'2A0D5C',lt2:'F3EEFB',accent1:'4A1D8C',accent2:'E2A614',accent3:'7B4FD0',accent4:'B9B9B9',accent5:'2A0D5C',accent6:'FFD666',hlink:'4A1D8C',folHlink:'7B4FD0'}};
const pres=new pptxgen();pres.layout='LAYOUT_WIDE';pres.theme={headFontFace:THEME.headFontFace,bodyFontFace:THEME.bodyFontFace};
pres.title='Material Selection for a Quadcopter Drone Arm';pres.author='Department of Mechanical Engineering, SJCET';
const C=pres.SchemeColor;const FOOT='ICAAN–2026  |  St. Joseph’s College of Engineering and Technology, Thanjavur';
pres.defineSlideMaster({title:'TITLE_DARK',background:{color:'2A0D5C'},objects:[]});
pres.defineSlideMaster({title:'CONTENT',background:{color:'FFFFFF'},margin:[0.5,0.6,0.6,0.6],
 objects:[{text:{text:FOOT,options:{x:0.6,y:7.0,w:9,h:0.3,fontSize:10,color:'8A8A8A',fontFace:'Calibri'}}},
  {placeholder:{options:{name:'title',type:'title',x:0.6,y:0.35,w:12.1,h:0.9,fontSize:34,bold:true,color:C.text2,fontFace:'Times New Roman',valign:'middle',margin:0},text:''}}],
 slideNumber:{x:12.2,y:7.0,w:0.6,h:0.3,fontSize:10,color:'8A8A8A',align:'right'}});
pres.defineSlideMaster({title:'PURPLE',background:{color:'4A1D8C'},objects:[],slideNumber:{x:12.2,y:7.0,w:0.6,h:0.3,fontSize:10,color:'D9CCF2',align:'right'}});
let sec='';function S(m,s){if(s!==sec){pres.addSection({title:s});sec=s}return pres.addSlide({masterName:m,sectionTitle:s})}
const T=(sl,t)=>sl.addText(t,{placeholder:'title'});
function num(sl,n,x,y,d=0.55){sl.addShape(pres.shapes.OVAL,{x,y,w:d,h:d,fill:{color:C.accent2},line:{color:C.accent2}});
 sl.addText(String(n),{x,y,w:d,h:d,align:'center',valign:'middle',fontSize:18,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'})}
function card(sl,x,y,w,h,fill){sl.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:0.12,fill:{color:fill||'F3EEFB'},line:{color:fill||'F3EEFB'},shadow:{type:'outer',color:'000000',opacity:0.12,blur:6,offset:2,angle:90}})}
const body=(sl,arr,o)=>sl.addText(arr.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<arr.length-1}})),Object.assign({fontSize:18,color:'1F1F1F',paraSpaceAfter:10,valign:'top',isTextBox:true},o));
const rows=R.rows;const short=n=>n.split(' (')[0].replace('Aluminium 6061-T6','Al 6061-T6').replace('Titanium Ti-6Al-4V','Ti-6Al-4V').replace('Steel AISI 4130','Steel 4130');
const names=rows.map(r=>short(r.name));
function bar(sl,title,vals,x,y,w,h,fmt){sl.addChart(pres.charts.BAR,[{name:title,labels:names,values:vals}],{x,y,w,h,barDir:'col',showTitle:true,title,titleFontSize:16,titleColor:'2A0D5C',titleFontFace:'+mj-lt',
 chartColors:['4A1D8C'],showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:fmt,dataLabelFontSize:12,dataLabelColor:'1F1F1F',dataLabelFontFace:'+mn-lt',
 catAxisLabelColor:'444444',valAxisLabelColor:'666666',catAxisLabelFontSize:12,valAxisLabelFontSize:11,catAxisLabelFontFace:'+mn-lt',valAxisLabelFontFace:'+mn-lt',
 valGridLine:{color:'E5E5E5',size:0.75},catGridLine:{style:'none'},showLegend:false,barGapWidthPct:60})}

// 1 Title
let s=S('TITLE_DARK','Introduction');
s.addImage({path:'logo.png',x:0.6,y:0.45,w:1.15,h:1.15});
s.addText([{text:'St. Joseph’s College of Engineering and Technology, Thanjavur',options:{breakLine:true,bold:true}},{text:'Department of Mechanical Engineering'}],{x:1.95,y:0.55,w:10,h:0.95,fontSize:16,color:'FFFFFF',isTextBox:true,margin:0});
s.addText('Material Selection for a Quadcopter Drone Arm Using Beam Theory and TOPSIS Method',{x:0.6,y:2.0,w:12.1,h:1.9,fontSize:40,bold:true,color:'FFFFFF',fontFace:'Times New Roman',isTextBox:true,margin:0,valign:'middle'});
s.addText('Track: Propulsion and Structures',{x:0.6,y:3.95,w:12,h:0.45,fontSize:18,italic:true,color:'FFD666',isTextBox:true,margin:0});
s.addText([{text:'Dr. S. R. Sathishkumar, [Staff Name]',options:{breakLine:true,bold:true}},{text:'[Student 1], [Student 2], [Student 3], [Student 4]'}],{x:0.6,y:4.8,w:12,h:0.95,fontSize:18,color:'FFFFFF',isTextBox:true,margin:0});
s.addText('ICAAN–2026  ·  Saranathan College of Engineering, Tiruchirappalli  ·  15–16 October 2026',{x:0.6,y:6.55,w:12,h:0.4,fontSize:13,color:'D9CCF2',isTextBox:true,margin:0});
s.addNotes('Presenter 1: Greet, introduce the team, read the title. One line: we found the best material for a drone arm using simple strength-of-materials formulas and a ranking method called TOPSIS.');

// 2 Intro with X-frame drawing
s=S('CONTENT','Introduction');T(s,'Why does the drone arm material matter?');
body(s,['The arm holds the motor and carries its thrust to the frame','Heavy arm → shorter flight time (battery limited)','Flexible arm → vibration and poor control','Weak arm → breaks in a hard landing','So we need: light + stiff + strong + affordable'],{x:0.6,y:1.5,w:6.6,h:5.0});
card(s,7.5,1.5,5.2,5.0,'F3EEFB');
const cx=10.1,cy=4.0;
s.addShape(pres.shapes.LINE,{x:8.35,y:2.25,w:3.5,h:3.5,line:{color:'2A0D5C',width:7}});
s.addShape(pres.shapes.LINE,{x:8.35,y:2.25,w:3.5,h:3.5,flipH:true,line:{color:'2A0D5C',width:7}});
[[8.35,2.25],[11.85,2.25],[8.35,5.75],[11.85,5.75]].forEach(([x,y])=>{s.addShape(pres.shapes.OVAL,{x:x-0.42,y:y-0.42,w:0.84,h:0.84,fill:{color:'E2A614'},line:{color:'FFFFFF',width:2}})});
s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:cx-0.55,y:cy-0.4,w:1.1,h:0.8,rectRadius:0.1,fill:{color:'4A1D8C'},line:{color:'FFFFFF',width:2}});
s.addText('Arm',{x:9.75,y:5.0,w:0.8,h:0.4,align:'center',fontSize:15,bold:true,color:'2A0D5C',isTextBox:true,margin:0});
s.addText('Motor',{x:11.5,y:1.5,w:1.1,h:0.35,fontSize:14,bold:true,color:'2A0D5C',isTextBox:true,margin:0});
s.addText('450 mm quadcopter (X-frame)',{x:7.6,y:6.05,w:5.0,h:0.35,fontSize:14,italic:true,color:'4A1D8C',align:'center',isTextBox:true,margin:0});
s.addNotes('Presenter 1: Point to the drawing. Each of the four arms holds a motor. A heavy arm reduces flight time, a bendy arm vibrates, a weak arm breaks. We want the best balance.');

// 3 Objectives
s=S('CONTENT','Introduction');T(s,'Objectives');
['Model the drone arm as a cantilever beam and find its stress and deflection','Compare five materials for mass, deflection, factor of safety and cost','Rank the materials with the TOPSIS method and check the effect of weights'].forEach((t,i)=>{const x=0.6+i*4.15;card(s,x,1.7,3.85,4.3);num(s,i+1,x+0.3,2.0);s.addText(t,{x:x+0.3,y:2.8,w:3.3,h:3.0,fontSize:19,color:'1F1F1F',valign:'top',isTextBox:true,margin:0})});
s.addNotes('Presenter 1: Three steps – calculate, compare, rank.');

// 4 Problem definition – cantilever diagram
s=S('CONTENT','Methodology');T(s,'Arm modelled as a cantilever beam');
s.addShape(pres.shapes.RECTANGLE,{x:0.9,y:2.0,w:0.45,h:2.6,fill:{color:'7F7F7F'},line:{color:'7F7F7F'}});
s.addText('Frame (fixed)',{x:0.4,y:4.7,w:1.6,h:0.4,fontSize:13,color:'444444',align:'center',isTextBox:true,margin:0});
s.addShape(pres.shapes.RECTANGLE,{x:1.35,y:3.05,w:5.4,h:0.5,fill:{color:'4A1D8C'},line:{color:'4A1D8C'}});
s.addShape(pres.shapes.DOWN_ARROW,{x:6.35,y:1.75,w:0.6,h:1.2,fill:{color:'E2A614'},line:{color:'E2A614'}});
s.addText('F = 20 N',{x:7.05,y:1.9,w:1.6,h:0.5,fontSize:18,bold:true,color:'2A0D5C',isTextBox:true,margin:0});
s.addShape(pres.shapes.LINE,{x:1.35,y:4.05,w:5.4,h:0,line:{color:'444444',width:1.25,beginArrowType:'arrow',endArrowType:'arrow'}});
s.addText('L = 200 mm',{x:3.3,y:4.15,w:1.6,h:0.4,fontSize:16,color:'2A0D5C',align:'center',isTextBox:true,margin:0});
s.addShape(pres.shapes.OVAL,{x:3.4,y:5.0,w:1.2,h:1.2,fill:{color:'4A1D8C'},line:{color:'4A1D8C'}});
s.addShape(pres.shapes.OVAL,{x:3.5,y:5.1,w:1.0,h:1.0,fill:{color:'FFFFFF'},line:{color:'FFFFFF'}});
s.addText('Tube cross-section:\nD = 12 mm, d = 10 mm',{x:4.8,y:5.15,w:3.0,h:0.9,fontSize:15,color:'2A0D5C',isTextBox:true,margin:0,valign:'middle'});
card(s,8.9,1.6,3.8,4.7);
s.addText([{text:'Design data',options:{bold:true,breakLine:true,fontSize:20,color:'4A1D8C'}},{text:'Drone: 450 mm, ≈ 1.5 kg',options:{bullet:true,breakLine:true}},{text:'Max motor thrust: 10 N',options:{bullet:true,breakLine:true}},{text:'Safety factor: 2',options:{bullet:true,breakLine:true}},{text:'Design load F = 10 × 2 = 20 N',options:{bullet:true,breakLine:true}},{text:'Load at free end (motor)',options:{bullet:true}}],{x:9.15,y:1.85,w:3.4,h:4.3,fontSize:17,color:'1F1F1F',valign:'top',isTextBox:true,paraSpaceAfter:6});
s.addNotes('Presenter 2: The arm is fixed at the frame and the motor pushes up at the other end – exactly a cantilever from Strength of Materials. The motor gives up to 10 N; we double it for safety, so 20 N.');

// 5 Formulas
s=S('CONTENT','Methodology');T(s,'Calculation using beam theory');
const fm=[['Moment of inertia','I = π(D⁴ − d⁴)/64',R.I.toFixed(1)+' mm⁴'],['Section modulus','Z = I / (D/2)',R.Z.toFixed(1)+' mm³'],['Bending moment','M = F × L = 20 × 200',R.M.toFixed(0)+' N·mm'],['Bending stress','σ = M / Z',R.sigma.toFixed(1)+' MPa'],['Tip deflection','δ = F L³ / (3 E I)','depends on E'],['Mass','m = ρ × A × L','depends on ρ']];
fm.forEach((f,i)=>{const col=i%3,row=Math.floor(i/3);const x=0.6+col*4.15,y=1.55+row*2.6;card(s,x,y,3.85,2.3,i==3?'4A1D8C':'F3EEFB');const dk=i==3;
 s.addText(f[0],{x:x+0.3,y:y+0.2,w:3.3,h:0.45,fontSize:16,bold:true,color:dk?'FFD666':'4A1D8C',isTextBox:true,margin:0});
 s.addText(f[1],{x:x+0.3,y:y+0.7,w:3.3,h:0.6,fontSize:19,color:dk?'FFFFFF':'1F1F1F',isTextBox:true,margin:0,fontFace:'Cambria'});
 s.addText(f[2],{x:x+0.3,y:y+1.4,w:3.3,h:0.6,fontSize:24,bold:true,color:dk?'FFFFFF':'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'})});
s.addNotes('Presenter 2: These are textbook formulas. Same tube shape for all materials, so the stress is the same 45.5 MPa for all. Deflection changes with E (stiffness) and mass changes with density. You can work these on a calculator.');

// 6 Materials table
s=S('CONTENT','Methodology');T(s,'Candidate materials');
const H={bold:true,color:'FFFFFF',fill:{color:'2A0D5C'},align:'center',fontSize:15};
const tr=[[{text:'Material',options:H},{text:'Density (kg/m³)',options:H},{text:'E (GPa)',options:H},{text:'Strength (MPa)',options:H},{text:'Cost (₹/kg, approx.)',options:H}]];
rows.forEach((r,i)=>{const o={fontSize:15,align:'center',fill:{color:i%2?'F3EEFB':'FFFFFF'}};tr.push([{text:r.name,options:Object.assign({},o,{align:'left'})},{text:String(r.rho),options:o},{text:String(r.E),options:o},{text:String(r.Sy),options:o},{text:r.ckg.toLocaleString('en-IN'),options:o}])});
s.addTable(tr,{x:0.6,y:1.55,w:12.1,colW:[3.7,2.1,2.0,2.1,2.2],rowH:0.55,border:{type:'solid',pt:0.75,color:'D0C4EA'},fontFace:'Calibri'});
s.addText('Source: typical handbook values (ASM Handbook, MatWeb). Strength = yield for metals, tensile for composites. Costs are approximate Indian market prices, used only for comparison.',{x:0.6,y:5.3,w:12.1,h:0.8,fontSize:13,italic:true,color:'666666',isTextBox:true,margin:0});
s.addNotes('Presenter 2: Two metals commonly used, one premium metal (titanium) and two composites. Values come from standard handbooks.');

// 7 Results mass & deflection
s=S('CONTENT','Results');T(s,'Results: arm mass and tip deflection');
bar(s,'Arm mass (g)',rows.map(r=>+r.mass.toFixed(1)),0.6,1.4,6.0,4.9,'0.0');
bar(s,'Tip deflection (mm)',rows.map(r=>+r.defl.toFixed(2)),6.7,1.4,6.0,4.9,'0.00');
s.addText('CFRP is lightest (11.1 g, ~80% lighter than steel); steel is stiffest but 5× heavier; GFRP bends the most',{x:0.6,y:6.35,w:12.1,h:0.5,fontSize:15,italic:true,color:'4A1D8C',isTextBox:true,margin:0});
s.addNotes('Presenter 3: Left – weight. Carbon fibre is the lightest. Right – how much the tip bends. Steel bends least but is very heavy. Glass fibre bends 4 mm, which is too flexible.');

// 8 FoS & cost
s=S('CONTENT','Results');T(s,'Results: factor of safety and cost');
bar(s,'Factor of safety',rows.map(r=>+r.fos.toFixed(1)),0.6,1.4,6.0,4.9,'0.0');
bar(s,'Material cost per arm (₹)',rows.map(r=>+r.cost.toFixed(1)),6.7,1.4,6.0,4.9,'0.0');
s.addText('All materials are safe (FoS > 6); titanium is strongest but costliest; aluminium is cheapest',{x:0.6,y:6.35,w:12.1,h:0.5,fontSize:15,italic:true,color:'4A1D8C',isTextBox:true,margin:0});
s.addNotes('Presenter 3: Every material is safe – factor of safety above 6. So the choice depends on weight, stiffness and cost. That is why we need a ranking method.');

// 9 TOPSIS steps
s=S('CONTENT','TOPSIS');T(s,'TOPSIS ranking method in 6 steps');
const st=[['Decision matrix','Materials × criteria table'],['Normalise','Divide by √(sum of squares)'],['Apply weights','Mass 0.35, Deflection 0.25, FoS 0.20, Cost 0.20'],['Ideal best & worst','Best and worst value of each criterion'],['Distances','D+ to best, D− to worst'],['Closeness score','C = D− / (D+ + D−); highest = best']];
st.forEach((q,i)=>{const col=i%3,row=Math.floor(i/3);const x=0.6+col*4.15,y=1.55+row*2.55;card(s,x,y,3.85,2.25);num(s,i+1,x+0.3,y+0.3);
 s.addText(q[0],{x:x+1.05,y:y+0.3,w:2.6,h:0.55,fontSize:19,bold:true,color:'2A0D5C',isTextBox:true,margin:0,valign:'middle',fontFace:'Times New Roman'});
 s.addText(q[1],{x:x+0.3,y:y+1.05,w:3.3,h:1.0,fontSize:16,color:'1F1F1F',isTextBox:true,margin:0,valign:'top'})});
s.addText('TOPSIS = Technique for Order of Preference by Similarity to Ideal Solution',{x:0.6,y:6.5,w:12.1,h:0.4,fontSize:14,italic:true,color:'666666',isTextBox:true,margin:0});
s.addNotes('Presenter 4: TOPSIS picks the option closest to an imaginary perfect material and farthest from the worst one. All steps are simple arithmetic and are shown in our Excel sheet.');

// 10 TOPSIS result
s=S('CONTENT','TOPSIS');T(s,'TOPSIS result: CFRP ranks first');
const ord=[...rows].sort((a,b)=>b.C-a.C);
s.addChart(pres.charts.BAR,[{name:'Closeness score',labels:ord.map(r=>short(r.name)),values:ord.map(r=>+r.C.toFixed(3))}],{x:0.6,y:1.4,w:7.4,h:5.2,barDir:'bar',showTitle:true,title:'Closeness score C (higher = better)',titleFontSize:16,titleColor:'2A0D5C',titleFontFace:'+mj-lt',
 chartColors:['4A1D8C'],showValue:true,dataLabelPosition:'outEnd',dataLabelFormatCode:'0.000',dataLabelFontSize:13,dataLabelFontFace:'+mn-lt',catAxisOrientation:'maxMin',
 catAxisLabelColor:'444444',valAxisLabelColor:'666666',catAxisLabelFontSize:14,valAxisLabelFontFace:'+mn-lt',catAxisLabelFontFace:'+mn-lt',valAxisMinVal:0,valAxisMaxVal:1,valGridLine:{color:'E5E5E5',size:0.75},catGridLine:{style:'none'},showLegend:false,barGapWidthPct:50});
card(s,8.4,1.5,4.3,2.4,'4A1D8C');
s.addText('1st  CFRP',{x:8.7,y:1.7,w:3.8,h:0.7,fontSize:30,bold:true,color:'FFD666',isTextBox:true,margin:0,fontFace:'Times New Roman'});
s.addText('Lightest, stiff and very safe – best overall',{x:8.7,y:2.5,w:3.8,h:1.2,fontSize:17,color:'FFFFFF',isTextBox:true,margin:0,valign:'top'});
card(s,8.4,4.2,4.3,2.4);
s.addText('2nd  Aluminium 6061-T6',{x:8.7,y:4.4,w:3.8,h:0.6,fontSize:22,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
s.addText('Cheapest and easy to machine – best budget choice',{x:8.7,y:5.1,w:3.8,h:1.2,fontSize:17,color:'1F1F1F',isTextBox:true,margin:0,valign:'top'});
s.addNotes('Presenter 4: Carbon fibre scores 0.784 and comes first; aluminium is second with 0.713. Steel is last because it is too heavy.');

// 11 Sensitivity
s=S('CONTENT','TOPSIS');T(s,'Does the result change with weights?');
const sc=[['Base weights','Mass 0.35 · Defl. 0.25 · FoS 0.20 · Cost 0.20','CFRP'],['Equal weights','0.25 each',R.eq[0][0].split(' (')[0]],['Cost-focused','Mass 0.25 · Defl. 0.15 · FoS 0.15 · Cost 0.45',R.cost[0][0].replace(' (glass/epoxy)','')]];
sc.forEach((q,i)=>{const x=0.6+i*4.15;card(s,x,1.6,3.85,3.6,i==2?'4A1D8C':'F3EEFB');const dk=i==2;
 s.addText(q[0],{x:x+0.3,y:1.85,w:3.3,h:0.5,fontSize:20,bold:true,color:dk?'FFD666':'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
 s.addText(q[1],{x:x+0.3,y:2.45,w:3.3,h:1.0,fontSize:15,color:dk?'FFFFFF':'444444',isTextBox:true,margin:0,valign:'top'});
 s.addText([{text:'Rank 1: ',options:{}},{text:q[2],options:{bold:true}}],{x:x+0.3,y:3.9,w:3.3,h:0.9,fontSize:22,color:dk?'FFFFFF':'4A1D8C',isTextBox:true,margin:0,fontFace:'Times New Roman'})});
s.addText('Matches real practice: premium drones use carbon-fibre arms, low-cost drones use aluminium arms',{x:0.6,y:5.6,w:12.1,h:0.6,fontSize:17,italic:true,color:'4A1D8C',isTextBox:true,margin:0});
s.addNotes('Presenter 4: If we care most about performance, carbon fibre wins. If cost is the main concern, aluminium wins. This matches what we see in the market.');

// 12 Conclusion
s=S('CONTENT','Conclusion');T(s,'Conclusion and future work');
card(s,0.6,1.5,5.9,4.9);card(s,6.8,1.5,5.9,4.9);
s.addText('Conclusion',{x:0.9,y:1.7,w:5.3,h:0.6,fontSize:22,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
body(s,['Bending stress in the arm is only 45.5 MPa – all five materials are safe','CFRP is the best overall choice (C = 0.784, 11.1 g arm)','Aluminium 6061-T6 is the best low-cost choice','Simple beam theory + TOPSIS gives a quick, transparent decision'],{x:0.9,y:2.4,w:5.3,h:3.9,fontSize:17});
s.addText('Future work',{x:7.1,y:1.7,w:5.3,h:0.6,fontSize:22,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
body(s,['Verify stress and deflection with FEA (ANSYS)','Include vibration (natural frequency) and impact load','Test 3D-printed and natural-fibre composite arms'],{x:7.1,y:2.4,w:5.3,h:3.9,fontSize:17});
s.addNotes('Presenter 1: Summarise. Next we will check the results with ANSYS and add vibration and crash loads.');

// 13 References
s=S('CONTENT','Conclusion');T(s,'References');
const refs=['R. C. Hibbeler, Mechanics of Materials, 10th ed., Pearson, 2017.','M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., Butterworth-Heinemann, 2017.','C. L. Hwang and K. Yoon, Multiple Attribute Decision Making: Methods and Applications, Springer, 1981.','ASM International, ASM Handbook, Vol. 2: Properties and Selection – Nonferrous Alloys, 1990.','MatWeb Material Property Data, www.matweb.com (accessed October 2026).'];
s.addText(refs.map((t,i)=>({text:t,options:{bullet:{type:'number'},breakLine:i<refs.length-1}})),{x:0.6,y:1.5,w:12.1,h:4.9,fontSize:17,color:'1F1F1F',paraSpaceAfter:12,valign:'top',isTextBox:true});

// 14 Thank you
s=S('TITLE_DARK','Conclusion');
s.addImage({path:'logo.png',x:5.92,y:1.2,w:1.5,h:1.5});
s.addText('Thank you',{x:0.6,y:3.0,w:12.1,h:1.2,fontSize:54,bold:true,color:'FFFFFF',align:'center',fontFace:'Times New Roman',isTextBox:true,margin:0});
s.addText('Questions?',{x:0.6,y:4.2,w:12.1,h:0.6,fontSize:24,italic:true,color:'FFD666',align:'center',isTextBox:true,margin:0});
s.addText('Department of Mechanical Engineering, St. Joseph’s College of Engineering and Technology, Thanjavur',{x:0.6,y:6.3,w:12.1,h:0.4,fontSize:14,color:'D9CCF2',align:'center',isTextBox:true,margin:0});
(async()=>{await pres.writeFile({fileName:'ICAAN2026_PPT_DroneArm.pptx'});await applyTheme('ICAAN2026_PPT_DroneArm.pptx',THEME);console.log('done')})();
