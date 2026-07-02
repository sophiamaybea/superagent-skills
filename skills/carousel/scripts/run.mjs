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

const contentPath = process.argv[2] || 'deck.json';
const outDir = process.argv[3] || 'carousel-out';

if (!fs.existsSync(contentPath)) {
  console.error(`✖ content file not found: ${contentPath}`);
  process.exit(1);
}
fs.mkdirSync(outDir, { recursive: true });

const deck = JSON.parse(fs.readFileSync(contentPath, 'utf8'));
const brand = (deck.brand || 'STUDIO BEA SOPHIA').trim();
const slides = deck.slides || [];
if (!slides.length) { console.error('✖ no slides in deck'); process.exit(1); }

const css = fs.readFileSync(CSS_PATH, 'utf8');
const esc = (s = '') => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const nl = (s = '') => esc(s).replace(/\n/g, '<br>');
const brandMark = brand.split(/\s+/).join('<br>');

function slideHTML(s, i, total) {
  const showNo = s.pageno !== false;
  const pageno = showNo ? `<div class="pageno">${i + 1}</div>` : '';
  const rule = `<div class="rule"></div>`;
  let inner = '';

  if (s.layout === 'cover') {
    inner = `
      <div class="center">
        ${s.eyebrow ? `<div class="eyebrow" style="text-align:center">${nl(s.eyebrow)}</div>` : ''}
        <h1 class="big" style="margin-top:${s.eyebrow ? '32px' : '0'}">${nl(s.title)}</h1>
        ${s.sub ? `<div class="sub">${nl(s.sub)}</div>` : ''}
      </div>`;
  } else if (s.layout === 'statement') {
    inner = `
      <div style="margin-top:150px">
        ${s.eyebrow ? `<div class="eyebrow">${nl(s.eyebrow)}</div>` : ''}
        <h1 class="mid" style="font-size:96px">${nl(s.title)}</h1>
        ${s.sub ? `<div class="row" style="color:var(--mut)">${nl(s.sub)}</div>` : ''}
      </div>`;
  } else if (s.layout === 'quote') {
    inner = `
      <div class="center">
        <h1 class="mid" style="text-align:center;font-size:70px">&ldquo;${nl(s.quote)}&rdquo;</h1>
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
        ${s.title ? `<h1 class="mid">${nl(s.title)}</h1>` : ''}
        ${items}${kicker}
      </div>`;
  }

  return `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head>
<body><div class="pad">
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
  await page.setContent(slideHTML(slides[i], i, slides.length), { waitUntil: 'networkidle' });
  const name = `slide-${String(i + 1).padStart(2, '0')}.png`;
  await page.screenshot({ path: path.join(outDir, name) });
  written.push(name);
  console.log('✓ rendered', name);
}
await browser.close();
fs.copyFileSync(contentPath, path.join(outDir, 'deck.used.json'));
console.log(`\nDone — ${written.length} slides in ${outDir}/`);
