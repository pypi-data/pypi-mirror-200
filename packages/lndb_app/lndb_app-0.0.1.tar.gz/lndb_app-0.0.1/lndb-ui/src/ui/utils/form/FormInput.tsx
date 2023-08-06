import {
  Box,
  FormControl,
  FormErrorMessage,
  FormHelperText,
  FormLabel,
  Input,
  InputProps,
  TextareaProps
} from '@chakra-ui/react';
import { ChakraComponent } from '@chakra-ui/react';

export const FormInput = ({
  label,
  textHelper,
  placeholder,
  currentValue,
  update,
  isInvalid,
  checks,
  testId,
  InputComponent = Input
}: {
  currentValue: any;
  label: string;
  testId: string;
  update: (value: any) => void;
  placeholder: string;
  textHelper: string;
  isInvalid: (value: string) => boolean;
  checks: {
    function: (value: any) => boolean;
    message: (value?: any) => string;
  }[];
  InputComponent?:
    | ChakraComponent<'textarea', TextareaProps>
    | ChakraComponent<'input', InputProps>;
}) => {
  return (
    <FormControl isInvalid={isInvalid(currentValue)}>
      <FormLabel>{label}</FormLabel>
      <InputComponent
        type={'text'}
        data-test-id={testId}
        onChange={e => update(e.target.value)}
        placeholder={placeholder}
      />
      <FormHelperText>{textHelper}</FormHelperText>
      {checks.map((check, i) => {
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
