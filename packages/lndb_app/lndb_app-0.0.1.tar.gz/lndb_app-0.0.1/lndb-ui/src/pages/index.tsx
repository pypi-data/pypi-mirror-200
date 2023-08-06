import {
  Box,
  Card,
  CardBody,
  Heading,
  Stack,
  StackDivider,
  Text
} from '@chakra-ui/react';
import { config } from '@fortawesome/fontawesome-svg-core';
import '@fortawesome/fontawesome-svg-core/styles.css';
import { useEffect, useState } from 'react';

import { getCurrentInstance } from '../services/instance';
import { Instance } from '../types/Instance';
import { Spinner } from '../ui/utils/Spinner';
import { Container } from '../ui/utils/layout/Container';
import {
  getInstanceDBHost,
  getInstanceDialect,
  getSchemaModules
} from '../utils/instance';
import { prettifyDatetimeString } from '../utils/string';

config.autoAddCss = false; /* eslint-disable import/first */

function Index() {
  const [instance, setInstance] = useState<any>();

  useEffect(() => {
    getCurrentInstance().then(res => setInstance(res));
  }, []);

  if (instance) {
    return (
      <Container size="md">
        <InstanceMetadata instance={instance} />
      </Container>
    );
  }

  return <Spinner />;
}

const InstanceMetadata = ({ instance }: { instance: Instance }) => {
  return (
    <Stack spacing={5}>
      <Card>
        <CardBody>
          <Stack divider={<StackDivider />} spacing="4">
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Database Type
              </Heading>
              <Text pt="2" fontSize="sm">
                {getInstanceDialect(instance)}
              </Text>
            </Box>
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Database Host
              </Heading>
              <Text pt="2" fontSize="sm">
                {getInstanceDBHost(instance)}
              </Text>
            </Box>
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Default Storage
              </Heading>
              <Text pt="2" fontSize="sm">
                {instance.storage.root}
              </Text>
            </Box>
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Schema Modules
              </Heading>
              <Text pt="2" fontSize="sm">
                {getSchemaModules(instance)}
              </Text>
            </Box>
            <Box>
              <Heading size="xs" textTransform="uppercase">
                Created At
              </Heading>
              <Text pt="2" fontSize="sm">
                {prettifyDatetimeString(instance.created_at)}
              </Text>
            </Box>
          </Stack>
        </CardBody>
      </Card>
    </Stack>
  );
};

export default Index;
