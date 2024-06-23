import { Link as ReactRouterLink, Navigate } from 'react-router-dom';
import {
    Box, Flex, Heading, Text, ButtonGroup, Button, VStack, Link as ChakraLink
} from "@chakra-ui/react";

import { useAuth } from '../contexts/AuthContext';

export default function Root() {

    const { user } = useAuth();

    if (user) {
        return <Navigate to="/dashboard/lead-generation" />;
    }

    return (
        <Box px={3} className="gradient-dark-1">
            <Flex align="center" justify="center" height="100vh">
                <VStack p={4}>
                    <Heading size="3xl" textAlign="center" color="green.400">Spotify Live Leads</Heading>
                    <Text mt={4} textAlign="center">Lead Generation Solution For Music Artists</Text>
                    <ButtonGroup mt={6} spacing={4} justifyContent="center">
                        <ChakraLink as={ReactRouterLink} to="/accounts/signup">
                            <Button colorScheme="green">Get Started</Button>
                        </ChakraLink>
                        <ChakraLink as={ReactRouterLink} to="/accounts/login">
                            <Button colorScheme="green" variant="outline">Log In</Button>
                        </ChakraLink>
                    </ButtonGroup>
                </VStack>
            </Flex>
        </Box>
    )
}