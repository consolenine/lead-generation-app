import React from 'react';
import { Formik, Field, Form } from 'formik';
import axiosInstance from '../../axiosConfig';

import {
    Box, Button, Checkbox, Flex,
    FormControl, FormLabel, Textarea, FormErrorMessage,
    Input, VStack, HStack, useToast,
} from "@chakra-ui/react";

import TagListInput from './TagListInput';

  
const LeadGenerationForm = ({ initialValues, close }) => {
    const defaultValues = {
        username: "",
        tags: "",
        allTagsCheckbox: false,
        min_likes: 0,
        max_likes: 1000000,
        date: '2015-01-01',
        limit: 20,
    };

    const combinedValues = { ...defaultValues, ...initialValues };

    const toast = useToast();
    return (
        <Formik
            initialValues={combinedValues}
            onSubmit={async (values) => {
                try {
                    const response = await axiosInstance.post('/api/scraper/generate/', values);
                    console.log(response);
                    
                } catch (error) {
                    console.error('Error fetching data:', error);
                }
                toast({
                    title: 'Request Submitted',
                    description: "Task has been queued.",
                    status: 'success',
                    duration: 5000,
                    isClosable: true,
                    position: 'bottom-right'
                })
                close();
            }}
        >
            {({ handleSubmit, errors, touched }) => (
                <Form onSubmit={handleSubmit}>
                    <VStack spacing={4} align="stretch">
                        <FormControl isInvalid={!!errors.username && touched.username}>
                            <FormLabel htmlFor="username">User Profile URLs</FormLabel>
                            <Field
                                as={TagListInput}
                                id="username"
                                name="username"
                            />
                            <FormErrorMessage>{errors.username}</FormErrorMessage>
                        </FormControl>
                        
                        <FormControl isInvalid={!!errors.tags && touched.tags}>
                            <FormLabel htmlFor="tags">Enter tags to filter playlists</FormLabel>
                            <Field
                                as={TagListInput}
                                id="tags"
                                name="tags"
                            />
                            <FormErrorMessage>{errors.tags}</FormErrorMessage>
                        </FormControl>
                        
                        <Field
                            as={Checkbox}
                            id="allTagsCheckbox"
                            name="allTagsCheckbox"
                            colorScheme="green"
                        >
                            Match All Tags (Default is Any)
                        </Field>

                        <FormControl isInvalid={!!errors.min_likes && touched.min_likes}>
                            <FormLabel htmlFor="min_likes">Minimum Likes</FormLabel>
                            <Field as={Input} id="min_likes" name="min_likes" type="number" placeholder="Minimum Playlist Likes" />
                            <FormErrorMessage>{errors.min_likes}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.max_likes && touched.max_likes}>
                            <FormLabel htmlFor="max_likes">Maximum Likes</FormLabel>
                            <Field as={Input} id="max_likes" name="max_likes" type="number" placeholder="Maximum Playlist Likes" />
                            <FormErrorMessage>{errors.max_likes}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.date && touched.date}>
                            <FormLabel htmlFor="date">Last Updated Date</FormLabel>
                            <Field as={Input} id="date" name="date" type="date" />
                            <FormErrorMessage>{errors.date}</FormErrorMessage>
                        </FormControl>

                        <FormControl isInvalid={!!errors.limit && touched.limit}>
                            <FormLabel htmlFor="limit">Maximum Leads</FormLabel>
                            <Field as={Input} id="limit" name="limit" type="number" placeholder="Maximum Leads" />
                            <FormErrorMessage>{errors.limit}</FormErrorMessage>
                        </FormControl>

                        <HStack mb={4}>
                            <Button type="submit" colorScheme="green" width="50%">
                                SUBMIT REQUEST
                            </Button>
                            <Button type="button" variant="outline" onClick={close} colorScheme="red" width="50%">
                                CANCEL
                            </Button>
                        </HStack>
                    </VStack>
                </Form>
            )}
        </Formik>
    );
}


export default LeadGenerationForm;