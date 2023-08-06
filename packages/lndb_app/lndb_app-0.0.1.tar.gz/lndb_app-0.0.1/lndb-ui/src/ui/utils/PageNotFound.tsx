import { Box, Container, VStack } from '@chakra-ui/react';
import Image from 'next/image';

export const PageNotFound = () => {
  return (
    <Container
      maxW={'container.lg'}
      marginTop={'5%'}
      marginBottom={'5%'}
      data-test-id="page-not-found-component"
    >
      <VStack spacing={5}>
        <Box fontSize={70} fontWeight={'bold'}>
          404
        </Box>
        <Box fontSize={50}>Page not found</Box>
        <Image src="/526-lemon.svg" height={'300'} width={'300'} alt="" />
      </VStack>
    </Container>
  );
};
