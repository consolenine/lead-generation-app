import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Table, TableContainer, TableCaption, Thead, 
    Tbody, Tfoot, Tr, Th, Td, Box,
} from '@chakra-ui/react';
import axiosInstance from '../../axiosConfig';
import { format } from 'date-fns';

const ReqList = ({ type }) => {

    const [columns, setColumns] = useState(['Index', 'Status', 'Created At', 'Time Running', 'Leads Generated']);
    const [data, setData] = useState([]);
    const dateColumnPattern = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z/;

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return format(date, 'd MMMM, yyyy - h:mm:ss a');
    };

    const navigate = useNavigate();
    const openLeadDetails = (id) => {
        navigate(`/dashboard/lead-generation/scraping-task/${id}`);
    }

    useEffect(() => {
        axiosInstance.get(`/api/scraper/scraping-tasks/${type}`)
        .then((response) => {
            const data = response.data.data;
            setColumns(data.length > 0 ? Object.keys(data[0]) : []);
            setData(data);
        })
        .catch((error) => {
            console.log(error);
        });
    },[]);

    return (
        <TableContainer>
            <Table variant='unstyled'>
                <Thead>
                    <Tr borderBottom="1px solid" borderBottomColor="whiteAlpha.200">
                        {columns.map((column, columnIndex) => (
                            <Th key={columnIndex}>{column}</Th>
                        ))}
                    </Tr>
                </Thead>
                <Tbody>
                    {data.length > 0 ? data.map((row, rowIndex) => (
                        <Tr 
                            key={rowIndex}
                            _hover={{ background: 'whiteAlpha.100', cursor: 'pointer' }}
                            onClick={() => openLeadDetails(row['id'])}
                        >
                            {columns.map((column, columnIndex) => (
                                <Td key={columnIndex}>
                                    {dateColumnPattern.test(row[column]) 
                                        ? formatDate(row[column])
                                        : row[column]}
                                </Td>
                            ))}
                        </Tr>
                    )) : 
                    <Tr>
                        <Td colSpan={columns.length} textAlign='center'>
                            <Box p={4} color='red.800' borderRadius='md'>
                                No data available
                            </Box>
                        </Td>
                    </Tr>}
                </Tbody>
            </Table>
        </TableContainer>
    )
}

export default ReqList;