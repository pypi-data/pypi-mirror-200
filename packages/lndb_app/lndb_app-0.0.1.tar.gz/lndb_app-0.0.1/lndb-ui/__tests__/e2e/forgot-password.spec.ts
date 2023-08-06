import { expect, test } from '@playwright/test';

export default function createTests() {
  test('Sending a request to reset password', async ({ page, baseURL }) => {
    // Go to home page
    await page.goto(baseURL);

    // Go to login page
    const navigationPromise1 = page.waitForNavigation({
      url: `${baseURL}/log-in`
    });
    await page.locator('data-test-id=main-menu-log-in-button').click();
    await navigationPromise1;

    // Go to forgot password page
    const navigationPromise2 = page.waitForNavigation({
      url: `${baseURL}/forgot-password`
    });
    await page.locator('data-test-id=forgot-password-link').click();
    await navigationPromise2;

    // Check confirm button is disable
    expect(
      await page
        .locator('data-test-id=forgot-password-confirm-button')
        .isDisabled()
    ).toBeTruthy();

    // Fill email
    await page
      .locator('data-test-id=forgot-password-email-input')
      .fill('testuser1@lamin.ai');

    // Check confirm button is enable
    expect(
      await page
        .locator('data-test-id=forgot-password-confirm-button')
        .isDisabled()
    ).toBeFalsy();
  });
}
