import { test } from '@playwright/test';

import ForgotPassword from './forgot-password.spec';
import Instance from './instance.spec';
import Login from './login.spec';
import Logout from './logout.spec';
import NavBar from './nav-bar.spec';
import Profile from './profile.spec';
import ResetPassword from './reset-password.spec';
import Settings from './settings.spec';
import SignUp from './signup.spec';
import { deleteCIUsers } from './utils';

test.use({
  headless: true
});

test.describe(SignUp);
test.describe(ForgotPassword);
test.describe(ResetPassword);
test.describe(NavBar);
test.describe(Login);
test.describe(Settings);
test.describe(Logout);
test.describe(Profile);
test.describe(Instance);

test.afterAll(async () => {
  await deleteCIUsers();
});
