import { Box, Heading } from '@chakra-ui/react';
import { createColumnHelper } from '@tanstack/table-core';
import {
  EntityPageBody,
  EntityPageLayout,
  EntityPageMenu
} from '../utils/layout/EntityPageLayout';
import { DataTable } from './DataTable';

export const TableComponent = ({ tableContent }: { tableContent: any }) => {
  const columnHelper = createColumnHelper<any>();

  const columns = Object.values(tableContent.schema.columns).map(
    (column: any) => {
      return columnHelper.accessor(column.key, {
        cell: info => info.getValue(),
        header: column.key
      });
    }
  );

  return (
    <EntityPageLayout>
      <EntityPageMenu>
        <Box alignItems={'center'} display={'flex'} flexDirection={'column'}>
          <Heading fontSize={'2xl'} fontFamily={'body'}>
            {tableContent.schema.key}
          </Heading>
        </Box>
      </EntityPageMenu>
      <EntityPageBody>
        <DataTable data={tableContent.rows} columns={columns} />
      </EntityPageBody>
    </EntityPageLayout>
  );
};
