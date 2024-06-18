import React, { forwardRef } from 'react';
import { Link } from 'react-router-dom';
import Cookies from 'js-cookie';

import { 
	Box, Flex, Image, Text, Spacer,
	Tag, TagLabel, Avatar, Heading,
	Menu, MenuButton, MenuList, MenuItem,
	IconButton,
} from "@chakra-ui/react";
import { IconLogout, IconZoomQuestion, IconArticle, IconBell } from '@tabler/icons-react';
import { useAuth } from '../../contexts/AuthContext';

const AvatarLabel = forwardRef(({ iconUrl, user, ...props }, ref) => {
	return (
		<Tag size="md" borderRadius="full" colorScheme="red" ref={ref} {...props}>
			<Avatar size="xs" name={user} src={iconUrl} mr={2} />
			<TagLabel>{user}</TagLabel>
		</Tag>
	);
});

const NotificationMenu = () => {
	return (
		<Menu>
			<MenuButton 
				as={IconButton} 
				size="sm"
				icon={<IconBell />}
				borderRadius="full"
			/>
			<MenuList bg="blackAlpha.600">
				<MenuItem icon={<IconArticle />} bg="">
					No new notifications
				</MenuItem>
			</MenuList>
		</Menu>
	)
}

const Header = ({ ...props }) => {

	const {user, setUser} = useAuth();

	const handleLogout = () => {
		Cookies.remove('token');
		setUser(null);
	}

	return (
		<Flex py="4" height="16">
			<Heading size="lg">
				{props.title}
			</Heading>
			<Spacer />
			<Flex gap={3}>
				<NotificationMenu />
				<Menu>
					<MenuButton 
						as={AvatarLabel} 
						size="sm" 
						user={user} 
						iconUrl={`https://bit.ly/sage-adebayo`} 
						cursor="pointer"
					/>
					<MenuList bg="blackAlpha.600">
						<MenuItem icon={<IconArticle />} bg="">
							Articles
						</MenuItem>
						<MenuItem icon={<IconZoomQuestion />} bg="">
							Support
						</MenuItem>
						<MenuItem 
							icon={<IconLogout />} 
							bg=""
							onClick={handleLogout}
						>
							Logout
						</MenuItem>
					</MenuList>
				</Menu>
			</Flex>
		</Flex>
	)
};

export default Header;
