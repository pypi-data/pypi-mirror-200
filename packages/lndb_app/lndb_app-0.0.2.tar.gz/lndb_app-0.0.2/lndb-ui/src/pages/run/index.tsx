import { useEffect, useState } from 'react';

import { getRuns } from '../../services/run';
import { RunListComponent } from '../../ui/run/RunListComponent';
import { Spinner } from '../../ui/utils/Spinner';

function Runs() {
  const [runs, setRuns] = useState<any>();
  const [orderBy, setOrderBy] = useState('created_at');
  const [descending, setDescending] = useState(true);

  useEffect(() => {
    getRuns(orderBy, descending).then(res => setRuns(res));
  }, [orderBy, descending]);

  if (runs) {
    return (
      <RunListComponent
        runs={runs}
        orderBy={orderBy}
        setOrderBy={setOrderBy}
        descending={descending}
        setDescending={setDescending}
      />
    );
  }

  return <Spinner />;
}

export default Runs;
