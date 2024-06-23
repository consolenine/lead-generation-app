import React from 'react';
import {
    Table, Thead, Tbody, Tr, Th, Td, 
    TableContainer, Box, Tag, Wrap, WrapItem, Link
} from '@chakra-ui/react';

const LeadsTable = ({ leads }) => {
    const parsePlaylist = (playlistStr) => {
        const match = playlistStr.match(/^\('(.+?)', '(.+?)'\)$/);
        return match ? { id: match[1], name: match[2] } : { id: '', name: '' };
    };

    return (
        <Box overflowX="scroll" width="80vw">
            <TableContainer>
                <Table variant="unstyled">
                    <Thead>
                        <Tr>
                            <Th>ID</Th>
                            <Th>Spotify Username</Th>
                            <Th>Contact</Th>
                            <Th>Related Playlists</Th>
                            <Th>Links</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {leads.map((lead, leadIndex) => (
                            <Tr key={leadIndex}>
                                <Td>{leadIndex + 1}</Td>
                                <Td>
                                    <Link href={`https://open.spotify.com/user/${lead.spotify_username.id}`} isExternal>
                                        {lead.spotify_username.name}
                                    </Link>
                                </Td>
                                <Td>
                                    <Box>
                                        {lead.email.length > 0 && (<strong>Email:</strong>)}
                                        <Wrap>
                                            {lead.email.map((email, index) => (
                                                <WrapItem key={leadIndex+"email-"+index}>
                                                    <Tag colorScheme="blue">
                                                        {email}
                                                    </Tag>
                                                </WrapItem>
                                            ))}
                                        </Wrap>
                                        {lead.phone.length > 0 && (<strong>Phone:</strong>)}
                                        <Wrap>
                                            {lead.phone.map((phone, index) => (
                                                <WrapItem key={leadIndex+"phone-"+index}>
                                                    <Tag colorScheme="green">
                                                        {phone}
                                                    </Tag>
                                                </WrapItem>
                                            ))}
                                        </Wrap>
                                    </Box>
                                </Td>
                                <Td>
                                    <Wrap>
                                        {lead.related_playlists.map((playlistStr, index) => {
                                            const { id, name } = parsePlaylist(playlistStr);
                                            return (
                                                <WrapItem key={index}>
                                                    <Link href={`https://open.spotify.com/playlist/${id}`} isExternal>
                                                        <Tag colorScheme="purple">
                                                            {name.length > 20 ? name.slice(0, 20) + '...' : name}
                                                        </Tag>
                                                    </Link>
                                                </WrapItem>
                                            );
                                        })}
                                    </Wrap>
                                </Td>
                                <Td>
                                    <Box>
                                        {lead.free_links.length > 0 && (<strong>Free Links:</strong>)}
                                        <Wrap>
                                            {lead.free_links.map((link, index) => (
                                                <WrapItem key={leadIndex+"free-links-"+index}>
                                                    <Link href={link} isExternal>
                                                        <Tag colorScheme="teal">
                                                            {link}
                                                        </Tag>
                                                    </Link>
                                                </WrapItem>
                                            ))}
                                        </Wrap>
                                        {lead.paid_links.length > 0 && (<strong>Paid Links:</strong>)}
                                        <Wrap>
                                            {lead.paid_links.map((link, index) => (
                                                <WrapItem key={leadIndex+"paid-links-"+index}>
                                                    <Link href={link} isExternal>
                                                        <Tag colorScheme="red">
                                                            {link}
                                                        </Tag>
                                                    </Link>
                                                </WrapItem>
                                            ))}
                                        </Wrap>
                                        {lead.others_links.length > 0 && (<strong>Other Links:</strong>)}
                                        <Wrap>
                                            {lead.others_links.map((link, index) => (
                                                <WrapItem key={leadIndex+"other-links-"+index}>
                                                    <Link href={link} isExternal>
                                                        <Tag colorScheme="orange">
                                                            {link}
                                                        </Tag>
                                                    </Link>
                                                </WrapItem>
                                            ))}
                                        </Wrap>
                                    </Box>
                                </Td>
                            </Tr>
                        ))}
                    </Tbody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default LeadsTable;
