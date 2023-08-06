import test, { expect } from '@playwright/test';

import { createPageWithSignUpUser } from './createPageWithSignUpUser';
import { deleteUser } from './utils';

export default function createTests() {
  test('Logout', async ({ page: basePage, baseURL, browserName }) => {
    const { page, user, redirectToBaseUrl } = await createPageWithSignUpUser(
      basePage,
      baseURL,
      browserName
    );

    // Go to home page
    await page.goto(redirectToBaseUrl);

    // Log out
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=log-out-button').click();

    // Check if login button is visibile
    expect(
      await page.locator('data-test-id=main-menu-log-in-button').isVisible()
    );

    deleteUser(user.id);
  });
}
