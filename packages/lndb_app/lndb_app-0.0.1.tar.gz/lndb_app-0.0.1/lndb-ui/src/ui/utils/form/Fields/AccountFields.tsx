import {
  Button,
  FormControl,
  FormLabel,
  Text,
  Textarea
} from '@chakra-ui/react';
import { useRef } from 'react';

import {
  checkBioLength,
  checkHandle,
  checkHandleLength,
  checkNameLength,
  extractNotUrlSafe,
  isUrlSafe,
  isValidEmail,
  isValidGithubHandle,
  isValidLinkedInProfileUrl,
  isValidTwitterHandle,
  isValidWebsiteUrl
} from '../../../../utils/checks';
import { creatLinkedinProfileUrl } from '../../../../utils/createUrl';
import { FormInput } from '../FormInput';

export const AvatarInput = ({ updateField, avatar, setAvatar, accountId }) => {
  const avatarRef = useRef<any>();

  return (
    <FormControl>
      <FormLabel htmlFor="name">Profile picture</FormLabel>
      <input
        type="file"
        ref={avatarRef}
        style={{ display: 'none' }}
        onChange={(event: any) => {
          setAvatar(event.target.files[0]);
          updateField(
            'avatar_url',
            `${accountId}/profile-picture/${Date.now()}`
          );
        }}
      ></input>
      <Button type={'button'} onClick={() => avatarRef.current.click()}>
        Click to select a file
      </Button>
      <Text>{avatar ? avatar.name : ''}</Text>
    </FormControl>
  );
};

export const HandleInput = ({
  updateField,
  prevValue,
  currentValue,
  showTextHelper = true
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
  showTextHelper?: boolean;
}) => (
  <FormInput
    label={'Handle'}
    textHelper={
      showTextHelper
        ? 'Unique handle to login into LaminDB and to construct profile URL.'
        : undefined
    }
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('handle', value)}
    isInvalid={(value: any) => !checkHandle(value)}
    checks={[
      {
        function: (value: any) => isUrlSafe(value),
        message: value =>
          `This handle contains not allowed characters: ${extractNotUrlSafe(
            value
          )}`
      },
      {
        function: (value: any) => checkHandleLength(value),
        message: () => 'Handle has to be between 4 and 30 characters length.'
      }
    ]}
    testId={'handle-input'}
  />
);

export const NameInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Name'}
    textHelper={'Name as it appears on the profile.'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('name', value)}
    isInvalid={(value: any) => !checkNameLength(value)}
    checks={[
      {
        function: (value: any) => checkNameLength(value),
        message: () => 'Name has to be between 3 and 30 characters length.'
      }
    ]}
    testId={'settings-name-input'}
  />
);

export const BioInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Bio'}
    textHelper={undefined}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('bio', value)}
    isInvalid={(value: any) => !checkBioLength(value)}
    checks={[
      {
        function: (value: any) => checkBioLength(value),
        message: () => 'Bio has to be maximum 250 characters length.'
      }
    ]}
    testId={'settings-bio-input'}
    InputComponent={Textarea}
  />
);

export const GithubInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Github'}
    textHelper={'Github handle (username).'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('github_handle', value)}
    isInvalid={(value: any) => !isValidGithubHandle(value)}
    checks={[
      {
        function: (value: any) => isValidGithubHandle(value),
        message: () => 'Invalid Github handle.'
      }
    ]}
    testId={'settings-github-input'}
  />
);

export const LinkedinInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Linkedin'}
    textHelper={'LinkedIn handle.'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('linkedin_handle', value)}
    isInvalid={(value: any) =>
      !isValidLinkedInProfileUrl(creatLinkedinProfileUrl(value))
    }
    checks={[
      {
        function: (value: any) =>
          isValidLinkedInProfileUrl(creatLinkedinProfileUrl(value)),
        message: value =>
          `Invalid Linkedin profile url: ${creatLinkedinProfileUrl(value)}.`
      }
    ]}
    testId={'settings-linkedin-input'}
  />
);

export const TwitterInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Twitter'}
    textHelper={'Twitter handle.'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('twitter_handle', value)}
    isInvalid={(value: any) => !isValidTwitterHandle(value)}
    checks={[
      {
        function: (value: any) => isValidTwitterHandle(value),
        message: () => 'Invalid Twitter handle.'
      }
    ]}
    testId={'settings-twitter-input'}
  />
);

export const WebsiteInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Website'}
    textHelper={'Website URL.'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('website', value)}
    isInvalid={(value: any) => !isValidWebsiteUrl(value)}
    checks={[
      {
        function: (value: any) => isValidWebsiteUrl(value),
        message: () => 'Invalid Website URL.'
      }
    ]}
    testId={'settings-website-input'}
  />
);

export const EmailInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Email address'}
    textHelper={`
        Choose the email address you want to use to connect lamin db.
        You must click on the confirmation link you received for the change to be effective!
        `}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField(value)}
    isInvalid={(value: any) => !isValidEmail(value)}
    checks={[
      {
        function: (value: any) => isValidEmail(value),
        message: () => 'This email is not valid.'
      }
    ]}
    testId={'settings-reset-email-input'}
  />
);
