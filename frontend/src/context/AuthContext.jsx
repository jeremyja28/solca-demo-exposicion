import { createContext, useState, useEffect } from 'react';
import axios from 'axios';
import { setupAxiosInterceptors, apiClient } from '../services/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [token, setToken] = useState(null);
    const [usuario, setUsuario] = useState(null);
    const [rol, setRol] = useState(null);
    const [medicoId, setMedicoId] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // En una app real podríamos validar el token en localStorage,
        // pero la instrucción dice "en memoria (variable de estado, NO en localStorage)".
        setLoading(false);
    }, []);

    const login = async (username, password) => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const res = await apiClient.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            const access_token = res.data.access_token;
            setToken(access_token);
            setupAxiosInterceptors(access_token);
            
            const payloadBase64 = access_token.split('.')[1];
            const payloadDecoded = JSON.parse(atob(payloadBase64));
            
            setUsuario(payloadDecoded.sub);
            setRol(payloadDecoded.rol);
            setMedicoId(payloadDecoded.medico_id);
            return { success: true, rol: payloadDecoded.rol };
        } catch (error) {
            console.error('Error de login', error);
            return { success: false };
        }
    };

    const logout = () => {
        setToken(null);
        setUsuario(null);
        setRol(null);
        setMedicoId(null);
    };

    return (
        <AuthContext.Provider value={{ token, usuario, rol, medicoId, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
