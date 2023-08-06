import { Table } from '../types/Table';
import { get } from './utils';

export const getTable = async (schemaName: string, tableName: string) => {
  const tableContent: Table = await get(
    `${process.env.NEXT_PUBLIC_LAMIN_REST_DB_URL}/introspection/${schemaName}/${tableName}`
  );
  console.log("tableContent-----", tableContent)
  return tableContent;
};
