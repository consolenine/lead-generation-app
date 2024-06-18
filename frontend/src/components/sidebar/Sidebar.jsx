import { useLocation, Link as ReactRouterLink } from 'react-router-dom';

import { Box, Flex, Image, Text, 
    Button, Stat, StatLabel, StatNumber, 
    UnorderedList, ListItem, Link as ChakraLink, Icon,
    VStack, Spacer
} from "@chakra-ui/react";
import { 
    IconHome, IconSettings, IconChartDots, IconCreditCard,
    IconHomeFilled, IconSettingsFilled, IconChartDotsFilled, IconCreditCardFilled,
} from '@tabler/icons-react';

import SidebarLink from './SidebarLink';

const Sidebar = () => {
    const location = useLocation();

    return (
        <Flex w="250px" h="100%" bg="#101010" py={4} borderRadius={8} direction="column">

            <VStack spacing={0}>
                <Flex align="center" px={4} mb={14}>
                    <Text fontSize="lg" fontWeight="bold">Live Leads</Text>
                </Flex>
                <SidebarLink as={ReactRouterLink} to="/dashboard/lead-generation" active={location.pathname.startsWith('/dashboard/lead-generation')}>
                    <Icon as={IconHomeFilled} w={6} h={6} mr={4} />
                    <Text>Lead Generation</Text>
                </SidebarLink>
                <SidebarLink as={ReactRouterLink} to="/dashboard/leads-all" active={location.pathname === '/dashboard/leads-all'}>
                    <Icon as={IconChartDots} w={6} h={6} mr={4} />
                    <Text>All Leads</Text>
                </SidebarLink>
                <SidebarLink active={location.pathname === '/dashboard/billing'}>
                    <Icon as={IconCreditCard} w={6} h={6} mr={4} />
                    <Text>Billing</Text>
                </SidebarLink>
                <SidebarLink active={location.pathname === '/dashboard/settings'}>
                    <Icon as={IconSettings} w={6} h={6} mr={4} />
                    <Text>Account</Text>
                </SidebarLink>
            </VStack>

            <Spacer />
            
            <Box mt="auto" p={4}  borderRadius="md">
                <Stat>
                    <StatLabel>Statistic</StatLabel>
                    <StatNumber>DEV MODE</StatNumber>
                </Stat>
            </Box>
        </Flex>
    );
};

export default Sidebar;