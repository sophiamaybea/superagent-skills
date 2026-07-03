// carousel skill — render Instagram PNGs (1080x1350 @2x) from a JSON content file.
// Usage: node run.mjs <content.json> [output-dir]
import { chromium } from 'playwright-core';
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SKILL_DIR = path.resolve(__dirname, '..');
const CSS_PATH = path.join(SKILL_DIR, 'base.css');
const FONT_PATH = path.join(SKILL_DIR, 'fonts', 'RedStrokes.ttf');
const CHERUB_PATH = path.join(SKILL_DIR, 'assets', 'cherub.png');

const contentPath = process.argv[2] || 'deck.json';
const outDir = process.argv[3] || 'carousel-out';

if (!fs.existsSync(contentPath)) {
  console.error(`✖ content file not found: ${contentPath}`);
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

const deck = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const brand = (deck.brand || 'STUDIO BEA SOPHIA').trim();
let slides = deck.slides || [];
const photocopy = deck.photocopy === true;
if (!slides.length) { console.error('✖ no slides in deck'); process.exit(1); }

// Auto-append the cherub signature end-card unless the deck opts out (signature:false)
// or already ends with a signature slide.
const hasSig = slides.some(s => s.layout === 'signature');
if (deck.signature !== false && !hasSig) {
  slides = [...slides, { layout: 'signature', pageno: false }];
}

const css = fs.readFileSync(CSS_PATH, 'utf8');

// Embed Red Strokes as base64 @font-face so headless chromium always has it
let fontFace = '';
if (fs.existsSync(FONT_PATH)) {
  const b64 = fs.readFileSync(FONT_PATH).toString('base64');
  fontFace = `@font-face{font-family:'RedStrokes';src:url(data:font/ttf;base64,${b64}) format('truetype');font-display:block}`;
}

// Embed cherub as base64 data URI so the signature slide always has it
let cherubData = '';
if (fs.existsSync(CHERUB_PATH)) {
  cherubData = `data:image/png;base64,${fs.readFileSync(CHERUB_PATH).toString('base64')}`;
}

const esc = (s = '') => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const nl = (s = '') => esc(s).replace(/\n/g, '<br>');
const brandMark = brand.split(/\s+/).join('<br>');

function slideHTML(s, i) {
  const showNo = s.pageno !== false;
  const pageno = showNo ? `<div class="pageno">${i + 1}</div>` : '';
  const rule = `<div class="rule"></div>`;
  const scriptCls = s.script ? ' script' : '';
  let inner = '';

  if (s.layout === 'hero') {
    // big handwritten opener — e.g. "hello" / "hi, I'm Bea"
    inner = `
      <div class="center" style="width:960px">
        ${s.hi ? `<div class="hi">${nl(s.hi)}</div>` : ''}
        ${s.title ? `<h1 class="mid" style="text-align:center;margin-top:24px">${nl(s.title)}</h1>` : ''}
        ${s.sub ? `<div class="sub" style="margin-top:36px">${nl(s.sub)}</div>` : ''}
      </div>`;
  } else if (s.layout === 'signature') {
    // cherub signature end-card — stays clean/red (photocopy-exempt by default)
    const handle = s.handle || '@studiobeasophia';
    inner = `
      <div class="center" style="width:100%">
        ${cherubData ? `<img src="${cherubData}" style="width:62%;max-width:660px;height:auto;display:block;margin:0 auto"/>` : ''}
        <div class="sig-handle">${esc(handle.toUpperCase())}</div>
        <div class="sig-rule"></div>
      </div>`;
  } else if (s.layout === 'cover') {
    inner = `
      <div class="center">
        ${s.eyebrow ? `<div class="eyebrow" style="text-align:center">${nl(s.eyebrow)}</div>` : ''}
        <h1 class="big${scriptCls}" style="margin-top:${s.eyebrow ? '32px' : '0'}">${nl(s.title)}</h1>
        ${s.sub ? `<div class="sub">${nl(s.sub)}</div>` : ''}
      </div>`;
  } else if (s.layout === 'statement') {
    inner = `
      <div style="margin-top:150px">
        ${s.eyebrow ? `<div class="eyebrow">${nl(s.eyebrow)}</div>` : ''}
        <h1 class="mid${scriptCls}" style="font-size:96px">${nl(s.title)}</h1>
        ${s.sub ? `<div class="row" style="color:var(--mut)">${nl(s.sub)}</div>` : ''}
      </div>`;
  } else if (s.layout === 'quote') {
    inner = `
      <div class="center">
        <h1 class="mid${scriptCls}" style="text-align:center;font-size:70px">&ldquo;${nl(s.quote)}&rdquo;</h1>
        ${s.attribution ? `<div class="sub">${nl(s.attribution)}</div>` : ''}
      </div>`;
  } else { // list (default)
    const items = (s.items || []).map(it =>
      `<div class="row"><span class="arw">&rarr;</span><span>${nl(it)}</span></div>`).join('');
    const kicker = s.kicker
      ? `<div class="row" style="margin-top:56px"><span class="arw kicker">&rarr;</span><span class="kicker">${nl(s.kicker)}</span></div>`
      : '';
    inner = `
      <div style="margin-top:150px">
        ${s.eyebrow ? `<div class="eyebrow">${nl(s.eyebrow)}</div>` : ''}
        ${s.title ? `<h1 class="mid${scriptCls}">${nl(s.title)}</h1>` : ''}
        ${items}${kicker}
      </div>`;
  }

  // Signature slide is photocopy-exempt by default so the cherub stays red.
  const isSig = s.layout === 'signature';
  const wantPhoto = (photocopy || s.photocopy === true) && s.photocopy !== false && !(isSig && s.photocopy !== true);
  const bodyCls = wantPhoto ? ' class="photocopy"' : '';
  return `<!doctype html><html><head><meta charset="utf-8">
<style>${fontFace}${css}
.sig-handle{font-family:'IBM Plex Mono',monospace;font-size:38px;letter-spacing:2px;color:var(--ink,#111);text-align:center;margin-top:64px}
.sig-rule{width:90px;height:6px;background:var(--org,#f07d1a);margin:36px auto 0}
</style></head>
<body${bodyCls}><div class="pad">
<div class="brand">${brandMark}</div>
${inner}
${rule}${pageno}
</div></body></html>`;
}

// locate headless chromium shell
const cacheBase = '/root/.cache/ms-playwright';
const shellDir = fs.readdirSync(cacheBase).find(d => d.startsWith('chromium_headless_shell'));
const exe = execSync(`find ${cacheBase}/${shellDir} -name 'chrome-headless-shell' -type f | head -1`).toString().trim();

const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });

const written = [];
for (let i = 0; i < slides.length; i++) {
  await page.setContent(slideHTML(slides[i], i), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const name = `slide-${String(i + 1).padStart(2, '0')}.png`;
  await page.screenshot({ path: path.join(outDir, name) });
  written.push(name);
  console.log('✓ rendered', name);
}
await browser.close();
fs.copyFileSync(contentPath, path.join(outDir, 'deck.used.json'));
console.log(`\nDone — ${written.length} slides in ${outDir}/`);
