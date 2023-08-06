import { expect, test } from '@playwright/test';

export default function createTests() {
  test('Navigate to Documentation', async ({ page, baseURL }) => {
    await page.goto(baseURL);
    const navigationPromise = page.waitForNavigation({
      url: `${baseURL}/docs`
    });
    await page.locator('a:has-text("Documentation")').click();
    await navigationPromise;
  });

  test('Navigate to Pricing', async ({ page, baseURL }) => {
    await page.goto(baseURL);
    await page.locator('text=Pricing').click();
    await expect(page).toHaveURL(`${baseURL}/pricing`);
  });

  test('Navigate to Blog', async ({ page, baseURL }) => {
    await page.goto(baseURL);
    const navigationPromise = page.waitForNavigation({
      url: `${baseURL}/blog`
    });
    await page.locator('text=Blog').click();
    await navigationPromise;
  });

  test('Navigate to About', async ({ page, baseURL }) => {
    await page.goto(baseURL);
    const navigationPromise = page.waitForNavigation({
      url: `${baseURL}/about`
    });
    await page.locator('text=About').click();
    await navigationPromise;
  });

  // test('Navigate to Home page using Lamin logo', async ({ page, baseURL }) => {
  //   await page.locator('text=LaminDocumentationPricingBlogReportsAboutLogin >> img').click();
  //   await expect(page).toHaveURL(baseURL);
  // })
}
