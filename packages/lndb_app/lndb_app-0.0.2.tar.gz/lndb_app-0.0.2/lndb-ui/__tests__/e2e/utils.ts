import { createClient } from '@supabase/supabase-js';
import fetch from 'cross-fetch';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_SECRET,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
);

export const generateLinkToCreateUser = async (baseURL, browserName) => {
  const redirectToBaseUrl = getRedirectToBaseUrl(baseURL);

  const handle = createHandle();
  const email = `${handle}@gmail.com`;
  const password = 'secret';

  const generateLinkResponse = await supabase.auth.admin.generateLink({
    type: 'signup',
    email,
    password,
    options: {
      redirectTo: `${redirectToBaseUrl}/signup`
    }
  });

  const userId = generateLinkResponse.data.user.id;
  const actionLink = generateLinkResponse.data.properties.action_link;

  const user = {
    id: userId,
    handle,
    email,
    password
  };

  return {
    actionLink,
    redirectToBaseUrl,
    user
  };
};

export const generateLinkToResetPassword = async (baseURL, email) => {
  const redirectToBaseUrl = getRedirectToBaseUrl(baseURL);

  const generateLinkResponse = await supabase.auth.admin.generateLink({
    type: 'recovery',
    email,
    options: {
      redirectTo: `${redirectToBaseUrl}/reset-password`
    }
  });

  const actionLink = generateLinkResponse.data.properties.action_link;

  return {
    actionLink,
    redirectToBaseUrl
  };
};

const getRedirectToBaseUrl = baseURL => {
  if (baseURL.includes('laminui-pnrr.netlify.app')) {
    // Netlify generate a new URL for each PR
    // it's not possible to register each them on supabase
    // for the moment we redirect on https://lamin.ai
    return 'https://lamin.ai';
  } else if (
    baseURL.includes('http://localhost:') ||
    baseURL == 'https://lamin.ai'
  ) {
    return baseURL;
  } else {
    throw new Error(`${baseURL} is not authorized for redirect`);
  }
};

export const createUser = async browserName => {
  const handle = createHandle();
  const email = `${handle}@gmail.com`;
  const password = 'secret';

  const createUserResponse = await supabase.auth.admin.createUser({
    email,
    password
  });

  const userId = createUserResponse.data.user.id;

  const user = {
    id: userId,
    handle,
    email,
    password
  };

  return user;
};

const createHandle = () => `lamin.ci.user.${Date.now().toString().slice(7)}`;

export const deleteUser = async userId => {
  await supabase.from('account').delete().eq('id', userId);
  await supabase.auth.admin.deleteUser(userId);
};

export const deleteCIUsers = async () => {
  await fetch(`${process.env.NEXT_PUBLIC_LAMIN_REST_HUB_URL}/ci/users`, {
    method: 'DELETE'
  });
};
