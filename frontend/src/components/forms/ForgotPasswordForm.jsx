import React from 'react';
import { Formik, Field, Form } from 'formik';
import { Link as ReactRouterLink } from 'react-router-dom';
import { Link as ChakraLink } from '@chakra-ui/react';

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
    HStack
} from "@chakra-ui/react";

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  
const ForgotPasswordForm = () => (
    <Formik
        initialValues={{
            email: '',
            password: '',
            rememberMe: false,
        }}
        onSubmit={ async (values) => {
            await sleep(500);
            alert(JSON.stringify(values, null, 2)); 
        }}
    >
        {({ handleSubmit, errors, touched }) => (
            <Form onSubmit={handleSubmit}>
                <VStack spacing={4} align="flex-start">
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
                    
                    <Button type="submit" colorScheme="green" width="full">
                    Generate Reset Link
                    </Button>
                </VStack>
            </Form>
        )}
        
    </Formik>
);


export default ForgotPasswordForm;