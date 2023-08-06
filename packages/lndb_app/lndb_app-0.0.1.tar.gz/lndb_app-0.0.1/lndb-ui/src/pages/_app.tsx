import { Box, ChakraProvider } from '@chakra-ui/react';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Head from 'next/head';

import { useInstanceSchema } from '../services/introspection';
import { theme } from '../theme';
import { NavBar } from '../ui/nav-bar/NavBar';

function MyApp({ Component, pageProps }) {
  const { loading, instanceSchema } = useInstanceSchema();

  return (
    <Box>
      <Head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#000000" />
        <title>Data infrastructure for biology &#8212; Lamin</title>
        <meta
          name="description"
          content="Enable data scientists and engineers with a shared data layer for R&D teams."
        />
      </Head>
      <ChakraProvider theme={theme}>
        <Box style={{ flexDirection: 'row', display: 'flex' }}>
          <NavBar />
          <Box width={'100%'}>
            <Component {...pageProps} />
          </Box>
        </Box>
      </ChakraProvider>
    </Box>
  );
}

export default MyApp;
