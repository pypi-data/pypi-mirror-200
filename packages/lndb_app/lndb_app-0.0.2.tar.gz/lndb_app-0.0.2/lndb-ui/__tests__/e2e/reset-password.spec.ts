import { test } from '@playwright/test';
import { nanoid } from 'nanoid';

import { createUser, deleteUser, generateLinkToResetPassword } from './utils';

export default function createTests() {
  test('Reset a user password using confirmation link', async ({
    page,
    browserName,
    baseURL
  }) => {
    const { id, email } = await createUser(browserName);
    const { actionLink, redirectToBaseUrl } = await generateLinkToResetPassword(
      baseURL,
      email
    );
    const password = nanoid(10);

    // Reset password
    await page.goto(actionLink);
    await page.locator('data-test-id=reset-password-input').fill(password);
    await page
      .locator('data-test-id=confirm-reset-password-input')
      .fill(password);
    const navigationPromise1 = page.waitForNavigation({
      url: redirectToBaseUrl
    });
    await page.locator('data-test-id=reset-password-button').click();
    await navigationPromise1;

    // Check toast message
    await page.waitForSelector('text=Password successfully reset');

    // Log out
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=log-out-button').click();

    // Log in with new password
    await page.locator('data-test-id=main-menu-log-in-button').click();
    await page.locator('data-test-id=log-in-email-input').fill(email);
    await page.locator('data-test-id=log-in-password-input').fill(password);
    const navigationPromise2 = page.waitForNavigation({
      url: redirectToBaseUrl
    });
    await page.locator('data-test-id=log-in-button').click();
    await navigationPromise2;

    // Delete user
    await deleteUser(id);
  });
}
