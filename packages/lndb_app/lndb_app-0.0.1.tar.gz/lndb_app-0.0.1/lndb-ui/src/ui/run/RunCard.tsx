import { ArrowDownIcon, ArrowUpIcon } from '@chakra-ui/icons';
import {
  Box,
  Card,
  CardBody,
  CardHeader,
  FormControl,
  HStack,
  Heading,
  IconButton,
  Select,
  Stack,
  useColorModeValue
} from '@chakra-ui/react';

import { ButtonLink, ButtonLinkText } from '../utils/Button';

export const RunCardList = ({
  runs,
  orderBy,
  setOrderBy,
  descending,
  setDescending
}: {
  runs: any[];
  orderBy: string;
  setOrderBy: any;
  descending: boolean;
  setDescending: any;
}) => {
  console.log('descending', descending);
  return (
    <Stack spacing={10}>
      <Box display={'flex'} flex={1} justifyContent={'flex-end'}>
        <HStack spacing={'1rem'}>
          <FormControl>
            <Select
              name="Order by"
              value={orderBy}
              onChange={event => setOrderBy(event.target.value)}
            >
              {['created_at', 'name'].map(orderByOption => (
                <option key={orderByOption} value={orderByOption}>
                  {orderByOption}
                </option>
              ))}
            </Select>
          </FormControl>

          <IconButton
            borderColor={descending ? 'grey' : undefined}
            aria-label="Descending"
            icon={<ArrowDownIcon color={'grey'} />}
            onClick={() => setDescending(true)}
          />

          <IconButton
            borderColor={!descending ? 'grey' : undefined}
            aria-label="Ascending"
            icon={<ArrowUpIcon color={'grey'} />}
            onClick={() => setDescending(false)}
          />
        </HStack>
      </Box>
      <Stack>
        {runs.map((run, i) => (
          <RunCard key={i} run={run} />
        ))}
      </Stack>
    </Stack>
  );
};

export const RunCard = ({ run }: { run: any }) => {
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
        <ButtonLink testId="table-page-link" href={`/run/${run.id}`}>
          <ButtonLinkText
            props={{
              _hover: { textDecoration: 'underline' },
              fontWeight: 500
            }}
          >
            <Heading size="md">{run.id}</Heading>
          </ButtonLinkText>
        </ButtonLink>
      </CardHeader>
      <CardBody fontSize={'0.9rem'} fontWeight={500}></CardBody>
    </Card>
  );
};
