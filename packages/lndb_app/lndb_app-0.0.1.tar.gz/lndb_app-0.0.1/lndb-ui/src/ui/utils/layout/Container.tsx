import { Container as ChakraUiContainer } from '@chakra-ui/react';

export const Container = ({
  children,
  size
}: {
  size: 'lg' | 'md';
  children: any;
}) => {
  return (
    <ChakraUiContainer
      maxW={`container.${size}`}
      justifyContent={'center'}
      display={'flex'}
      flexDirection={'column'}
      marginTop={'4em'}
      marginBottom={'4em'}
    >
      {children}
    </ChakraUiContainer>
  );
};
