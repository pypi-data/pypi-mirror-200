import { expect, test } from '@playwright/test';

import { createPageWithLoggedInUser } from './createPageWithLoggedInUser';
import { createPageWithSignUpUser } from './createPageWithSignUpUser';
import { deleteUser } from './utils';

export default function createTests() {
  test('Instance page visited by a user with admin permision', async ({
    page: basePage,
    baseURL
  }) => {
    const { page, user } = await createPageWithLoggedInUser(
      '2e35fa63-05d6-47f6-9d40-c56383ff04a3',
      'static-testuser1',
      'static-testuser1@lamin.ai',
      'static-testuser1-password',
      basePage,
      baseURL
    );

    // Go to instance page
    await page.goto(`${baseURL}/static-testuser1/static-testinstance1`);
    await page.waitForLoadState('networkidle');

    // Go to collaborators tab
    await page.locator('data-test-id=instance-page-collaborators-tab').click();
    await expect(page).toHaveURL(
      `${baseURL}/static-testuser1/static-testinstance1?tab=collaborators`
    );

    // Check listed collaborators
    await page.waitForSelector('text=static-testuser1');
    await page.waitForSelector('text=static-testuser2');

    // Check add collaborator button
    await page.waitForSelector('data-test-id=add-collaborator-button');

    // Check update collaborator permission button
    await page.waitForSelector(
      'data-test-id=collaborator-permission-drop-down'
    );

    // Check delete collaborator button
    await page.waitForSelector('data-test-id=delete-collaborator-button');

    // Check settings tab
    await page.waitForSelector('data-test-id=instance-page-settings-tab');

    // Go to collaborator page
    await page.locator('h2:has-text("static-testuser2")').click();
    await page.waitForURL(`${baseURL}/static-testuser2`);
  });
  test('Instance page visited by a user with read permission', async ({
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

    // Go to instance page
    await page.goto(`${baseURL}/static-testuser1/static-testinstance1`);

    // Go to collaborators tab
    await page.locator('data-test-id=instance-page-collaborators-tab').click();
    await expect(page).toHaveURL(
      `${baseURL}/static-testuser1/static-testinstance1?tab=collaborators`
    );

    // Check listed collaborators
    await page.waitForSelector('text=static-testuser1');
    await page.waitForSelector('text=static-testuser2');

    // Check add collaborator button
    await expect(
      page.locator('data-test-id=add-collaborator-button')
    ).toHaveCount(0);

    // Check update collaborator permission button
    await expect(
      page.locator('data-test-id=collaborator-permission-drop-down')
    ).toHaveCount(0);

    // Check delete collaborator button
    await expect(
      page.locator('data-test-id=delete-collaborator-button')
    ).toHaveCount(0);

    // Check settings tab
    await expect(
      page.locator('data-test-id=instance-page-settings-tab')
    ).toHaveCount(0);

    // Go to collaborator page
    await page.locator('h2:has-text("static-testuser1")').click();
    await page.waitForURL(`${baseURL}/static-testuser1`);
  });
  test('Instance management (create, update, delete)', async ({
    page: basePage,
    baseURL,
    browserName
  }) => {
    const { page, user } = await createPageWithSignUpUser(
      basePage,
      baseURL,
      browserName
    );
    const instanceName = `lamin.ci.instance.${Date.now().toString().slice(7)}`;

    // Go to a profile page
    await page.goto(`${baseURL}/${user.handle}`);

    // Go to instances tab
    await page.waitForSelector('data-test-id=profile-page-instances-tab');
    await page.locator('data-test-id=profile-page-instances-tab').click();
    await expect(page).toHaveURL(`${baseURL}/${user.handle}?tab=instances`);

    // Create an instance
    await page.waitForSelector('data-test-id=create-instance-button');
    await page.locator('data-test-id=create-instance-button').click();
    await page.locator('data-test-id=instance-name-input').fill(instanceName);
    await page
      .locator('data-test-id=instance-storage-input')
      .fill('s3://lndb-setup-ci');
    await page
      .locator('data-test-id=instance-db-input')
      .fill(`postgresql://user:password@host:5432/${instanceName}`);
    await page
      .locator('data-test-id=instance-description-input')
      .fill('Instance description.');
    await page.locator('data-test-id=confirm-create-instance-button').click();
    await page.waitForURL(`${baseURL}/${user.handle}/${instanceName}`);

    // Go to collaborators tab
    await page.locator('data-test-id=instance-page-collaborators-tab').click();
    await expect(page).toHaveURL(
      `${baseURL}/${user.handle}/${instanceName}?tab=collaborators`
    );

    // Check listed collaborators
    await page.waitForSelector(`text=${user.handle}`);

    // Add a collaborator
    await page.locator('data-test-id=add-collaborator-button').click();
    await page.locator('data-test-id=handle-input').fill('testuser1');
    await page.locator('data-test-id=confirm-add-collaborator-button').click();

    // Check listed collaborators
    await page.waitForSelector(`text=${user.handle}`);
    await page.waitForSelector('text=testuser1');

    // Update collaborator permission
    await page
      .locator('data-test-id=collaborator-permission-drop-down')
      .nth(1)
      .selectOption('read-write');
    await page
      .locator('data-test-id=confirm-update-account-permission-button')
      .click();
    await page.waitForLoadState('networkidle');
    await page.waitForSelector('text=Account permission successfully updated');

    // Check collaborators permission
    await page.waitForTimeout(2000);
    expect(
      await page
        .locator('data-test-id=collaborator-permission-current-value')
        .nth(0)
        .textContent()
    ).toEqual('admin');
    expect(
      await page
        .locator('data-test-id=collaborator-permission-current-value')
        .nth(1)
        .textContent()
    ).toEqual('read-write');

    // Delete a collaborator
    await page
      .locator('data-test-id=delete-collaborator-button')
      .nth(1)
      .click();
    await page.locator('data-test-id=confirm-delete-account-button').click();
    await page.waitForLoadState('networkidle');

    // Check listed collaborators
    await page.waitForSelector(`text=${user.handle}`);
    await expect(
      page.locator('data-test-id=delete-collaborator-button')
    ).toHaveCount(1);

    // Update instance settings
    await page.locator('data-test-id=instance-page-settings-tab').click();
    await page
      .locator('data-test-id=instance-visibility-drop-down')
      .selectOption('public');
    await page
      .locator('data-test-id=instance-description-input')
      .fill('Instance new description.');
    await page.locator('data-test-id=settings-update-instance-button').click();
    await page.waitForLoadState('networkidle');

    // Check updated instance
    await page.waitForSelector('text=Instance new description.');
    expect(
      await page.locator('data-test-id=instance-visibility').textContent()
    ).toEqual('Public');

    // Delete instance
    await page.locator('data-test-id=delete-instance-button').click();
    await page.waitForURL(baseURL);

    // Check instance is deleted
    await page.goto(`${baseURL}/${user.handle}/${instanceName}`);
    await page.waitForSelector('data-test-id=page-not-found-component');

    await deleteUser(user.id);
  });
}
