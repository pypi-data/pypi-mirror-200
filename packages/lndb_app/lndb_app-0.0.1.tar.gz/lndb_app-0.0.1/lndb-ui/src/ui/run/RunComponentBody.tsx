import { FileCardList } from '../file/FileCard';
import { CustomTabs, TabItem } from '../utils/custom-tabs/CustomTabs';

export const RunComponentBody = ({
  run,
  currentTab,
  orderByFile,
  setOrderByFile,
  descendingFile,
  setDescendingFile
}: {
  run: any;
  currentTab: RunComponentTabName;
  orderByFile: string;
  setOrderByFile: any;
  descendingFile: boolean;
  setDescendingFile: any;
}) => {
  const inputCount = run.Input.length;
  const outputCount = run.Output.length;

  const baseUrl = `/run/${run.Run.id}`;

  const tabs: { [tabName: string]: TabItem } = {
    transform: {
      index: 0,
      title: 'Transform',
      url: `${baseUrl}?tab=transform`,
      stat: undefined,
      component: null,
      testId: 'run-page-transform-tab'
    },
    user: {
      index: 1,
      title: 'User',
      url: `${baseUrl}?tab=user`,
      stat: undefined,
      component: null,
      testId: 'run-page-user-tab'
    },
    inputs: {
      index: 2,
      title: 'Inputs',
      url: `${baseUrl}?tab=inputs`,
      stat: inputCount,
      component: (
        <FileCardList
          files={run.Input}
          orderBy={orderByFile}
          setOrderBy={setOrderByFile}
          descending={descendingFile}
          setDescending={setDescendingFile}
        />
      ),
      testId: 'run-page-inputs-tab'
    },
    outputs: {
      index: 3,
      title: 'Outputs',
      url: `${baseUrl}?tab=outputs`,
      stat: outputCount,
      component: (
        <FileCardList
          files={run.Output}
          orderBy={orderByFile}
          setOrderBy={setOrderByFile}
          descending={descendingFile}
          setDescending={setDescendingFile}
        />
      ),
      testId: 'run-page-outputs-tab'
    }
  };

  return (
    <CustomTabs
      tabs={tabs}
      currentTabIndex={
        tabs[Object.keys(tabs).includes(currentTab) ? currentTab : 'transform']
          .index
      }
    />
  );
};

export type RunComponentTabName = 'transform' | 'user' | 'inputs' | 'outputs';
