import { Box, useColorModeValue } from '@chakra-ui/react';
import Link from 'next/link';
import { ReactNode } from 'react';

export const ButtonLink = ({
  testId,
  href,
  backgroundColor,
  props,
  children
}: {
  testId: string;
  href: string;
  backgroundColor?: string;
  props?: object;
  children: ReactNode;
}) => {
  return (
    <Link
      href={href}
      style={{
        color: useColorModeValue('#333333', '#C8D1D9'),
        fontWeight: '400',
        textDecoration: 'none'
      }}
    >
      <Box
        data-test-id={testId}
        display={'flex'}
        alignItems={'center'}
        backgroundColor={backgroundColor}
        borderRadius={'0.3rem'}
        cursor={'pointer'}
        {...props}
      >
        {children}
      </Box>
    </Link>
  );
};

export const ButtonLinkIcon = ({
  props,
  children
}: {
  props?: object;
  children: ReactNode;
}) => {
  return <Box {...props}>{children}</Box>;
};

export const ButtonLinkText = ({
  color,
  props,
  children
}: {
  color?: string;
  props?: object;
  children: ReactNode;
}) => {
  return (
    <Box style={{ userSelect: 'none', color }} {...props}>
      {children}
    </Box>
  );
};
