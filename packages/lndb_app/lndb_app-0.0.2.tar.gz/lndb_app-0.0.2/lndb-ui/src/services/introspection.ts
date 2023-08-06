import { useEffect, useState } from 'react';

import { InstanceSchema } from '../types/DatabaseSchema';
import { InstanceLocalSettings } from '../types/Instance';
import { Table } from '../types/Table';
import { get } from './utils';

export const useInstanceSchema = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [instanceSchema, setInstanceSchema] = useState<InstanceSchema>();

  useEffect(() => {
    setLoading(true);
    getInstanceSchema()
      .then(res => setInstanceSchema(res))
      .finally(() => setLoading(false));
  }, []);

  return { loading, instanceSchema };
};

export const useTableSchema = (tableName: string) => {
  const [loading, setLoading] = useState<boolean>(false);
  const [table, setTable] = useState<Table>();

  useEffect(() => {
    setLoading(true);
    getTableSchema(tableName)
      .then(res => setTable(res))
      .then(res => setLoading(false));
  }, []);

  return { loading, table };
};

export const getInstanceSettings = async () => {
  const instanceSettings: InstanceLocalSettings = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/instance/settings`
  );
  return instanceSettings;
};

export const getInstanceSchema = async () => {
  const instanceSchema: InstanceSchema = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/introspection/`
  );
  return instanceSchema;
};

export const getTableSchema = async (tableName: string) => {
  const table: Table = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/introspection/${tableName}`
  );
  return table;
};
