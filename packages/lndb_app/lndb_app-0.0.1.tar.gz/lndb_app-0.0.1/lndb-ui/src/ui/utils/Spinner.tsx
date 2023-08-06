import { Spinner as ChakraUISpinner, VStack } from '@chakra-ui/react';

import { bodyMinHeight } from '../../utils/constants';

export const Spinner = () => {
  return (
    <VStack height={bodyMinHeight} justifyContent={'center'}>
      <ChakraUISpinner
        thickness="4px"
        speed="0.65s"
        emptyColor="gray.200"
        color="#2F8555"
        size="xl"
      />
    </VStack>
  );
};

export const MiniSpinner = () => {
  return (
    <ChakraUISpinner
      thickness="4px"
      speed="0.65s"
      emptyColor="gray.200"
      color="#2F8555"
      size="md"
    />
  );
};
