import { chromium } from 'playwright-core';
import { execSync } from 'child_process';
import fs from 'fs';

// locate the downloaded headless shell
const base = '/root/.cache/ms-playwright';
const dir = fs.readdirSync(base).find(d => d.startsWith('chromium_headless_shell'));
const exe = execSync(`find ${base}/${dir} -name 'chrome-headless-shell' -type f | head -1`).toString().trim();

const slides = JSON.parse(fs.readFileSync('carousel/slides.json','utf8'));
const browser = await chromium.launch({ executablePath: exe });
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });

for (const s of slides) {
  const html = fs.readFileSync(`carousel/${s}.html`,'utf8');
  await page.setContent(html, { waitUntil: 'networkidle' });
  await page.screenshot({ path: `carousel/${s}.png` });
  console.log('rendered', s);
}
await browser.close();
