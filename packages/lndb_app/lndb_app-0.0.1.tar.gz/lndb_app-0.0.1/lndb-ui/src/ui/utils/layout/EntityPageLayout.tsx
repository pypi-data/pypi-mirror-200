import { Box } from '@chakra-ui/react';
import { ReactNode } from 'react';

import { bodyMinHeight, bodyWidth } from '../../../utils/constants';

export const EntityPageLayout = ({ children }: { children: ReactNode }) => {
  return (
    <Box
      style={{ minHeight: bodyMinHeight, display: 'flex' }}
      flexDirection={{ base: 'column', md: 'row' }}
    >
      {children}
    </Box>
  );
};

export const EntityPageMenu = ({ children }: { children: ReactNode }) => {
  return (
    <Box
      width={{ base: undefined, md: '20rem' }}
      padding={'2rem'}
      borderRightWidth={{ base: 0, md: 1 }}
      borderBottomWidth={{ base: 1, md: 0 }}
      minHeight={{ base: undefined, md: bodyMinHeight }}
    >
      <Box
        width={{ base: '100%', md: '100%' }}
        style={{
          position: 'sticky',
          top: '2rem',
          display: 'flex',
          flexDirection: 'column'
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export const EntityPageMargin = () => {
  return (
    <Box
      width={{ base: 0, md: '20rem' }}
      padding={{ base: 0, md: '2rem' }}
      minHeight={{ base: 0, md: bodyMinHeight }}
     
    />
  );
};

export const EntityPageMenuSections = ({
  children
}: {
  children: ReactNode;
}) => {
  return (
    <Box display={'flex'} flexDirection={{ base: 'row', md: 'column' }}>
      {children}
    </Box>
  );
};

export const EntityPageMenuTitle = ({ children }: { children: ReactNode }) => {
  return (
    <Box style={{ fontWeight: 'bold', paddingBottom: '1rem' }}>{children}</Box>
  );
};

export const EntityPageBody = ({ children }: { children: ReactNode }) => {
  return (
    <Box padding={'2rem'} maxWidth={bodyWidth} flex={1}>
      {children}
    </Box>
  );
};
