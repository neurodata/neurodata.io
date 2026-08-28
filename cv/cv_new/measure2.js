const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 } });
  await page.emulateMedia({ media: 'print' });
  await page.goto('file://' + path.resolve(__dirname, 'cv.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const result = await page.evaluate(() => {
    const el = document.querySelector('.entry-line');
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const span = document.createElement('span');
    span.style.font = cs.font;
    span.style.whiteSpace = 'nowrap';
    span.style.position = 'absolute';
    span.style.visibility = 'hidden';
    document.body.appendChild(span);
    const sample = 'Department of Applied Mathematics and Statistics, JHU, Baltimore, MD, USA 0123456789';
    span.textContent = sample;
    const textWidth = span.getBoundingClientRect().width;
    const charsPerUnit = sample.length / textWidth;
    const availableChars = rect.width * charsPerUnit;
    document.body.removeChild(span);
    return { columnWidthPx: rect.width, font: cs.font, estCharsAvailable: availableChars };
  });
  console.log(JSON.stringify(result, null, 2));
  await browser.close();
})();
