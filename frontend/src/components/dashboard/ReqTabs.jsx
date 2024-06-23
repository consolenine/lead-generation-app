import React from 'react';
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import ReqList from './ReqList';

const ReqTabs = () => {
    return (
        <Tabs variant='soft-rounded' colorScheme='green' mt={4}>
            <TabList>
                <Tab>All Requests</Tab>
                <Tab>Queued</Tab>
                <Tab>Completed</Tab>
                <Tab>Failed</Tab>
            </TabList>
            <TabPanels>
                <TabPanel>
                    <ReqList />
                </TabPanel>
                <TabPanel>
                <p>two!</p>
                </TabPanel>
                <TabPanel>
                <p>four!</p>
                </TabPanel>
                <TabPanel>
                <p>five!</p>
                </TabPanel>
            </TabPanels>
        </Tabs>
    )
}

export default ReqTabs;