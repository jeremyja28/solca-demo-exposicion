import { useState, useEffect } from 'react';
import { apiClient, exportarConcentradoExcel } from '../services/api';

const GlobalPage = () => {
    const [pacientes, setPacientes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [mes, setMes] = useState(new Date().getMonth() + 1);
    const [anio, setAnio] = useState(new Date().getFullYear());
    const [medicoId, setMedicoId] = useState('');
    const [isDownloading, setIsDownloading] = useState(false);
    const [downloadError, setDownloadError] = useState('');

    const cargarDatos = async () => {
        setLoading(true);
        try {
            // Calcular primer y último día del mes
            const start = new Date(anio, mes - 1, 1).toISOString().split('T')[0];
            const end = new Date(anio, mes, 0).toISOString().split('T')[0];
            
            let url = `/agenda/global?fecha_inicio=${start}&fecha_fin=${end}`;
            if (medicoId) url += `&medico_id=${medicoId}`;
            const res = await apiClient.get(url);
            setPacientes(res.data);
        } catch (error) {
            console.error('Error al cargar agenda global', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        cargarDatos();
    }, [mes, anio]);

    const handleDescargarExcel = async (idMedico) => {
        if (!idMedico) {
            setDownloadError("Por favor, seleccione un médico primero.");
            setTimeout(() => setDownloadError(''), 3000);
            return;
        }
        if (!mes || !anio) {
            setDownloadError("Mes y año son requeridos.");
            setTimeout(() => setDownloadError(''), 3000);
            return;
        }

        setIsDownloading(true);
        setDownloadError('');
        
        try {
            const response = await exportarConcentradoExcel(idMedico, mes, anio);
            const blob = new Blob([response.data], { type: response.headers['content-type'] });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Concentrado_Mensual_Doctor_${idMedico}_${mes}_${anio}.xlsx`);
            document.body.appendChild(link);
            link.click();
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch(e) {
            console.error("Error al exportar", e);
            setDownloadError("Hubo un error al generar el Excel.");
            setTimeout(() => setDownloadError(''), 3000);
        } finally {
            setIsDownloading(false);
        }
    };

    const totalCompletos = pacientes.filter(p => p.ComplementoCompleto).length;

    return (
        <div>
            <div className="mb-4 bg-solca-fila-alterna p-4 border-b border-solca-borde flex items-end gap-4">
                <div>
                    <label className="block text-xs font-bold mb-1">Mes</label>
                    <select className="border p-2 rounded" value={mes} onChange={e => setMes(parseInt(e.target.value))}>
                        <option value={1}>Enero</option>
                        <option value={2}>Febrero</option>
                        <option value={3}>Marzo</option>
                        <option value={4}>Abril</option>
                        <option value={5}>Mayo</option>
                        <option value={6}>Junio</option>
                        <option value={7}>Julio</option>
                        <option value={8}>Agosto</option>
                        <option value={9}>Septiembre</option>
                        <option value={10}>Octubre</option>
                        <option value={11}>Noviembre</option>
                        <option value={12}>Diciembre</option>
                    </select>
                </div>
                <div>
                    <label className="block text-xs font-bold mb-1">Año</label>
                    <input type="number" className="border p-2 rounded w-24" value={anio} onChange={e => setAnio(parseInt(e.target.value))} min="2020" max="2050" />
                </div>
                <div>
                    <label className="block text-xs font-bold mb-1">Médico</label>
                    <select className="border p-2 rounded" value={medicoId} onChange={e => setMedicoId(e.target.value)}>
                        <option value="">Todos los médicos</option>
                        <option value="10">Dr. 10</option>
                        <option value="20">Dr. 20</option>
                    </select>
                </div>
                <button onClick={cargarDatos} className="bg-solca-azul text-white px-4 py-2 rounded">Aplicar filtros</button>
                <div className="ml-auto flex flex-col items-end">
                    <button 
                        onClick={() => handleDescargarExcel(medicoId)} 
                        disabled={isDownloading}
                        className="bg-green-600 hover:bg-green-700 text-white font-bold px-4 py-2 rounded disabled:opacity-50 transition-colors"
                    >
                        {isDownloading ? '⏳ Descargando...' : '⬇ Descargar Excel Mensual'}
                    </button>
                    {downloadError && <span className="text-red-500 text-xs mt-1">{downloadError}</span>}
                </div>
            </div>

            <div className="mb-4 flex gap-4 text-sm font-bold">
                <div className="bg-white border rounded px-4 py-2">Total Pacientes: {pacientes.length}</div>
                <div className="bg-white border rounded px-4 py-2">Partes Completos: {totalCompletos}</div>
                <div className="bg-white border rounded px-4 py-2">Partes Pendientes: {pacientes.length - totalCompletos}</div>
            </div>

            {loading ? (
                <div className="p-8 text-center">Cargando...</div>
            ) : pacientes.length === 0 ? (
                <div className="rounded border p-8 text-center text-gray-500">No hay datos</div>
            ) : (
                <div className="overflow-x-auto rounded border border-solca-borde">
                    <table className="w-full text-left text-sm text-solca-texto">
                        <thead className="bg-solca-azul text-white">
                            <tr>
                                <th className="p-2">Médico</th>
                                <th className="p-2">#</th>
                                <th className="p-2">N° HC</th>
                                <th className="p-2">Apellidos</th>
                                <th className="p-2">Nombres</th>
                                <th className="p-2">Diagnóstico</th>
                                <th className="p-2">Convenio</th>
                                <th className="p-2">Especialidad</th>
                                <th className="p-2">Actividad</th>
                                <th className="p-2">Consulta</th>
                            </tr>
                        </thead>
                        <tbody>
                            {pacientes.map((p, index) => {
                                const isComplete = p.ComplementoCompleto;
                                return (
                                    <tr key={index} className={`border-t border-solca-borde ${isComplete ? '' : 'text-gray-400'}`}>
                                        <td className="p-2">{p.MedicoId}</td>
                                        <td className="p-2">{index + 1}</td>
                                        <td className="p-2">{p.N_HC}</td>
                                        <td className="p-2">{p.Apellidos}</td>
                                        <td className="p-2">{p.Nombres}</td>
                                        <td className="p-2">{p.Diagnostico}</td>
                                        <td className="p-2">{p.Convenio}</td>
                                        <td className="p-2">{p.Complemento?.EspecialidadId || '-'}</td>
                                        <td className="p-2">{p.Complemento?.ActividadId || '-'}</td>
                                        <td className="p-2">{p.Complemento?.TipoConsulta || '-'}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default GlobalPage;
