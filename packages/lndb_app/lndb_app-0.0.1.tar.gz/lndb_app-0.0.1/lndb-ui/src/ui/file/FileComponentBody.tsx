import { CustomTabs, TabItem } from '../utils/custom-tabs/CustomTabs';

export const FileComponentBody = ({
  file,
  currentTab
}: {
  file: any;
  currentTab: FileComponentTabName;
}) => {
  const baseUrl = `/file/${file.id}`;

  const tabs: { [tabName: string]: TabItem } = {
    run: {
      index: 0,
      title: 'Run',
      url: `${baseUrl}?tab=run`,
      stat: undefined,
      component: null,
      testId: 'file-page-run-tab'
    },
    transform: {
      index: 1,
      title: 'Transform',
      url: `${baseUrl}?tab=transform`,
      stat: undefined,
      component: null,
      testId: 'file-page-transform-tab'
    },
    user: {
      index: 2,
      title: 'User',
      url: `${baseUrl}?tab=user`,
      stat: undefined,
      component: null,
      testId: 'file-page-user-tab'
    }
  };

  return (
    <CustomTabs
      tabs={tabs}
      currentTabIndex={
        tabs[Object.keys(tabs).includes(currentTab) ? currentTab : 'run'].index
      }
    />
  );
};

export type FileComponentTabName = 'run' | 'transform' | 'user';
