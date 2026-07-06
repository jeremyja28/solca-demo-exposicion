import { useCallback, useRef } from "react";
import { apiClient } from "../services/api";

export function useAutoGuardado() {
    const timerRef = useRef({});

    const guardar = useCallback((agendamientoId, datos, setStatusMap) => {
        if (timerRef.current[agendamientoId]) {
            clearTimeout(timerRef.current[agendamientoId]);
        }
        
        setStatusMap(prev => ({ ...prev, [agendamientoId]: 'guardando' }));

        timerRef.current[agendamientoId] = setTimeout(async () => {
            try {
                await apiClient.put(
                    `/complemento/${agendamientoId}`,
                    datos
                );
                setStatusMap(prev => ({ ...prev, [agendamientoId]: 'guardado' }));
                
                // Limpiar el estado de guardado después de 2s
                setTimeout(() => {
                    setStatusMap(prev => {
                        const newState = { ...prev };
                        if (newState[agendamientoId] === 'guardado') {
                            delete newState[agendamientoId];
                        }
                        return newState;
                    });
                }, 2000);
            } catch (err) {
                console.error("Error al guardar:", err);
                setStatusMap(prev => ({ ...prev, [agendamientoId]: 'error' }));
            }
        }, 500); // 500ms de debounce
    }, []);

    return guardar;
}
