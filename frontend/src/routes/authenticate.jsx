import React, { useState } from 'react';
import { Link, Outlet, Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

import {
	Box, Flex, VStack, Heading, Spacer, IconButton
} from "@chakra-ui/react";
import { ArrowBackIcon } from '@chakra-ui/icons';

const Authenticator = () => {
	const { user } = useAuth();

    if (user) {
        return <Navigate to="/dashboard" />;
    }
	return (
		<Box className='gradient-dark-1'>
			<VStack px={4} py={4}>
				<Flex minWidth='max-content' alignItems='center' gap='2'>
					<Box p='2'>
						<Heading size='md'>Live Lead Generator</Heading>
					</Box>
					<Spacer />
				</Flex>
				<Flex align="center" justify="start" w={[300,400,500]} mt={[4,8,10]}>
					<Link to={-1}>
						<IconButton 
							aria-label="Back" 
							icon={<ArrowBackIcon />} 
							size="lg" 
							variant="solid"
							isRound={true}
							
						/>
					</Link>
				</Flex>
				<Flex align="center" justify="center" mt={[4,8,10]}>
					<VStack spacing={4}>
						<Outlet />
					</VStack>
				</Flex>
			</VStack>
		</Box>
	);
};

export default Authenticator;


