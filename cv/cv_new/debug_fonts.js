const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const filePath = 'file://' + path.resolve(__dirname, 'cv.html');
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('requestfailed', req => console.log('FAILED:', req.url(), req.failure()));
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const info = await page.evaluate(() => {
    const list = [];
    document.fonts.forEach(f => list.push(f.family + ' ' + f.weight + ' status=' + f.status));
    return {count: document.fonts.size, list, bodyFont: getComputedStyle(document.body).fontFamily, headFont: getComputedStyle(document.querySelector('h3')).fontFamily};
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
