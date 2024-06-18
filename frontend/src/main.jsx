import React from 'react'
import * as ReactDOM from 'react-dom/client'
import {
	createBrowserRouter,
	RouterProvider,
} from "react-router-dom";

import { ChakraProvider, ColorModeScript } from '@chakra-ui/react'
import theme from './theme'

import { Authenticator, Dashboard, Root } from './routes';
import { 
	LoginForm, SignUpForm, ForgotPasswordForm,
	LeadGeneration, LeadsCompiled, ReqDetails,
	ReqTabs,
} from './components';

import './index.css'
import AuthenticatedRoute from './components/AuthenticatedRoute';
import { AuthProvider } from './contexts/AuthContext';

const router = createBrowserRouter([
	{
		path: "/",
		element: <Root />,
	},
	{
		path: "/accounts",
		element: <Authenticator />,
		children: [
			{
				path: "login",
				element: <LoginForm />,
			},
			{
				path: "signup",
				element: <SignUpForm />,
			},
			{
				path: "forgot-password",
				element: <ForgotPasswordForm />,
			}
		],
	},
	{
		path: "/dashboard",
		element: <AuthenticatedRoute />,
		children: [
			{
				path: "",
				element: <Dashboard />,
				children: [
					{
						path: "lead-generation",
						element: <LeadGeneration />,
						children: [
							{
								path: "",
								element: <ReqTabs />,
							},
							{
								path: "scraping-task/:id",
								element: <ReqDetails />,
							}
						]
					},
					{
						path: "leads-all",
						element: <LeadsCompiled />,
					},
				]
			},
		],
	},
]);

ReactDOM.createRoot(document.getElementById('root')).render(
	// <React.StrictMode>
		<ChakraProvider theme={ theme }>
			<ColorModeScript initialColorMode={theme.config.initialColorMode} />
			<AuthProvider>
				<RouterProvider router={router} />
			</AuthProvider>
		</ChakraProvider>
	// </React.StrictMode>
)
