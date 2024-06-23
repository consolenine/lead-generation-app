import React, { createContext, useContext, useState, useEffect } from 'react';
import axiosInstance from '../axiosConfig';
import cookies from 'js-cookie';

const AuthContext = createContext({ user: null, loading: true, setUser: () => {}});

export const useAuth = () => {
    return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axiosInstance.get('/api/accounts/user/');
                setUser(response.data.username);
            } catch (error) {
                cookies.remove('token');
                setUser(null);
            }
            setLoading(false);
        };
        fetchUser();
    }, []);

    return (
        <AuthContext.Provider value={{ user, loading, setUser }}>
        {children}
        </AuthContext.Provider>
    );
};
