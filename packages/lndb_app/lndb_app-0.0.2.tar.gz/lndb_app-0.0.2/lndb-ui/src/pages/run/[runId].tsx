import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

import { getRun } from '../../services/run';
import { RunComponent } from '../../ui/run/RunComponent';
import { RunComponentTabName } from '../../ui/run/RunComponentBody';
import { Spinner } from '../../ui/utils/Spinner';

function Run() {
  const router = useRouter();

  const [run, setRun] = useState<any>();
  const [orderByFile, setOrderByFile] = useState('created_at');
  const [descendingFile, setDescendingFile] = useState(true);

  const { runId, tab } = router.query;

  useEffect(() => {
    if (runId) {
      getRun(runId as string, orderByFile, descendingFile).then(res =>
        setRun(res)
      );
    }
  }, [runId, orderByFile, descendingFile]);

  if (run) {
    return (
      <RunComponent
        tab={tab as RunComponentTabName}
        run={run}
        orderByFile={orderByFile}
        setOrderByFile={setOrderByFile}
        descendingFile={descendingFile}
        setDescendingFile={setDescendingFile}
      />
    );
  }

  return <Spinner />;
}

export default Run;
