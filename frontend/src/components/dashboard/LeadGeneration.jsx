import React, { useState } from "react";
import { Outlet } from "react-router-dom";
import {
    Button, Heading, Text, Flex, Box, Icon,
    Divider, useDisclosure, Modal, ModalOverlay,
    ModalContent, ModalHeader, ModalCloseButton,
    ModalBody, ModalFooter, Progress, HStack
} from "@chakra-ui/react";

import {
    IconPlus
} from '@tabler/icons-react';
import { LeadGenerationForm } from "../forms";

const LeadGeneration = () => {

    const { isOpen, onOpen, onClose } = useDisclosure();
    const [leadsGenerated, setLeadsGenerated] = useState({total: 0, completed: 0});


    return (
        <>
            <Flex direction="column" gap={4} mt={[4,4,12]}>
                <HStack justify="space-between">
                    <Button 
                        variant="outline" 
                        colorScheme="green" 
                        px={[10]} 
                        py={[12]}
                        onClick={onOpen}
                    >
                        <Icon as={IconPlus} w={6} h={6} mr={2} />
                        <Text>Create New Request</Text>
                    </Button>
                    {/* <Progress 
                        h={28} 
                        borderRadius="2xl" 
                        flex={0.7}
                        display="flex" 
                        alignItems="center" 
                        flexDirection="column"
                        justifyContent="center"
                        isIndeterminate 
                    >
                        <Text color="green.400" variant="h1" as="b">Lead Generation Task Running</Text>
                        <Heading>2/20</Heading>
                    </Progress> */}
                </HStack>
                <Divider my={2} />
                <Outlet />
            </Flex>
            <Modal onClose={onClose} isOpen={isOpen}>
                <ModalOverlay />
                <ModalContent w="800px" maxW="90%" className="gradient-dark-1">
                    <ModalHeader>Create Request</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <LeadGenerationForm close={onClose} />
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    )
}

export default LeadGeneration;