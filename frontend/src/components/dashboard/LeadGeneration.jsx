import { Outlet } from "react-router-dom";
import {
    Button, Heading, Text, Flex, Box, Icon,
    Divider, useDisclosure, Modal, ModalOverlay,
    ModalContent, ModalHeader, ModalCloseButton,
    ModalBody, ModalFooter
} from "@chakra-ui/react";

import {
    IconPlus
} from '@tabler/icons-react';
import { LeadGenerationForm } from "../forms";

const LeadGeneration = () => {

    const { isOpen, onOpen, onClose } = useDisclosure();


    return (
        <>
            <Flex direction="column" gap={4} mt={[4,4,12]}>
                <Box>
                    <Button 
                        variant="outline" 
                        colorScheme="green" 
                        px={[10]} 
                        py={[20]}
                        onClick={onOpen}
                    >
                        <Icon as={IconPlus} w={6} h={6} mr={2} />
                        <Text>Create New Request</Text>
                    </Button>
                </Box>
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