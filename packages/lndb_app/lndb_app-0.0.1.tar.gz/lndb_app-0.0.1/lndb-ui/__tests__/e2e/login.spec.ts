import { test } from '@playwright/test';

export default function createTests() {
  test('Login', async ({ page, baseURL }) => {
    const email = 'testuser1@lamin.ai';
    const password = 'cEvcwMJFX4OwbsYVaMt2Os6GxxGgDUlBGILs2RyS';

    // Go to home page
    await page.goto(baseURL);

    // Login
    await page.locator('data-test-id=main-menu-log-in-button').click();
    await page.locator('data-test-id=log-in-email-input').fill(email);
    await page.locator('data-test-id=log-in-password-input').fill(password);
    const navigationPromise1 = page.waitForNavigation({ url: baseURL });
    await page.locator('data-test-id=log-in-button').click();
    await navigationPromise1;

    // Check toast message
    await page.waitForSelector('text=Login success');
  });
}
