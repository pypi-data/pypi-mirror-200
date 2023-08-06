import {
  Box,
  Circle,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  useColorModeValue
} from '@chakra-ui/react';
import { useRouter } from 'next/router';

import { getStatCircleWidth } from '../../../utils/getStatCircleWidth';

export const CustomTabs = ({
  tabs,
  currentTabIndex
}: {
  tabs: { [tabName: string]: TabItem };
  currentTabIndex: number;
}) => {
  return (
    <Tabs variant="unstyled" index={currentTabIndex}>
      <TabList marginBottom={'5%'}>
        {Object.values(tabs).map((tab, i) => (
          <TabListItem key={i} tab={tab} />
        ))}
      </TabList>

      <TabPanels>
        {Object.values(tabs).map((tab, i) => (
          <TabPanel key={i}> {tab.component} </TabPanel>
        ))}
      </TabPanels>
    </Tabs>
  );
};

const TabListItem = ({ tab }: { tab: TabItem }) => {
  const router = useRouter();
  return (
    <Tab
      data-test-id={tab.testId}
      onClick={() => router.push(tab.url, undefined, { shallow: true })}
    >
      {tab.title}
      <TabStat tabStat={tab.stat} />
    </Tab>
  );
};

const TabStat = ({ tabStat }: { tabStat?: number }) => {
  const statColor = useColorModeValue('#C3C3C3', '#242526');
  if (tabStat?.valueOf) {
    return (
      <Circle
        style={{
          margin: 5,
          fontSize: 12,
          fontWeight: 'bold',
          backgroundColor: statColor,
          height: '2.5vh',
          width: getStatCircleWidth(tabStat)
        }}
      >
        <Box>{tabStat}</Box>
      </Circle>
    );
  }
  return null;
};

export interface TabItem {
  index: number;
  title: string;
  url: string;
  stat?: number;
  component: JSX.Element;
  testId: string;
}
