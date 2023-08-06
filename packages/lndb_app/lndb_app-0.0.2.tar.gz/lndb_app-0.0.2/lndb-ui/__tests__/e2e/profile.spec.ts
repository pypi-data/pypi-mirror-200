import { expect, test } from '@playwright/test';

import { createPageWithLoggedInUser } from './createPageWithLoggedInUser';

export default function createTests() {
  test('Profile page visited by owner', async ({ page: basePage, baseURL }) => {
    const { page, user } = await createPageWithLoggedInUser(
      '2e35fa63-05d6-47f6-9d40-c56383ff04a3',
      'static-testuser1',
      'static-testuser1@lamin.ai',
      'static-testuser1-password',
      basePage,
      baseURL
    );

    // Go to home page
    await page.goto(baseURL);

    // Go to own profile
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=main-menu-profile-button').click();
    await page.waitForURL(`${baseURL}/static-testuser1`);

    // Go to instances tab
    await page.locator('data-test-id=profile-page-instances-tab').click();
    await expect(page).toHaveURL(`${baseURL}/static-testuser1?tab=instances`);

    // Check listed instances
    await page.waitForSelector('text=static-testinstance1');

    // Check create instance button
    await page.waitForSelector('data-test-id=create-instance-button');

    // Go to instance page
    await page.locator('text=static-testinstance1').click();
    await page.waitForURL(`${baseURL}/static-testuser1/static-testinstance1`);
  });
  test('Profile page visited by another user', async ({
    page: basePage,
    baseURL
  }) => {
    const { page, user } = await createPageWithLoggedInUser(
      '9163df82-d4df-4bb5-9ce3-7e940c491da4',
      'static-testuser2',
      'static-testuser2@lamin.ai',
      'static-testuser2-password',
      basePage,
      baseURL
    );

    // Go to a profile page
    await page.goto(`${baseURL}/static-testuser1`);

    // Go to instances tab
    await page.locator('data-test-id=profile-page-instances-tab').click();
    await expect(page).toHaveURL(`${baseURL}/static-testuser1?tab=instances`);

    // Check create instance button
    await expect(
      page.locator('data-test-id=create-instance-button')
    ).toHaveCount(0);

    // Check listed instances
    await page.waitForSelector('text=static-testinstance1');
  });
}
