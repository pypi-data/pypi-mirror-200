import test, { expect } from '@playwright/test';
import { nanoid } from 'nanoid';

import { createPageWithSignUpUser } from './createPageWithSignUpUser';
import { deleteUser } from './utils';

export default function createTests() {
  test('Navigate to settings', async ({
    page: basePage,
    browserName,
    baseURL
  }) => {
    const { page, user, redirectToBaseUrl } = await createPageWithSignUpUser(
      basePage,
      baseURL,
      browserName
    );

    // Go to home page
    await page.goto(redirectToBaseUrl);

    // Go to settings
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=main-menu-settings-button').click();
    await expect(page).toHaveURL(`${redirectToBaseUrl}/settings/profile`);

    // Go to settings authentication section
    await page.locator('data-test-id=settings-authentication-button').click();
    await expect(page).toHaveURL(
      `${redirectToBaseUrl}/settings/authentication`
    );

    // Go to settings profile section
    await page.locator('data-test-id=settings-profile-button').click();
    await expect(page).toHaveURL(`${redirectToBaseUrl}/settings/profile`);

    // Delete user
    await deleteUser(user.id);
  });
  test('Update profile settings', async ({
    page: basePage,
    browserName,
    baseURL
  }) => {
    const { page, user, redirectToBaseUrl } = await createPageWithSignUpUser(
      basePage,
      baseURL,
      browserName
    );

    // Go to home page
    await page.goto(redirectToBaseUrl);

    // Go to settings
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=main-menu-settings-button').click();
    await expect(page).toHaveURL(`${redirectToBaseUrl}/settings/profile`);

    // Check placeholder handle value
    await page.waitForSelector(`[placeholder="${user.handle}"]`);

    // Check update profile button is disable
    expect(
      await page
        .locator('data-test-id=settings-update-profile-button')
        .isDisabled()
    ).toBeTruthy();

    // Update handle
    await page.locator('data-test-id=handle-input').fill(user.handle + '-new');
    await page.locator('data-test-id=settings-update-profile-button').click();

    // Check toast message
    await page.waitForSelector('text=User profile successfully update');

    // Check update profile button is disable
    await page.waitForSelector(`[placeholder="${user.handle + '-new'}"]`);
    expect(
      await page
        .locator('data-test-id=settings-update-profile-button')
        .isDisabled()
    ).toBeTruthy();

    // Update other fields
    await page.locator('data-test-id=settings-name-input').fill('name');
    await page.locator('data-test-id=settings-bio-input').fill('bio');
    await page.locator('data-test-id=settings-github-input').fill('github');
    await page.locator('data-test-id=settings-linkedin-input').fill('linkedin');
    await page.locator('data-test-id=settings-twitter-input').fill('twitter');
    await page
      .locator('data-test-id=settings-website-input')
      .fill('www.website.com');
    await page.locator('data-test-id=settings-update-profile-button').click();

    // Check toast message
    await page.waitForSelector('text=User profile successfully update');

    // Check placeholder values
    await page.waitForSelector(`[placeholder="${user.handle + '-new'}"]`);
    await page.waitForSelector('[placeholder="name"]');
    await page.waitForSelector('[placeholder="bio"]');
    await page.waitForSelector('[placeholder="github"]');
    await page.waitForSelector('[placeholder="linkedin"]');
    await page.waitForSelector('[placeholder="twitter"]');
    await page.waitForSelector('[placeholder="www.website.com"]');
  });
  test('Update authentication settings', async ({
    page: basePage,
    browserName,
    baseURL
  }) => {
    const { page, user, redirectToBaseUrl } = await createPageWithSignUpUser(
      basePage,
      baseURL,
      browserName
    );

    // Go to home page
    await page.goto(redirectToBaseUrl);

    // Go to settings
    await page.locator('data-test-id=main-menu-button').click();
    await page.locator('data-test-id=main-menu-settings-button').click();

    // Go to settings authentication section
    await page.locator('data-test-id=settings-authentication-button').click();
    await expect(page).toHaveURL(
      `${redirectToBaseUrl}/settings/authentication`
    );

    // Check reset email button is disable
    expect(
      await page
        .locator('data-test-id=settings-reset-email-button')
        .isDisabled()
    ).toBeTruthy();

    // Reset email
    await page
      .locator('data-test-id=settings-reset-email-input')
      .fill('updated_' + user.email);
    await page.locator('data-test-id=settings-reset-email-button').click();

    // Check toast message
    await page.waitForSelector('text=Please check your email');

    // Reset password

    const password = nanoid(10);

    await page.locator('data-test-id=reset-password-input').fill(password);
    await page
      .locator('data-test-id=confirm-reset-password-input')
      .fill(password);
    await page.locator('data-test-id=reset-password-button').click();

    // Check toast message
    await page.waitForSelector('text=Password successfully reset');
  });
}
