import { Container } from '../utils/layout/Container';
import { RunCardList } from './RunCard';

export const RunListComponent = ({
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
  return (
    <Container size="lg">
      <RunCardList
        runs={runs}
        orderBy={orderBy}
        setOrderBy={setOrderBy}
        descending={descending}
        setDescending={setDescending}
      />
    </Container>
  );
};
