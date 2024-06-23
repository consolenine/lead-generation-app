import React, { useState } from 'react';
import { Formik, Field, Form } from 'formik';
import { Link as ReactRouterLink, useNavigate } from 'react-router-dom';
import { Link as ChakraLink } from '@chakra-ui/react';
import axiosInstance from '../../axiosConfig';
import Cookies from 'js-cookie';
import { useAuth } from '../../contexts/AuthContext';

import {
    Box, Button, Checkbox, Flex, FormControl,
    FormLabel, FormErrorMessage, Input, VStack, 
    CircularProgress, Alert, AlertIcon, AlertDescription,
} from "@chakra-ui/react";

import ShakeBox from '../ShakeBox';

  
const LoginForm = () => {
    const navigate = useNavigate();
    const { setUser } = useAuth();
    const [ processing, setProcessing ] = useState(false);

    return (
        <Formik
            initialValues={{
                email: '',
                password: '',
                rememberMe: false,
            }}

            onSubmit={ async (values, { setSubmitting, setErrors }) => {
                setProcessing(true);
                try {
                    const response = await axiosInstance.post('/api/accounts/login/', {
                        username: values.email,
                        password: values.password,
                    });

                    if (response.data.user) {
                        const { token, expiry, user } = response.data;
                        setUser(user.username);
                        Cookies.set('token', token, { expires: new Date(expiry), sameSite: 'Lax' });
                    }

                    // Redirect to the homepage or dashboard
                    navigate('/dashboard/lead-generation');

                } catch (error) {
                    // Handle login errors (e.g., show a message to the user)
                    setErrors({ general: 'Invalid email or password' });
                    setProcessing(false);
                    console.log(error);
                } finally {
                    setSubmitting(false);
                }
            }}
        >
            {({ handleSubmit, errors, touched }) => (
                <Form onSubmit={handleSubmit}>
                    <VStack spacing={4} align="flex-start">
                        {errors.general && (
                            <ShakeBox isError={true}>
                                <Alert status="error" variant="solid">
                                    <AlertIcon />
                                    <AlertDescription>{errors.general}</AlertDescription>
                                </Alert>
                            </ShakeBox>
                        )}
                        <FormControl w={[300,400,500]} isInvalid={!!errors.email && touched.email}>
                            <FormLabel htmlFor="email">Email Address</FormLabel>
                            <Field
                                as={Input}
                                id="email"
                                name="email"
                                type="email"
                                variant="filled"
                                p={6}
                                validate={(value) => {
                                    let error;
                                        
                                    if (!value) {
                                        error = "Email is required";
                                    } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(value)) {
                                        error = "Invalid email address";
                                    }

                                    return error;
                                }}

                            />
                            <FormErrorMessage>
                                {errors.email}
                            </FormErrorMessage>
                        </FormControl>
                        <FormControl isInvalid={!!errors.password && touched.password}>
                            <FormLabel htmlFor="password">Password</FormLabel>
                            <Field
                                as={Input}
                                id="password"
                                name="password"
                                type="password"
                                variant="filled"
                                p={6}
                                validate={(value) => {
                                    let error;

                                    if (value.length < 6) {
                                        error = "Password must contain at least 6 characters";
                                    }

                                    return error;
                                }}
                            />
                            <FormErrorMessage>{errors.password}</FormErrorMessage>
                        </FormControl>
                        <Flex justifyContent="space-between" w="100%">
                            <Field
                                as={Checkbox}
                                id="rememberMe"
                                name="rememberMe"
                                colorScheme="green"
                            >
                            Remember me?
                            </Field>
                            <ChakraLink as={ReactRouterLink} to='/accounts/forgot-password'>
                                Forgot Password?
                            </ChakraLink>

                        </Flex>
                        <Button type="submit" colorScheme="green" width="full">
                            {processing ? (
                                <>
                                Logging in
                                <CircularProgress isIndeterminate size="24px" color="green.400" />
                                </>
                            ) : (
                                "Login"
                            )}
                        </Button>
                        <ChakraLink as={ReactRouterLink} to='/accounts/signup'>
                            Don't have an account? Sign up here
                        </ChakraLink>
                    </VStack>
                </Form>
            )}
            
        </Formik>
    );
}


export default LoginForm;