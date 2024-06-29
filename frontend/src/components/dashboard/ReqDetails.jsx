import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axiosInstance from "../../axiosConfig";
import { 
    Table, Thead, Tbody, Tr, 
    Th, Td, Box, Text, List, 
    ListItem, ListIcon, Flex,
    Divider, HStack, VStack, Button,
    useDisclosure, Icon, Skeleton, Link,
    Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody
} from "@chakra-ui/react";
import { IconTag, IconPlus } from "@tabler/icons-react";
import LeadsTable from "./LeadsTable";
import { LeadGenerationForm } from "../forms";

const ReqDetails = () => {
    const { id } = useParams();
    const [task, setTask] = useState({});
    const [leads, setLeads] = useState([]);
    const { isOpen, onOpen, onClose } = useDisclosure();
    const [cloneData, setCloneData] = useState({});

    useEffect(() => {
        axiosInstance.get(`/api/scraper/tasks/${id}/`)
        .then((response) => {
            setTask(response.data.task);
            setLeads(response.data.leads);
            
        })
        .catch((error) => {
            console.log(error);
        });
    
    },[]);

    const cloneReq = () => {
        setCloneData({
            "username": task.config.users.join("&"),
            "tags": task.config.tags.join("&"),
            "allTagsCheckbox": task.config.allTags,
            "min_likes": task.config.min_likes,
            "max_likes": task.config.max_likes,
            "date": task.config.last_updated,
            "limit": task.config.run_limit,
        });
        onOpen();
    }

    const exportToCSV = () => {
        axiosInstance.get(`/api/scraper/tasks/${id}/leads/export`)
        .then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'leads.csv');
            document.body.appendChild(link);
            link.click();
        })
        .catch((error) => {
            console.log(error);
        });
    }

    return (
        <Box>
            <Flex gap={8} mt={[4,4,12]}>
                <Box borderRadius="md">
                    <Table variant="simple" maxWidth="fit-content" border="1px solid" borderColor="gray.700">
                        <Thead>
                        <Tr>
                            <Th>Key</Th>
                            <Th>Value</Th>
                        </Tr>
                        </Thead>
                        <Tbody>
                        {
                            task && Object.entries(task).map(([key, value]) => {
                                if (value instanceof Object) {
                                    return
                                } else {
                                    return (
                                        <Tr key={key}>
                                            {console.log(key)}
                                            <Td>{key}</Td>
                                            <Td>
                                                <Text>{value}</Text>
                                            </Td>
                                        </Tr>
                                    )
                                }
                            }
                            )
                        }
                        </Tbody>
                    </Table>
                </Box>
                <Table variant="simple" maxWidth="fit-content" border="1px solid" borderColor="gray.700">
                    <Thead>
                    <Tr>
                        <Th>Key</Th>
                        <Th>Value</Th>
                    </Tr>
                    </Thead>
                    <Tbody>
                    {task.config &&
                        Object.entries(task.config).map(([key, value]) => (
                        <Tr key={key}>
                            <Td>{key}</Td>
                            <Td>
                            {value instanceof Array ? (
                                <List>
                                {value.map((item, index) => (
                                    <ListItem key={index}>
                                        <ListIcon as={IconTag} color="green.500" />
                                        {item}
                                    </ListItem>
                                ))}
                                </List>
                            ) : value instanceof Boolean ? (
                                <Text>{value ? "True" : "False"}</Text>
                            ) : (<Text>{value}</Text>)}
                            </Td>
                        </Tr>
                        ))}
                    </Tbody>
                </Table>
                <VStack spacing={4} align="flex-start">
                        <Button onClick={cloneReq} variant="outline" colorScheme="blue" size="md">CLONE & RESEND</Button>
                        <Button colorScheme="green" onClick={exportToCSV} size="md">EXPORT LEADS</Button>
                </VStack>
            </Flex>
            <Divider my="4" />
            {
                leads.length > 0  && (
                    <LeadsTable leads={leads} />
                )
            }
            <Modal onClose={onClose} isOpen={isOpen}>
                <ModalOverlay />
                <ModalContent w="800px" maxW="90%" className="gradient-dark-1">
                    <ModalHeader>Create Request</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        <LeadGenerationForm close={onClose} initialValues={cloneData} />
                    </ModalBody>
                </ModalContent>
            </Modal>
        </Box>
    )
}

export default ReqDetails;