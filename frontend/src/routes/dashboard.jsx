import React, { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/sidebar/Sidebar";
import Header from "../components/dashboard/Header";
import { Box, Flex } from "@chakra-ui/react";

const Dashboard = () => {
    const location = useLocation();
    const [title, setTitle] = useState("Dashboard");

    useEffect(() => {
        const path = location.pathname.split("/").filter(Boolean);
        let newTitle = "Dashboard";
        if (path.length > 1) {
            newTitle += " / " + path.slice(1).map(word => 
                word.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
            ).join(" / ");
        }
        setTitle(newTitle);
    }, [location]);

    return (
        <Flex p={3} gap={4} height="100%">
            <Sidebar />
            <Box p={4} flex={1} className="gradient-dark-1" borderRadius={8}>
                <Header title={title} />
                <Box height="calc(100% - 4rem)" overflow="auto">
                    <Outlet />
                </Box>
            </Box>
        </Flex>
    );
}

export default Dashboard;
