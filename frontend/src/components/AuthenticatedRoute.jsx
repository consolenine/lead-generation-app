import React from 'react';
import { Route, Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const AuthenticatedRoute = () => {
    const { user, loading } = useAuth();

    if (loading) {
        return <div>Loading...</div>;
    }
    return user ? <Outlet /> : <Navigate to="/accounts/login" />;
}

export default AuthenticatedRoute;