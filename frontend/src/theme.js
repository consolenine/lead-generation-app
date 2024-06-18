import { extendTheme } from '@chakra-ui/react';
import { mode } from '@chakra-ui/theme-tools';

const config = {
	initialColorMode: 'dark',
	useSystemColorMode: false,
}

const styles = {
	global: (props) => ({
		body: {
			bg: '#101010',
			color: 'gray.100',
		}
	})
}

const theme = extendTheme({ config, styles })

export default theme