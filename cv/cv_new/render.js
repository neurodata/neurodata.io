const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const filePath = 'file://' + path.resolve(__dirname, 'cv.html');
  await page.goto(filePath, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);

  await page.pdf({
    path: 'jovo_cv.pdf',
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.62in', bottom: '0.55in', left: '0.72in', right: '0.72in' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `
      <div style="width:100%; font-family: 'EB Garamond', Georgia, serif; font-size:8pt; color:#888; text-align:center; padding-top:2pt;">
        Page <span class="pageNumber"></span> of <span class="totalPages"></span>
      </div>`,
  });

  await browser.close();
  console.log('done');
})();
