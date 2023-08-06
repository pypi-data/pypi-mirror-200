import { Box, Stack } from '@chakra-ui/react';
import { InstanceSchema } from '../../types/DatabaseSchema';
import { InstanceLocalSettings } from '../../types/Instance';
import { TableCardList } from './TableCard';
import { Container } from '../utils/layout/Container';

export const TableListComponent = ({
  tab,
  instanceSettings,
  schema
}: {
  tab: string;
  instanceSettings: InstanceLocalSettings;
  schema: InstanceSchema;
}) => {
  return (
    <Container size='lg'>
      <Stack spacing={10}>
        <Box display={'flex'} flex={1} justifyContent={'flex-end'}></Box>
        <TableCardList schema={schema} />
      </Stack>
    </Container>
  );
};
