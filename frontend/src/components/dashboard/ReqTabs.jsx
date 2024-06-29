import React from 'react';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import ReqList from './ReqList';

const ReqTabs = () => {
    return (
        <Tabs variant='soft-rounded' colorScheme='green' mt={4} isLazy>
            <TabList>
                <Tab>All Requests</Tab>
                <Tab>Queued</Tab>
                <Tab>Completed</Tab>
                <Tab>Failed</Tab>
            </TabList>
            <TabPanels>
                <TabPanel>
                    <ReqList type="all" />
                </TabPanel>
                <TabPanel>
                    <ReqList type="queued" />
                </TabPanel>
                <TabPanel>
                    <ReqList type="completed" />
                </TabPanel>
                <TabPanel>
                    <ReqList type="failed" />
                </TabPanel>
            </TabPanels>
        </Tabs>
    )
}

export default ReqTabs;