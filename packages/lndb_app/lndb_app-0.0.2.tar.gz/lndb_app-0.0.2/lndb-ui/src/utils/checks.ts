// Account

export const checkHandle = (handle: string | undefined) => {
  if (handle) {
    if (!checkHandleLength(handle)) return false;
    if (!isUrlSafe(handle)) return false;
  }
  return true;
};

export const checkPassword = (
  password: string | undefined,
  passwordConfirmation: string | undefined
) => {
  if (password && passwordConfirmation) {
    return (
      checkPasswordLength(password) &&
      checkPasswordAreEqual(password, passwordConfirmation)
    );
  }
  return true;
};

export const checkHandleLength = (handle: string) => {
  if (handle) return handle.length >= 3 && handle.length <= 30;
  return true;
};

export const checkNameLength = (name: string) => {
  if (name) return name.length >= 4 && name.length <= 30;
  return true;
};

export const checkBioLength = (bio: string) => {
  if (bio) return bio.length <= 250;
  return true;
};

export const checkPasswordLength = (password: string) => {
  if (password) {
    return password.length >= 6 && password.length <= 99;
  }
  return true;
};

export const checkPasswordAreEqual = (
  password: string | undefined,
  passwordConfirmation: string | undefined
) => {
  if (password && passwordConfirmation) {
    return password === passwordConfirmation;
  }
  return true;
};

export const isUrlSafe = (str: string) => {
  if (str) return /^[a-zA-Z0-9-._~]+$/.test(str);
  return true;
};

export const extractNotUrlSafe = (str: string) => {
  return str.match(/[^a-zA-Z0-9-._~]+/g) || [];
};

export const isValidEmail = (email: string) => {
  if (email) {
    const emailRegex =
      /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
    return emailRegex.test(email);
  }
  return true;
};

export const isValidGithubHandle = (handle: string) => {
  if (handle) {
    if (handle.length > 39) return false;
    if (!/^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$/i.test(handle)) return false;
  }
  return true;
};

export const isValidLinkedInProfileUrl = (url: string) => {
  if (url) {
    const linkedInProfileUrlRegex =
      /^(https?:\/\/[\w]+\.linkedin\.com\/in\/[\w\u00C0-\u017F-]+\/?)$/;
    return linkedInProfileUrlRegex.test(url);
  }
  return true;
};

export const isValidTwitterHandle = (handle: string) => {
  if (handle) {
    if (handle.length > 15) return false;
    if (!/^[a-zA-Z0-9_]+$/.test(handle)) return false;
  }
  return true;
};

export const isValidWebsiteUrl = (websiteUrl: string) => {
  if (websiteUrl) {
    const urlRegex =
      /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/;
    return urlRegex.test(websiteUrl);
  }
  return true;
};

// Instance

export const checkInstanceDescriptionLength = (description: string) => {
  if (description) return description.length <= 250;
  return true;
};

export const checkInstanceNameLength = (name: string) => {
  if (name) return name.length >= 1 && name.length <= 40;
  return true;
};

export const checkInstanceName = (name: string | undefined) => {
  if (name) {
    if (!checkInstanceNameLength(name)) return false;
    if (!isUrlSafe(name)) return false;
  }
  return true;
};
