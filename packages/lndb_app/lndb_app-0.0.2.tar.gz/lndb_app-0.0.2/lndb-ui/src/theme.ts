import { extendTheme } from '@chakra-ui/react';
import { StyleFunctionProps, mode } from '@chakra-ui/theme-tools';
import 'ag-grid-community/styles/ag-grid.css';
import 'ag-grid-community/styles/ag-theme-alpine.css';
import 'bootstrap/dist/css/bootstrap.min.css';

export const theme = extendTheme({
  config: {
    initialColorMode: 'system',
    useSystemColorMode: true
  },
  colors: {
    primary: {
      100: '#2e8555'
    }
  },
  styles: {
    global: (props: StyleFunctionProps) => ({
      body: {
        bg: mode('#FFFFFF', '#18191A')(props),
        color: mode('#333333', '#C8D1D9')(props),
        fontFamily:
          '-apple-system,BlinkMacSystemFont,Segoe UI,"Helvetica Neue",Arial,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol'
      },
      innerHeight: '100%',
      a: {
        color: mode('primary.100', '#5EBFA2')(props),
        _hover: {
          color: mode('primary.100', '#5EBFA2')(props),
          textDecoration: 'underline'
        }
      }
    })
  },
  components: {
    Th: {
      baseStyle: {
        textTransform: 'unset'
      }
    },
    Tabs: {
      baseStyle: (props: StyleFunctionProps) => ({
        tab: {
          fontWeight: 500,
          borderRadius: 5,
          _selected: {
            bg: mode('rgba(0, 0, 0, 0.1);', '#1B8870')(props)
          }
        }
      })
    },
    Card: {
      baseStyle: (props: StyleFunctionProps) => ({
        container: {
          bg: mode(undefined, '#242526')(props)
        }
      })
    },
    Button: {
      baseStyle: (props: StyleFunctionProps) => ({
        //borderColor: 'grey',
        borderWidth: 1.5,
        fontWeight: 750,
        padding: 4.5,
        borderColor: mode(undefined, '#C8D1D9')(props),
        color: mode('primary.100', '#5EBFA2')(props),
        bg: mode('#FFFFFF', '#18191A')(props)
      })
    },
    Menu: {
      baseStyle: (props: StyleFunctionProps) => ({
        list: {
          bg: mode('#FFFFFF', '#18191A')(props)
        },
        item: {
          // this will style the MenuItem and MenuItemOption components
          color: mode('#333333', '#C8D1D9')(props),
          bg: mode('#FFFFFF', '#18191A')(props),
          _hover: {
            bg: mode('rgba(0, 0, 0, 0.1);', 'rgba(27, 136, 112, 0.2);')(props)
          }
        }
      })
    },
    Modal: {
      baseStyle: (props: StyleFunctionProps) => ({
        overlay: {
          bg: 'blackAlpha.600'
        },
        dialog: {
          bg: mode('#FFFFFF', '#18191A')(props)
        }
      })
    }
  }
});
