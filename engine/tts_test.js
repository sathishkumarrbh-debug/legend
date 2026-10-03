const m=require('mespeak');const fs=require('fs');
m.loadConfig(require('mespeak/src/mespeak_config.json'));m.loadVoice(require('mespeak/voices/en/en-us.json'));
const dir=process.argv[3]||'_tts';
const lines=fs.readFileSync(process.argv[2],'utf8').trim().split('\n');
lines.forEach((l,i)=>{const b=m.speak(l,{rawdata:'buffer',speed:185,pitch:40});fs.writeFileSync(dir+'/l'+String(i).padStart(2,'0')+'.wav',Buffer.from(b));});
