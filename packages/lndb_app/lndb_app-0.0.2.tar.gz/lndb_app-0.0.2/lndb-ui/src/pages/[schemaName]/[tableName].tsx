import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { getTable } from '../../services/table';
import { Table } from '../../types/Table';
import { TableComponent } from '../../ui/table/TableComponent';
import { Spinner } from '../../ui/utils/Spinner';

export const TablePage = () => {
  const router = useRouter();

  const [tableContent, setTableContent] = useState<Table>();

  const { schemaName, tableName } = router.query;

  useEffect(() => {
    if (tableName) {
      getTable(schemaName as string, tableName as string).then(res => setTableContent(res));
    }
  }, [tableName]);

  if (tableContent) {
    return <TableComponent tableContent={tableContent} />;
  }

  return <Spinner />;
};

export default TablePage;
