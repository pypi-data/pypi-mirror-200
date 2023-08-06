import { test } from '@playwright/test';

import { deleteUser, generateLinkToCreateUser } from './utils';

export default function createTests() {
  test('Finishing signup process', async ({ page, browserName, baseURL }) => {
    const { actionLink, redirectToBaseUrl, user } =
      await generateLinkToCreateUser(baseURL, browserName);

    // Go to signup page using a token
    await page.goto(actionLink, { waitUntil: 'networkidle' });

    // Wait for supabase session to be loaded
    await page.waitForSelector('data-test-id=main-menu-avatar');

    // Fill input
    await page.locator('data-test-id=sign-up-handle-input').fill(user.handle);

    // Confirm
    const navigationPromise = page.waitForNavigation({
      url: redirectToBaseUrl
    });
    await page.locator('data-test-id=sign-up-confirm-button').click();
    await navigationPromise;

    // Check toast message
    await page.waitForSelector('text=Account successfully created');

    // Delete user
    await deleteUser(user.id);
  });
}
