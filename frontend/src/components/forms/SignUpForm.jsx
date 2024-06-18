import React from 'react';
import { Formik, Field, Form } from 'formik';
import { Link as ReactRouterLink, useNavigate } from 'react-router-dom';
import { Link as ChakraLink } from '@chakra-ui/react';
import axiosInstance from '../../axiosConfig';

import {
    Box,
    Button,
    Checkbox,
    Flex,
    FormControl,
    FormLabel,
    FormErrorMessage,
    Input,
    VStack,
    HStack,
    Alert, AlertIcon, AlertDescription,
} from "@chakra-ui/react";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  
const SignUpForm = () => {
    const navigate = useNavigate();

    return (
        <Formik
            initialValues={{
                firstName: '',
                lastName: '',
                email: '',
                password: ''
            }}
            onSubmit={ async (values, { setSubmitting, setErrors }) => {
                try {
                    const response = await axiosInstance.post('/api/accounts/create/', {
                        first_name: values.firstName,
                        last_name: values.lastName,
                        username: values.email,
                        email: values.email,
                        password: values.password,
                    });

                    if (response.data.username && response.data.username === values.email) {
                        // Redirect to the homepage or dashboard
                        navigate('/accounts/login');
                    } else {
                        setErrors({ general: response.data.username[0] });
                    }

                } catch (error) {
                    // Handle login errors (e.g., show a message to the user)
                    setErrors({ general: 'Unable to create user' });
                    console.log(error);
                } finally {
                    setSubmitting(false);
                }
            }}
        >
            {({ handleSubmit, errors, touched }) => (
                <Form onSubmit={handleSubmit}>
                    <VStack spacing={4} align="flex-start" w={[300,400,500]}>
                        {errors.general && (
                            <Alert status="error" variant="solid">
                                <AlertIcon />
                                <AlertDescription>{errors.general}</AlertDescription>
                            </Alert>
                        )}
                        <HStack w="100%">
                            <FormControl isInvalid={!!errors.firstName && touched.firstName}>
                                <FormLabel htmlFor="firstName">First Name</FormLabel>
                                <Field
                                    as={Input}
                                    id="firstName"
                                    name="firstName"
                                    type="text"
                                    variant="filled"
                                    p={6}
                                    validate={(value) => {
                                        let error;

                                        if (!value) {
                                            error = "First Name is required";
                                        }

                                        return error;
                                    }}

                                />
                                <FormErrorMessage>
                                    {errors.firstName}
                                </FormErrorMessage>
                            </FormControl>
                            <FormControl isInvalid={!!errors.lastName && touched.lastName}>
                                <FormLabel htmlFor="lastName">Last Name</FormLabel>
                                <Field
                                    as={Input}
                                    id="lastName"
                                    name="lastName"
                                    type="text"
                                    variant="filled"
                                    p={6}

                                />
                                <FormErrorMessage>
                                    {errors.lastName}
                                </FormErrorMessage>
                            </FormControl>
                        </HStack>
                        <FormControl isInvalid={!!errors.email && touched.email}>
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
                        <Button type="submit" colorScheme="green" width="full" mt={4}>
                        Create Account
                        </Button>
                        <ChakraLink as={ReactRouterLink} to='/accounts/login'>
                            Already Have An Account? Login
                        </ChakraLink>
                    </VStack>
                </Form>
            )}
            
        </Formik>
    );
}


export default SignUpForm;