window.__RES = null;
(async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const v = document.querySelector('video');
  v.muted = true; v.pause();
  const pr = window.ytInitialPlayerResponse || {};
  const vd = pr.videoDetails || {};
  const out = { id: vd.videoId, title: vd.title, ch: vd.author, len: +vd.lengthSeconds, views: vd.viewCount,
    date: pr.microformat?.playerMicroformatRenderer?.publishDate?.slice(0, 10),
    subs: (document.querySelector('#owner-sub-count')?.innerText || '').trim() };
  const grab = () => [...document.querySelectorAll('ytd-transcript-segment-renderer, transcript-segment-view-model')].map(s => s.innerText.replace(/\s+/g, ' ').trim()).join(' | ');
  document.querySelector('ytd-text-inline-expander #expand')?.click(); await sleep(800);
  [...document.querySelectorAll('button')].find(b => /^show transcript$/i.test((b.innerText || '').trim()))?.click();
  await sleep(3500); out.transcript = grab();
  const W = 36, H = 64, c = document.createElement('canvas'); c.width = W; c.height = H;
  const g = c.getContext('2d', { willReadFrequently: true });
  const dur = v.duration || out.len;
  const sheetTimes = [0.2, 1.5, 3, 5, dur * 0.35, dur * 0.55, dur * 0.75, dur - 1];
  const tw = 180, th = 320, sheet = document.createElement('canvas'); sheet.width = tw * 4; sheet.height = th * 2;
  const sg = sheet.getContext('2d'); sg.fillStyle = '#000'; sg.fillRect(0, 0, sheet.width, sheet.height);
  let prev = null, si = 0; const cuts = [];
  v.currentTime = 0; v.playbackRate = 2; v.loop = false; await v.play();
  await new Promise(done => {
    const iv = setInterval(() => {
      const t = v.currentTime;
      g.drawImage(v, 0, 0, W, H);
      const d = g.getImageData(0, 0, W, H).data;
      if (prev) { let s = 0; for (let i = 0; i < d.length; i += 4) s += Math.abs(d[i] - prev[i]) + Math.abs(d[i + 1] - prev[i + 1]) + Math.abs(d[i + 2] - prev[i + 2]); if (s / (W * H * 3) > 35 && (!cuts.length || t - cuts[cuts.length - 1] > 0.4)) cuts.push(+t.toFixed(1)); }
      prev = d;
      while (si < sheetTimes.length && t >= sheetTimes[si]) {
        const vw = v.videoWidth, vh = v.videoHeight, s = Math.min(tw / vw, th / vh);
        sg.drawImage(v, (si % 4) * tw + (tw - vw * s) / 2, Math.floor(si / 4) * th + (th - vh * s) / 2, vw * s, vh * s);
        sg.fillStyle = '#ff0'; sg.font = 'bold 16px sans-serif'; sg.fillText(t.toFixed(1) + 's', (si % 4) * tw + 4, Math.floor(si / 4) * th + 18);
        si++;
      }
      if (v.ended || t >= dur - 0.3 || t < (window.__lastT || 0) - 1) { clearInterval(iv); v.pause(); done(); }
      window.__lastT = t;
    }, 100);
  });
  out.cuts = cuts; out.shots_per_10s = +(cuts.length / dur * 10).toFixed(1);
  document.getElementById('__sheet')?.remove();
  sheet.id = '__sheet'; Object.assign(sheet.style, { position: 'fixed', left: '0', top: '0', zIndex: 99999, width: tw * 4 + 'px', height: th * 2 + 'px' });
  document.body.appendChild(sheet);
  window.__RES = out;
})(); 'started';
