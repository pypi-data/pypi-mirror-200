import { Box } from '@chakra-ui/react';

import {
  EntityPageBody,
  EntityPageLayout,
  EntityPageMenu
} from '../utils/layout/EntityPageLayout';
import { FileComponentBody, FileComponentTabName } from './FileComponentBody';

export const FileComponent = ({
  tab,
  file
}: {
  tab: FileComponentTabName;
  file: any;
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
        <FileComponentBody currentTab={tab} file={file} />
      </EntityPageBody>
    </EntityPageLayout>
  );
};
