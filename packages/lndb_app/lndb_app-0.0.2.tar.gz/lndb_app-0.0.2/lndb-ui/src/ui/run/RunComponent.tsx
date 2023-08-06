import { Box } from '@chakra-ui/react';

import {
  EntityPageBody,
  EntityPageLayout,
  EntityPageMenu
} from '../utils/layout/EntityPageLayout';
import { RunComponentBody, RunComponentTabName } from './RunComponentBody';

export const RunComponent = ({
  tab,
  run,
  orderByFile,
  setOrderByFile,
  descendingFile,
  setDescendingFile
}: {
  tab: RunComponentTabName;
  run: any;
  orderByFile: string;
  setOrderByFile: any;
  descendingFile: boolean;
  setDescendingFile: any;
}) => {
  return (
    <EntityPageLayout>
      <EntityPageMenu>
        <Box
          alignItems={'center'}
          display={'flex'}
          flexDirection={'column'}
        ></Box>
      </EntityPageMenu>
      <EntityPageBody>
        <RunComponentBody
          currentTab={tab}
          run={run}
          orderByFile={orderByFile}
          setOrderByFile={setOrderByFile}
          descendingFile={descendingFile}
          setDescendingFile={setDescendingFile}
        />
      </EntityPageBody>
    </EntityPageLayout>
  );
};
