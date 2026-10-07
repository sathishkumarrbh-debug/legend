const pptxgen=require('pptxgenjs');const {applyTheme}=require('/root/.claude/skills/synced/45b7e87e-ac83-452a-89b7-74bd0de926e7_3d9968d9-88c4-400f-b210-6b62be8e5894/pptx/scripts/apply_theme.js');
const R=require('./results.json');
const THEME={name:'SJCET Purple Gold',headFontFace:'Times New Roman',bodyFontFace:'Calibri',
 colors:{dk1:'1F1F1F',lt1:'FFFFFF',dk2:'2A0D5C',lt2:'F3EEFB',accent1:'4A1D8C',accent2:'E2A614',accent3:'7B4FD0',accent4:'B9B9B9',accent5:'2A0D5C',accent6:'FFD666',hlink:'4A1D8C',folHlink:'7B4FD0'}};
const pres=new pptxgen();pres.layout='LAYOUT_WIDE';pres.theme={headFontFace:THEME.headFontFace,bodyFontFace:THEME.bodyFontFace};
pres.title='ML Surrogate Model for NACA Airfoils';pres.author='Department of Mechanical Engineering, SJCET';
const C=pres.SchemeColor;
const FOOT='ICAAN–2026  |  St. Joseph’s College of Engineering and Technology, Thanjavur';
pres.defineSlideMaster({title:'TITLE_DARK',background:{color:'2A0D5C'},objects:[],
 slideNumber:null});
pres.defineSlideMaster({title:'CONTENT',background:{color:'FFFFFF'},margin:[0.5,0.6,0.6,0.6],
 objects:[{text:{text:FOOT,options:{x:0.6,y:7.0,w:9,h:0.3,fontSize:10,color:'8A8A8A',fontFace:'Calibri'}}},
  {placeholder:{options:{name:'title',type:'title',x:0.6,y:0.35,w:12.1,h:0.9,fontSize:34,bold:true,color:C.text2,fontFace:'Times New Roman',valign:'middle',margin:0},text:''}}],
 slideNumber:{x:12.2,y:7.0,w:0.6,h:0.3,fontSize:10,color:'8A8A8A',align:'right'}});
pres.defineSlideMaster({title:'SECTION_GOLD',background:{color:'4A1D8C'},objects:[],slideNumber:{x:12.2,y:7.0,w:0.6,h:0.3,fontSize:10,color:'D9CCF2',align:'right'}});
let sec='';function S(m,s){if(s!==sec){pres.addSection({title:s});sec=s}return pres.addSlide({masterName:m,sectionTitle:s})}
const T=(sl,t)=>sl.addText(t,{placeholder:'title'});
function num(sl,n,x,y,d=0.55){sl.addShape(pres.shapes.OVAL,{x,y,w:d,h:d,fill:{color:C.accent2},line:{color:C.accent2},objectName:'num'+n});
 sl.addText(String(n),{x,y,w:d,h:d,align:'center',valign:'middle',fontSize:18,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'})}
function card(sl,x,y,w,h,fill){sl.addShape(pres.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:0.12,fill:{color:fill||'F3EEFB'},line:{color:fill||'F3EEFB'},shadow:{type:'outer',color:'000000',opacity:0.12,blur:6,offset:2,angle:90}})}
const body=(sl,arr,o)=>sl.addText(arr.map((t,i)=>({text:t,options:{bullet:true,breakLine:i<arr.length-1}})),Object.assign({fontSize:18,color:'1F1F1F',paraSpaceAfter:10,valign:'top',isTextBox:true},o));

// 1 Title
let s=S('TITLE_DARK','Introduction');
s.addImage({path:'logo.png',x:0.6,y:0.45,w:1.15,h:1.15});
s.addText([{text:'St. Joseph’s College of Engineering and Technology, Thanjavur',options:{breakLine:true,bold:true}},{text:'Department of Mechanical Engineering',options:{}}],{x:1.95,y:0.55,w:10,h:0.95,fontSize:16,color:'FFFFFF',isTextBox:true,margin:0,fontFace:'Calibri'});
s.addText('Machine Learning Surrogate Model for Rapid Prediction of Lift and Suction Peak of NACA 4-Digit Airfoils',{x:0.6,y:2.0,w:12.1,h:1.9,fontSize:38,bold:true,color:'FFFFFF',fontFace:'Times New Roman',isTextBox:true,margin:0,valign:'middle'});
s.addText('Track: Artificial Intelligence in Aerospace',{x:0.6,y:3.95,w:12,h:0.45,fontSize:18,italic:true,color:'FFD666',isTextBox:true,margin:0});
s.addText([{text:'Dr. S. R. Sathishkumar, [Staff Name]',options:{breakLine:true,bold:true}},{text:'[Student 1], [Student 2], [Student 3], [Student 4]'}],{x:0.6,y:4.8,w:12,h:0.95,fontSize:18,color:'FFFFFF',isTextBox:true,margin:0});
s.addText('ICAAN–2026  ·  Saranathan College of Engineering, Tiruchirappalli  ·  15–16 October 2026',{x:0.6,y:6.55,w:12,h:0.4,fontSize:13,color:'D9CCF2',isTextBox:true,margin:0});
s.addNotes('Presenter 1: Greet the audience, introduce the team and say the title. One line: we built a computer model that predicts how much lift an aircraft wing section produces, in a fraction of a millisecond.');

// 2 Problem
s=S('CONTENT','Introduction');T(s,'Why do we need fast airfoil prediction?');
body(s,['An airfoil is the cross-section of a wing; its shape decides the lift','Designing a UAV wing means testing hundreds of shapes and angles','Each test needs a flow calculation (CFD or panel method) – slow when repeated','Idea: train a machine learning model once, then predict instantly'],{x:0.6,y:1.5,w:6.6,h:4.8});
card(s,7.6,1.55,5.1,4.9,'F3EEFB');
s.addImage({path:'fig_airfoils.png',x:7.75,y:2.6,w:4.8,h:1.17});
s.addText('Same thickness (12%), different camber → different lift',{x:7.8,y:4.75,w:4.7,h:0.9,fontSize:15,italic:true,color:'4A1D8C',isTextBox:true,align:'center'});
s.addNotes('Explain with a hand gesture: the curved (cambered) shape gives more lift than the symmetric one at the same angle. Engineers must check many such shapes, which takes time. Our idea is to replace the slow calculation with a trained ML model.');

// 3 Objectives
s=S('CONTENT','Introduction');T(s,'Objectives');
const objs=['Build and validate a panel-method solver for NACA 4-digit airfoils in Python','Generate a dataset of 3,000 airfoil cases (shape + angle of attack)','Train and compare Linear Regression, Random Forest and ANN models to predict CL and Cp,min'];
objs.forEach((t,i)=>{const x=0.6+i*4.15;card(s,x,1.7,3.85,4.3,'F3EEFB');num(s,i+1,x+0.3,2.0);s.addText(t,{x:x+0.3,y:2.8,w:3.3,h:3.0,fontSize:18,color:'1F1F1F',valign:'top',isTextBox:true,margin:0})});
s.addNotes('Presenter 1: Read the three objectives. Build a solver, make data with it, and teach ML models from the data.');

// 4 NACA basics
s=S('CONTENT','Methodology');T(s,'Understanding NACA 4-digit airfoils');
s.addText('NACA 2412',{x:0.6,y:1.6,w:6,h:1.0,fontSize:54,bold:true,color:C.accent1,fontFace:'Times New Roman',isTextBox:true,margin:0});
const dig=[['2','Maximum camber = 2% of chord'],['4','Position of max camber = 40% of chord'],['12','Maximum thickness = 12% of chord']];
dig.forEach((d,i)=>{const y=2.95+i*1.1;s.addShape(pres.shapes.ROUNDED_RECTANGLE,{x:0.6,y,w:1.1,h:0.8,rectRadius:0.1,fill:{color:C.accent1},line:{color:C.accent1}});
 s.addText(d[0],{x:0.6,y,w:1.1,h:0.8,align:'center',valign:'middle',fontSize:26,bold:true,color:'FFFFFF',isTextBox:true,margin:0,fontFace:'Times New Roman'});
 s.addText(d[1],{x:1.95,y,w:4.8,h:0.8,valign:'middle',fontSize:19,color:'1F1F1F',isTextBox:true,margin:0})});
card(s,7.3,1.6,5.4,4.9,'F3EEFB');
s.addText([{text:'Inputs to our model',options:{bold:true,breakLine:true,fontSize:20,color:'4A1D8C'}},{text:'Camber m: 0 – 6%',options:{bullet:true,breakLine:true}},{text:'Camber position p: 20 – 60%',options:{bullet:true,breakLine:true}},{text:'Thickness t: 8 – 18%',options:{bullet:true,breakLine:true}},{text:'Angle of attack α: −4° to 12°',options:{bullet:true,breakLine:true}},{text:' ',options:{breakLine:true}},{text:'Outputs',options:{bold:true,breakLine:true,fontSize:20,color:'4A1D8C'}},{text:'Lift coefficient CL',options:{bullet:true,breakLine:true}},{text:'Suction peak Cp,min',options:{bullet:true}}],{x:7.6,y:1.85,w:4.9,h:4.5,fontSize:18,color:'1F1F1F',valign:'top',isTextBox:true,paraSpaceAfter:4});
s.addNotes('Presenter 2: The four digits describe the shape. 2412 means 2% camber at 40% chord and 12% thickness. These shape numbers plus the angle of attack are the four inputs; lift coefficient and suction peak are the two outputs.');

// 5 Workflow
s=S('CONTENT','Methodology');T(s,'Methodology');
const steps=[['Airfoil geometry','NACA 4-digit equations, 160 panels'],['Panel method','Hess–Smith source–vortex solver'],['Dataset','3,000 random cases'],['ML training','80% train, 20% test'],['Prediction','CL and Cp,min in < 0.01 ms']];
steps.forEach((st,i)=>{const x=0.6+i*2.5;card(s,x,2.0,2.2,3.2,i==4?'4A1D8C':'F3EEFB');num(s,i+1,x+0.82,2.25);
 s.addText(st[0],{x:x+0.1,y:3.0,w:2.0,h:0.8,align:'center',valign:'middle',fontSize:18,bold:true,color:i==4?'FFFFFF':'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
 s.addText(st[1],{x:x+0.15,y:3.85,w:1.9,h:1.1,align:'center',valign:'top',fontSize:14,color:i==4?'FFFFFF':'333333',isTextBox:true,margin:0});
 if(i<4)s.addShape(pres.shapes.RIGHT_TRIANGLE?pres.shapes.RIGHT_ARROW:pres.shapes.RIGHT_ARROW,{x:x+2.22,y:3.4,w:0.26,h:0.4,fill:{color:C.accent2},line:{color:C.accent2}})});
s.addText('Tools: Python, NumPy, scikit-learn, Matplotlib',{x:0.6,y:5.7,w:12,h:0.5,fontSize:16,italic:true,color:'4A1D8C',isTextBox:true,margin:0});
s.addNotes('Presenter 2: Walk left to right. We draw the airfoil with equations, split its surface into 160 small panels, solve the flow, repeat for 3,000 random shapes and angles, then teach the ML model with this data.');

// 6 Validation
s=S('CONTENT','Methodology');T(s,'Panel method validation');
s.addImage({path:'fig_validation.png',x:0.6,y:1.4,w:6.9,h:4.83});
const v=R.val;const vs=[[v.slope_0012_perdeg.toFixed(3)+' /°','Lift-curve slope, NACA 0012','Theory: 0.110 /° (thin plate); thickness adds ≈ 9%'],[v.aL0_2412.toFixed(2)+'°','Zero-lift angle, NACA 2412','Thin airfoil theory: −2.08°']];
vs.forEach((q,i)=>{const y=1.6+i*2.35;card(s,7.9,y,4.8,2.05,'F3EEFB');s.addText(q[0],{x:8.15,y:y+0.15,w:4.4,h:0.85,fontSize:40,bold:true,color:C.accent1,fontFace:'Times New Roman',isTextBox:true,margin:0});
 s.addText([{text:q[1],options:{bold:true,breakLine:true}},{text:q[2]}],{x:8.15,y:y+1.0,w:4.4,h:0.95,fontSize:15,color:'333333',isTextBox:true,margin:0,valign:'top'})});
s.addNotes('Presenter 3: Before trusting the data we checked the solver. The straight lines match theory: the symmetric airfoil gives zero lift at zero angle, and the cambered 2412 gives zero lift at about minus 2 degrees, exactly as theory predicts.');

// 7 Cp
s=S('CONTENT','Methodology');T(s,'Pressure distribution and suction peak');
s.addImage({path:'fig_cp.png',x:0.6,y:1.4,w:6.9,h:4.83});
body(s,['Lower pressure on the upper surface lifts the wing','Cp,min is the strongest suction, near the leading edge','A sharp suction peak warns of flow separation and stall','Cp,min changes strongly (nonlinearly) with angle and thickness – a harder target for ML'],{x:7.9,y:1.6,w:4.8,h:4.7,fontSize:17});
s.addNotes('Presenter 3: The purple curve is the top surface, gold is the bottom. The gap between them is the lift. The tall spike near the front is the suction peak; designers watch it because a very sharp peak leads to stall.');

// 8 ML models
s=S('CONTENT','Machine learning');T(s,'Machine learning models compared');
const mods=[['Linear Regression','Fits a straight-line relation between inputs and output. Fast and simple.'],['Random Forest','Averages 300 decision trees. Handles nonlinear data.'],['Artificial Neural Network','2 hidden layers × 64 neurons. Learns complex nonlinear patterns.']];
mods.forEach((m,i)=>{const x=0.6+i*4.15;card(s,x,1.7,3.85,3.2,i==2?'4A1D8C':'F3EEFB');
 s.addText(m[0],{x:x+0.3,y:1.95,w:3.3,h:0.8,fontSize:21,bold:true,color:i==2?'FFD666':'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
 s.addText(m[1],{x:x+0.3,y:2.85,w:3.3,h:1.9,fontSize:17,color:i==2?'FFFFFF':'1F1F1F',isTextBox:true,margin:0,valign:'top'})});
s.addText('Dataset: 3,000 cases  ·  Training: 2,400  ·  Testing: 600  ·  Metrics: R² and mean absolute error (MAE)',{x:0.6,y:5.35,w:12.1,h:0.5,fontSize:16,italic:true,color:'4A1D8C',isTextBox:true,margin:0});
s.addNotes('Presenter 4: We tried three models from simple to advanced. R squared close to 1 means the prediction matches the solver almost perfectly; MAE is the average error.');

// 9 Results table + parity
s=S('CONTENT','Results');T(s,'Results: prediction accuracy on test data');
const H={bold:true,color:'FFFFFF',fill:{color:'2A0D5C'},align:'center',fontSize:15};
const rows=[[{text:'Model',options:H},{text:'R² (CL)',options:H},{text:'MAE (CL)',options:H},{text:'R² (Cp,min)',options:H},{text:'MAE (Cp,min)',options:H}]];
['Linear Regression','Random Forest','ANN (MLP)'].forEach(m=>{const a=R.res.CL[m],b=R.res.CPmin[m];const best=m=='ANN (MLP)';const o={fontSize:15,align:'center',bold:best,color:best?'4A1D8C':'1F1F1F',fill:{color:best?'F3EEFB':'FFFFFF'}};
 rows.push([{text:m,options:Object.assign({},o,{align:'left'})},{text:a.R2.toFixed(3),options:o},{text:a.MAE.toFixed(3),options:o},{text:b.R2.toFixed(3),options:Object.assign({},o,m=='Linear Regression'?{color:'B3261E',bold:true}:{})},{text:b.MAE.toFixed(3),options:o}])});
s.addTable(rows,{x:0.6,y:1.45,w:12.1,colW:[3.3,2.2,2.2,2.2,2.2],rowH:0.42,border:{type:'solid',pt:0.75,color:'D0C4EA'},fontFace:'Calibri'});
s.addImage({path:'fig_parity.png',x:1.9,y:3.4,w:7.6,h:3.5});
s.addText('Linear regression fails on the nonlinear suction peak; the ANN is accurate for both outputs',{x:9.7,y:3.8,w:3.0,h:2.6,fontSize:16,italic:true,color:'4A1D8C',isTextBox:true,margin:0,valign:'middle'});
s.addNotes('Presenter 4: All models predict lift well because lift is almost a straight line with angle. But for the suction peak, linear regression scores only 0.66 while the ANN scores 0.999. In the plots, points on the dashed line are perfect predictions.');

// 10 Key findings
s=S('SECTION_GOLD','Results');
s.addText('Key findings',{x:0.6,y:0.45,w:12,h:0.9,fontSize:34,bold:true,color:'FFFFFF',fontFace:'Times New Roman',isTextBox:true,margin:0});
const sp=Math.round(R.res.CL['ANN (MLP)'].speedup/100)*100;
const kf=[['0.999','R² of ANN for both CL and Cp,min'],['~'+sp.toLocaleString('en-IN')+'×','faster than the panel method per prediction'],[Math.round(R.rf_importance_CL.alpha*100)+'%','of lift variation explained by angle of attack (camber: '+Math.round(R.rf_importance_CL.camber*100)+'%)']];
kf.forEach((k,i)=>{const x=0.6+i*4.15;s.addText(k[0],{x,y:2.0,w:3.85,h:1.4,fontSize:60,bold:true,color:'FFD666',fontFace:'Times New Roman',isTextBox:true,margin:0});
 s.addText(k[1],{x,y:3.5,w:3.6,h:1.4,fontSize:19,color:'FFFFFF',isTextBox:true,margin:0,valign:'top'})});
s.addNotes('Presenter 4: Three numbers to remember: 0.999 accuracy, about 1,500 times faster, and angle of attack is the biggest factor for lift, followed by camber.');

// 11 Conclusion
s=S('CONTENT','Conclusion');T(s,'Conclusion and future work');
card(s,0.6,1.5,5.9,4.9,'F3EEFB');card(s,6.8,1.5,5.9,4.9,'F3EEFB');
s.addText('Conclusion',{x:0.9,y:1.7,w:5.3,h:0.6,fontSize:22,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
body(s,['Validated panel solver matches thin airfoil theory','ANN surrogate predicts CL and Cp,min with R² = 0.999','Predictions are about 1,500× faster – useful for quick UAV wing-section design'],{x:0.9,y:2.4,w:5.3,h:3.8,fontSize:17});
s.addText('Future work',{x:7.1,y:1.7,w:5.3,h:0.6,fontSize:22,bold:true,color:'2A0D5C',isTextBox:true,margin:0,fontFace:'Times New Roman'});
body(s,['Add viscous effects (XFOIL / CFD) to capture drag and stall','Extend to NACA 5-digit and custom airfoil shapes','Use the surrogate for automatic airfoil optimisation'],{x:7.1,y:2.4,w:5.3,h:3.8,fontSize:17});
s.addText('Limitation: inviscid, incompressible flow – drag and stall are not modelled',{x:0.6,y:6.5,w:12.1,h:0.4,fontSize:14,italic:true,color:'8A8A8A',isTextBox:true,margin:0});
s.addNotes('Presenter 1: Summarise and be honest about the limitation: our flow model has no viscosity, so it cannot predict drag or stall. That is our next step.');

// 12 References
s=S('CONTENT','Conclusion');T(s,'References');
const refs=['I. H. Abbott and A. E. von Doenhoff, Theory of Wing Sections, Dover Publications, 1959.','J. L. Hess and A. M. O. Smith, “Calculation of potential flow about arbitrary bodies,” Progress in Aerospace Sciences, vol. 8, pp. 1–138, 1967.','J. Katz and A. Plotkin, Low-Speed Aerodynamics, 2nd ed., Cambridge University Press, 2001.','J. D. Anderson, Fundamentals of Aerodynamics, 6th ed., McGraw-Hill, 2017.','F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.'];
s.addText(refs.map((t,i)=>({text:t,options:{bullet:{type:'number'},breakLine:i<refs.length-1}})),{x:0.6,y:1.5,w:12.1,h:4.9,fontSize:16,color:'1F1F1F',paraSpaceAfter:12,valign:'top',isTextBox:true});

// 13 Thank you
s=S('TITLE_DARK','Conclusion');
s.addImage({path:'logo.png',x:5.92,y:1.2,w:1.5,h:1.5});
s.addText('Thank you',{x:0.6,y:3.0,w:12.1,h:1.2,fontSize:54,bold:true,color:'FFFFFF',align:'center',fontFace:'Times New Roman',isTextBox:true,margin:0});
s.addText('Questions?',{x:0.6,y:4.2,w:12.1,h:0.6,fontSize:24,italic:true,color:'FFD666',align:'center',isTextBox:true,margin:0});
s.addText('Department of Mechanical Engineering, St. Joseph’s College of Engineering and Technology, Thanjavur',{x:0.6,y:6.3,w:12.1,h:0.4,fontSize:14,color:'D9CCF2',align:'center',isTextBox:true,margin:0});
(async()=>{await pres.writeFile({fileName:'ICAAN2026_PPT_SJCET.pptx'});await applyTheme('ICAAN2026_PPT_SJCET.pptx',THEME);console.log('done')})();
