

import React from 'react';
import { Box, Flex } from '@chakra-ui/react';

const SidebarLink = ({ active, children, ...props }) => {
    return (
        <Box
            as="button"
            w="100%"
            py={4}
            px={4}
            textAlign="left"
            bg={active ? 'gray.900' : (props.bg || '#101010')}
            borderRight={active ? '4px solid #38A169' : '4px solid transparent'}
            borderRadius={16}
            color={active ? 'white' : 'white'}
            _active={{ bg: 'teal.900' }}
            {...props}
        >
            <Flex>
                {children}
            </Flex>
        </Box>
    );
};

export default SidebarLink;
