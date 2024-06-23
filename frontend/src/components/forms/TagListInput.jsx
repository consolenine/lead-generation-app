import React, { useEffect, useState } from 'react';
import { Input, Tag, TagLabel, TagCloseButton, Wrap, WrapItem } from '@chakra-ui/react';
import { useFormikContext } from 'formik';

const TagListInput = ({ field, form, ...props }) => {
    const { values } = useFormikContext();
    const [inputValue, setInputValue] = useState('');
    const [tags, setTags] = useState([]);

    const handleInputChange = (e) => {
        setInputValue(e.target.value);
    };

    const handleInputKeyDown = (e) => {
        
        if (e.key === 'Enter' && inputValue.trim() !== '') {
            e.preventDefault();
            setTags([...tags, inputValue.trim()]);
            setInputValue('');
            let temp = tags;
            temp.push(inputValue.trim());
            values[props.name] = temp.join('&');
        }
    };

    const handleRemoveTag = (tagToRemove) => {
        const newTags = tags.filter(tag => tag !== tagToRemove);
        setTags(newTags);
        values[props.name] = newTags.join('&');
    };

    useEffect(() => {
        if (values[props.name]) {
            setTags(values[props.name].split('&'));
        }
    }, []);

    return (
        <>
            <Input
                {...field}
                {...props}
                value={inputValue}
                onChange={handleInputChange}
                onKeyDown={handleInputKeyDown}
                placeholder="Type something and press enter"
            />
            <Wrap mt={2}>
                {tags.map((tag, index) => (
                    <WrapItem key={index}>
                        <Tag size="lg" colorScheme="teal" borderRadius="full">
                            <TagLabel>{tag}</TagLabel>
                            <TagCloseButton onClick={() => handleRemoveTag(tag)} />
                        </Tag>
                    </WrapItem>
                ))}
            </Wrap>
        </>
    );
};

export default TagListInput;