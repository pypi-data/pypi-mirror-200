import {
  Badge,
  Card,
  CardBody,
  CardHeader,
  Heading,
  Stack,
  useColorModeValue
} from '@chakra-ui/react';
import { useRouter } from 'next/router';
import { InstanceSchema } from '../../types/DatabaseSchema';
import { ButtonLink, ButtonLinkText } from '../utils/Button';

export const TableCardList = ({ schema }: { schema: InstanceSchema }) => {
  return (
    <Stack>
      {
        Object.keys(schema).map(
          schemaName => {
            return schema[schemaName].map(
              (tableName, i) => {
                return (
                  <TableCard
                    key={`${schemaName}-${i}`}
                    schemaName={schemaName}
                    tableName={tableName}
                  />
                )
              }
            )
          }
        )
      }
    </Stack>
  );
};

export const TableCard = ({ tableName, schemaName }: { tableName: string, schemaName: string }) => {
  const router = useRouter();

  const hooverBackgroundColor = useColorModeValue(
    'rgba(0, 0, 0, 0.1);',
    'rgba(27, 136, 112, 0.2);'
  );

  return (
    <Card
      size={'sm'}
      backgroundColor={undefined}
      _hover={{ backgroundColor: hooverBackgroundColor }}
    >
      <CardHeader>
        <ButtonLink testId="table-page-link" href={`/${schemaName}/${tableName.toLowerCase()}`}>
          <ButtonLinkText
            props={{
              _hover: { textDecoration: 'underline' },
              fontWeight: 500
            }}
          >
            <Heading size="md">{tableName}</Heading>
          </ButtonLinkText>
        </ButtonLink>
      </CardHeader>
      <CardBody fontSize={'0.9rem'} fontWeight={500}>
        <Badge ml="1" colorScheme="gray">
          {schemaName}
        </Badge>
      </CardBody>
    </Card>
  );
};
