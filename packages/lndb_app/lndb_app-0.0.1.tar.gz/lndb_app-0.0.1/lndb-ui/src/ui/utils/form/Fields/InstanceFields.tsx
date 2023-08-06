import {
  Box,
  Checkbox,
  CheckboxGroup,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Select,
  Stack,
  Textarea
} from '@chakra-ui/react';

import {
  checkInstanceDescriptionLength,
  checkInstanceName,
  checkInstanceNameLength,
  extractNotUrlSafe,
  isUrlSafe
} from '../../../../utils/checks';
import { FormInput } from '../FormInput';

export const InstanceNameInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Instance name'}
    textHelper={'Unique to a specific owner account.'}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('name', value)}
    isInvalid={(value: any) => !checkInstanceName(value)}
    checks={[
      {
        function: (value: any) => isUrlSafe(value),
        message: value =>
          `This instance name contains not allowed characters: ${extractNotUrlSafe(
            value
          )}`
      },
      {
        function: (value: any) => checkInstanceNameLength(value),
        message: () =>
          'Instance name has to be between 1 and 40 characters length.'
      }
    ]}
    testId={'instance-name-input'}
  />
);

export const InstanceStorageRootInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Storage root'}
    textHelper={undefined}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('storage', value)}
    isInvalid={(value: any) => undefined}
    checks={[]}
    testId={'instance-storage-input'}
  />
);

export const InstanceDbInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Database url'}
    textHelper={undefined}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('db', value)}
    isInvalid={(value: any) => undefined}
    checks={[]}
    testId={'instance-db-input'}
  />
);

export const InstanceSchemaInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string[]) => void;
  prevValue: string[];
  currentValue: string[];
}) => {
  const schemaModules = ['bionty', 'wetlab'];

  return (
    <FormControl>
      <FormLabel>Schema modules</FormLabel>
      <CheckboxGroup
        colorScheme="green"
        defaultValue={prevValue}
        onChange={(values: string[]) => updateField('schema', values)}
      >
        <Stack spacing={[1, 5]} direction={['column', 'row']}>
          {schemaModules.map(schemaModule => (
            <Checkbox key={schemaModule} value={schemaModule}>
              {schemaModule}
            </Checkbox>
          ))}
        </Stack>
      </CheckboxGroup>
      <FormHelperText>{undefined}</FormHelperText>
      {[].map((check, i) => {
        return (
          <Box key={i}>
            {!check.function(currentValue) ? (
              <FormErrorMessage>{check.message(currentValue)}</FormErrorMessage>
            ) : undefined}
          </Box>
        );
      })}
    </FormControl>
  );
};

export const InstanceDescriptionInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => (
  <FormInput
    label={'Description'}
    textHelper={undefined}
    placeholder={prevValue}
    currentValue={currentValue}
    update={(value: any) => updateField('description', value)}
    isInvalid={(value: any) => !checkInstanceDescriptionLength(value)}
    checks={[
      {
        function: (value: any) => checkInstanceDescriptionLength(value),
        message: () => 'Description has to be maximum 250 characters length.'
      }
    ]}
    testId={'instance-description-input'}
    InputComponent={Textarea}
  />
);

export const InstanceTypeInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => {
  return (
    <FormControl>
      <FormLabel>Database type</FormLabel>
      <Select
        data-test-id="instance-db-type-drop-down"
        onChange={(e: any) => updateField('type', e.target.value)}
        value={currentValue}
      >
        {['sqlite', 'postgres'].map(type => (
          <option key={type} value={type}>
            {type}
          </option>
        ))}
      </Select>
    </FormControl>
  );
};

export const InstanceVisibilityInput = ({
  updateField,
  prevValue,
  currentValue
}: {
  updateField: (key: string, value: string) => void;
  prevValue: string;
  currentValue: string;
}) => {
  return (
    <FormControl>
      <FormLabel>Visibility</FormLabel>
      <Select
        data-test-id="instance-visibility-drop-down"
        onChange={(e: any) => updateField('visibility', e.target.value)}
        value={currentValue}
      >
        {['private', 'public'].map(type => (
          <option key={type} value={type}>
            {type}
          </option>
        ))}
      </Select>
    </FormControl>
  );
};
