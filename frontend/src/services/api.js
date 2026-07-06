import axios from 'axios';

// Utiliza la variable de entorno o un fallback local si no existe
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_URL,
});

// Interceptor para agregar el token si está disponible
export const setupAxiosInterceptors = (token) => {
    apiClient.interceptors.request.clear(); // Limpiar previos
    apiClient.interceptors.request.use(config => {
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    });
};

export const exportarConcentradoExcel = (medicoId, mes, anio) => {
    return apiClient.get(`/api/exportacion/excel/${medicoId}`, {
        params: { mes, anio },
        responseType: 'blob'
    });
};

export const exportarDiarioExcel = (medicoId, fecha) => {
    return apiClient.get(`/api/exportacion/diario/excel/${medicoId}`, {
        params: { fecha },
        responseType: 'blob'
    });
};

export const exportarDiarioPDF = (medicoId, fecha) => {
    return apiClient.get(`/api/exportacion/diario/pdf/${medicoId}`, {
        params: { fecha },
        responseType: 'blob'
    });
};
