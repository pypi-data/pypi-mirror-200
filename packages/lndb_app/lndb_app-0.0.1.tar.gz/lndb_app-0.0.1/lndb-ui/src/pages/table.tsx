import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import {
  getInstanceSchema,
  getInstanceSettings
} from '../services/introspection';
import { InstanceSchema } from '../types/DatabaseSchema';
import { InstanceLocalSettings } from '../types/Instance';
import { TableListComponent } from '../ui/table/TableListComponent';
import { Spinner } from '../ui/utils/Spinner';

function Introspection() {
  const router = useRouter();

  const { tab } = router.query;

  const [instanceSettings, setInstanceSettings] =
    useState<InstanceLocalSettings>();
  const [instanceSchema, setInstanceSchema] = useState<InstanceSchema>();

  useEffect(() => {
    getInstanceSchema().then(res => setInstanceSchema(res));
    getInstanceSettings().then(res => setInstanceSettings(res));
  }, []);

  console.log(instanceSchema, instanceSettings)

  if (instanceSchema && instanceSettings) {
    return (
      <TableListComponent
        instanceSettings={instanceSettings}
        schema={instanceSchema}
        tab={tab as string}
      />
    );
  }

  return <Spinner />;
}

export default Introspection;
