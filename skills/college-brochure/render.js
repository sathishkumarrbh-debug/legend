// Usage: node render.js <file.html> [outName]   -> outName.pdf (print) + outName.png (WhatsApp)
// Run with NODE_PATH=$(npm root -g). Uses the preinstalled Playwright Chromium.
const {chromium}=require('playwright');const path=require('path');
(async()=>{const f=path.resolve(process.argv[2]||'template.html');const out=process.argv[3]||path.basename(f,'.html');
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1123,height:794},deviceScaleFactor:2});
await p.goto('file://'+f);await p.waitForTimeout(800);
const over=await p.evaluate(()=>[...document.querySelectorAll('.pan')].map((x,i)=>{const r=x.getBoundingClientRect();let m=0;
 x.querySelectorAll(':scope > :not(.shard):not(.deco):not(svg)').forEach(e=>m=Math.max(m,e.getBoundingClientRect().bottom));return m>r.bottom-2?'panel '+(i+1)+' overflows by '+Math.round(m-r.bottom+2)+'px':null}).filter(Boolean));
if(over.length)console.log('WARNING:',over.join('; '));
await p.screenshot({path:out+'.png'});await p.pdf({path:out+'.pdf',width:'297mm',height:'210mm',printBackground:true});await b.close();console.log('wrote',out+'.pdf',out+'.png')})();
