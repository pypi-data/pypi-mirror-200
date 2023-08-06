import { Box, Image, VStack, useColorModeValue } from '@chakra-ui/react';
import { config } from '@fortawesome/fontawesome-svg-core';
import '@fortawesome/fontawesome-svg-core/styles.css';
import {
  faFileAlt,
  faRunning,
  faTable
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Link from 'next/link';

import { bodyMinHeight } from '../../utils/constants';

config.autoAddCss = false; /* eslint-disable import/first */

export const NavBar = () => {
  const color = useColorModeValue('#333333', '#C8D1D9');

  return (
    <VStack
      style={{ fontSize: 16 }}
      spacing={5}
      borderRightColor={useColorModeValue('#E5E5E5', '#242526')}
      borderRightWidth={1.5}
      paddingLeft={4}
      paddingRight={4}
      backgroundColor={useColorModeValue('#FFFFFF', '#242526')}
      fontWeight={500}
    >
      <Box minHeight={bodyMinHeight}>
        <Box
          style={{
            position: 'sticky',
            top: '2rem',
            display: 'flex',
            flexDirection: 'column'
          }}
        >
          <Link href="/" style={{ textDecoration: 'none', color }}>
            <Box marginTop={1}>
              <Image
                style={{
                  height: '3rem',
                  marginBottom: '1rem',
                  opacity: useColorModeValue(1, 0.78)
                }}
                src="https://raw.githubusercontent.com/laminlabs/lamin-profile/main/assets/logo.svg"
                alt=""
              />
            </Box>
          </Link>

          <Link href="/table" style={{ textDecoration: 'none', color }}>
            <Box marginTop={'3rem'} justifyContent={'center'} display={'flex'}>
              <FontAwesomeIcon icon={faTable} size={'2x'} />
            </Box>
          </Link>

          <Link href="/run" style={{ textDecoration: 'none', color }}>
            <Box marginTop={'3rem'} justifyContent={'center'} display={'flex'}>
              <FontAwesomeIcon icon={faRunning} size={'2x'} />
            </Box>
          </Link>

          <Link href="/file" style={{ textDecoration: 'none', color }}>
            <Box marginTop={'3rem'} justifyContent={'center'} display={'flex'}>
              <FontAwesomeIcon icon={faFileAlt} size={'2x'} />
            </Box>
          </Link>
        </Box>
      </Box>
    </VStack>
  );
};
