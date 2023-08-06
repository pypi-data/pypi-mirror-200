import { Page } from '@playwright/test';

export const createPageWithLoggedInUser = async (
  id: string,
  handle: string,
  email: string,
  password: string,
  page: Page,
  baseURL: string
) => {
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

  const user = {
    id,
    handle,
    email,
    password
  };

  return {
    page,
    user
  };
};
