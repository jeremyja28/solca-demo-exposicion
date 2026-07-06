import { Routes, Route, Navigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import LoginPage from '../pages/LoginPage';
import AgendaPage from '../pages/AgendaPage';
import GlobalPage from '../pages/GlobalPage';
import DoctorLayout from '../layouts/DoctorLayout';

const PrivateRoute = ({ children, allowedRol }) => {
    const { token, rol, loading } = useContext(AuthContext);

    if (loading) return <div>Cargando...</div>;
    
    if (!token) {
        return <Navigate to="/" replace />;
    }

    if (allowedRol && rol !== allowedRol) {
        return <Navigate to="/" replace />;
    }

    return children;
};

const AppRouter = () => {
    return (
        <Routes>
            <Route path="/" element={<LoginPage />} />
            
            <Route path="/doctor" element={
                <PrivateRoute allowedRol="doctor">
                    <DoctorLayout>
                        <AgendaPage />
                    </DoctorLayout>
                </PrivateRoute>
            } />
            
            <Route path="/enfermero" element={
                <PrivateRoute allowedRol="enfermero">
                    <DoctorLayout>
                        <GlobalPage />
                    </DoctorLayout>
                </PrivateRoute>
            } />
        </Routes>
    );
};

export default AppRouter;
