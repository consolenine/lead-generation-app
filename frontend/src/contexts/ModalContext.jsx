import React, { createContext, useContext, useState } from 'react';

const ModalContext = createContext();

export const ModalProvider = ({ children }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [modalData, setModalData] = useState(null);

    const openModal = (data = null) => {
        setModalData(data);
        setIsOpen(true);
    };

    const closeModal = () => {
        setModalData(null);
        setIsOpen(false);
    };

    return (
        <ModalContext.Provider value={{ isOpen, modalData, openModal, closeModal }}>
            {children}
        </ModalContext.Provider>
    );
};

export const useModal = () => useContext(ModalContext);
