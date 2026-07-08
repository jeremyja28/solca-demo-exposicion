import axios from 'axios';

// SOLUCIÓN NUCLEAR: URL base hardcodeada para evitar fallos de Vercel/Variables
const API_URL = 'https://solca-demo-exposicion.onrender.com';

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
    return apiClient.get(`/exportar/excel/${medicoId}`, {
        params: { mes, anio },
        responseType: 'blob'
    });
};

export const exportarDiarioExcel = (medicoId, fecha) => {
    return apiClient.get(`/exportar/diario/excel/${medicoId}`, {
        params: { fecha },
        responseType: 'blob'
    });
};

export const exportarDiarioPDF = (medicoId, fecha) => {
    return apiClient.get(`/exportar/diario/pdf/${medicoId}`, {
        params: { fecha },
        responseType: 'blob'
    });
};
