import { useState, useEffect } from 'react';
import { apiClient, exportarDiarioExcel, exportarDiarioPDF } from '../services/api';
import { useAutoGuardado } from '../hooks/useAutoGuardado';
import { Download, Calendar, Activity, Loader2, CheckCircle2, AlertCircle, FileText, LayoutList, Clock } from 'lucide-react';

const AgendaPage = () => {
    const [pacientes, setPacientes] = useState([]);
    const [especialidades, setEspecialidades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [statusMap, setStatusMap] = useState({});
    const guardar = useAutoGuardado();
    const [actividadesCache, setActividadesCache] = useState({});
    const [isExportingPdf, setIsExportingPdf] = useState(false);
    const [isExportingExcel, setIsExportingExcel] = useState(false);
    const [exportError, setExportError] = useState('');

    useEffect(() => {
        cargarDatos();
        cargarCatalogos();
    }, []);

    const cargarDatos = async () => {
        try {
            const res = await apiClient.get('/agenda/dia');
            setPacientes(res.data);
        } catch (error) {
            console.error('Error al cargar agenda', error);
        } finally {
            setLoading(false);
        }
    };

    const cargarCatalogos = async () => {
        try {
            const resEsp = await apiClient.get('/catalogos/especialidades');
            setEspecialidades(resEsp.data);
        } catch (error) {
            console.error('Error al cargar especialidades', error);
        }
    };

    const handleFieldChange = async (index, field, value) => {
        const nuevosPacientes = [...pacientes];
        const paciente = nuevosPacientes[index];
        
        let comp = paciente.Complemento || {
            EspecialidadId: 0, ActividadId: 0, TipoConsulta: 'PRIMERA_VEZ',
            Pre_QT: false, Pre_QX: false, Quimio: false, EKG: false
        };

        comp = { ...comp, [field]: value };

        if (field === 'EspecialidadId') {
            comp.ActividadId = 0;
            if (value && !actividadesCache[value]) {
                const res = await apiClient.get(`/catalogos/actividades/${value}`);
                setActividadesCache(prev => ({ ...prev, [value]: res.data }));
            }
        }

        paciente.Complemento = comp;
        setPacientes(nuevosPacientes);

        if (comp.EspecialidadId && comp.ActividadId && comp.TipoConsulta) {
            guardar(paciente.AgendamientoId, comp, setStatusMap);
            paciente.ComplementoCompleto = true;
        } else {
            paciente.ComplementoCompleto = false;
        }
    };

    const handleExport = async (tipo) => {
        if (pacientes.length === 0) {
            setExportError("No hay pacientes atendidos el día de hoy para exportar.");
            setTimeout(() => setExportError(''), 3000);
            return;
        }

        const medicoId = pacientes[0].MedicoId;
        const hoy = new Date().toISOString().split('T')[0];

        try {
            if (tipo === 'pdf') setIsExportingPdf(true);
            else setIsExportingExcel(true);
            setExportError('');

            const response = tipo === 'pdf' 
                ? await exportarDiarioPDF(medicoId, hoy)
                : await exportarDiarioExcel(medicoId, hoy);
                
            const blob = new Blob([response.data], { type: response.headers['content-type'] });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `ParteDiario_${hoy}.${tipo === 'excel' ? 'xlsx' : 'pdf'}`;
            document.body.appendChild(a);
            a.click();
            a.parentNode.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch(e) {
            console.error("Error al exportar", e);
            setExportError(`Error al generar el ${tipo.toUpperCase()}.`);
            setTimeout(() => setExportError(''), 3000);
        } finally {
            if (tipo === 'pdf') setIsExportingPdf(false);
            else setIsExportingExcel(false);
        }
    };

    if (loading) {
        return (
            <div className="flex h-[60vh] flex-col items-center justify-center gap-4 text-slate-400">
                <Loader2 className="h-10 w-10 animate-spin text-cyan-500" />
                <p className="text-lg font-medium">Sincronizando agenda con HIS...</p>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            {/* Header Section */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-5 rounded-2xl shadow-sm border border-slate-100">
                <div className="flex items-center gap-3">
                    <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl">
                        <Calendar className="h-6 w-6" />
                    </div>
                    <div>
                        <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Agenda Diaria</h2>
                        <p className="text-sm text-slate-500 font-medium">Gestiona tu parte médico del día</p>
                    </div>
                </div>
                <div className="flex flex-col items-end relative">
                    <div className="flex flex-wrap gap-3">
                        <button onClick={() => handleExport('pdf')} disabled={isExportingPdf} className="group flex items-center gap-2 rounded-xl bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-red-50 hover:text-red-600 border border-slate-200 transition-colors shadow-sm disabled:opacity-50">
                            {isExportingPdf ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4 group-hover:scale-110 transition-transform" />}
                            {isExportingPdf ? 'Generando PDF...' : 'Descargar PDF'}
                        </button>
                        <button onClick={() => handleExport('excel')} disabled={isExportingExcel} className="group flex items-center gap-2 rounded-xl bg-slate-50 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-emerald-50 hover:text-emerald-600 border border-slate-200 transition-colors shadow-sm disabled:opacity-50">
                            {isExportingExcel ? <Loader2 className="h-4 w-4 animate-spin" /> : <Download className="h-4 w-4 group-hover:-translate-y-0.5 transition-transform" />}
                            {isExportingExcel ? 'Generando Excel...' : 'Descargar Excel'}
                        </button>
                    </div>
                    {exportError && <span className="text-red-500 text-xs mt-1 absolute -bottom-5 right-0">{exportError}</span>}
                </div>
            </div>

            {/* Main Content */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                {pacientes.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-20 px-4 text-center">
                        <div className="h-20 w-20 bg-slate-50 rounded-full flex items-center justify-center mb-4">
                            <Activity className="h-10 w-10 text-slate-300" />
                        </div>
                        <h3 className="text-xl font-bold text-slate-700 mb-1">Sin agendamientos</h3>
                        <p className="text-slate-500 max-w-md">No tienes pacientes agendados para el día de hoy en el sistema principal.</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm whitespace-nowrap">
                            <thead>
                                <tr className="bg-slate-50/80 border-b border-slate-100 text-slate-500 font-semibold text-xs uppercase tracking-wider">
                                    <th className="px-4 py-4 w-12 text-center">#</th>
                                    <th className="px-4 py-4">Paciente Info</th>
                                    <th className="px-4 py-4">Diagnóstico</th>
                                    <th className="px-4 py-4 w-48">Especialidad</th>
                                    <th className="px-4 py-4 w-48">Actividad</th>
                                    <th className="px-4 py-4 w-32">Consulta</th>
                                    <th className="px-2 py-4 text-center w-16" title="Pre Quimioterapia">QT</th>
                                    <th className="px-2 py-4 text-center w-16" title="Pre Quirúrgico">QX</th>
                                    <th className="px-2 py-4 text-center w-16" title="Quimioterapia">Q</th>
                                    <th className="px-2 py-4 text-center w-16" title="Electrocardiograma">EKG</th>
                                    <th className="px-4 py-4 w-24 text-right">Estado</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100">
                                {pacientes.map((p, index) => {
                                    const comp = p.Complemento || {};
                                    const acts = actividadesCache[comp.EspecialidadId] || [];
                                    const status = statusMap[p.AgendamientoId];

                                    return (
                                        <tr key={p.AgendamientoId} className="group hover:bg-blue-50/30 transition-colors">
                                            <td className="px-4 py-3 text-center">
                                                <span className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${p.ComplementoCompleto ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-500'}`}>
                                                    {index + 1}
                                                </span>
                                            </td>
                                            
                                            <td className="px-4 py-3">
                                                <div className="font-bold text-slate-800">{p.Apellidos} {p.Nombres}</div>
                                                <div className="flex items-center gap-2 text-xs text-slate-500 mt-1">
                                                    <span className="bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded font-bold border border-blue-100">🕒 {p.Hora || '--:--'}</span>
                                                    <span className="bg-slate-100 px-1.5 py-0.5 rounded font-medium">HC: {p.N_HC}</span>
                                                    <span>{p.Edad} años</span>
                                                    <span>•</span>
                                                    <span>{p.Sexo === 'Femenino' ? 'F' : 'M'}</span>
                                                </div>
                                            </td>

                                            <td className="px-4 py-3 max-w-[200px] truncate" title={p.Diagnostico}>
                                                <div className="font-medium text-slate-700 truncate">{p.Diagnostico}</div>
                                                <div className="flex items-center gap-2 text-xs mt-1">
                                                    <span className="text-blue-600 font-semibold">{p.CIE10}</span>
                                                    <span className="text-slate-400 truncate">{p.Convenio}</span>
                                                </div>
                                            </td>

                                            <td className="px-4 py-3">
                                                <div className="relative">
                                                    <select 
                                                        className="w-full appearance-none bg-white border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-2 pr-8 shadow-sm transition-all hover:border-slate-300 outline-none"
                                                        value={comp.EspecialidadId || ""}
                                                        onChange={(e) => handleFieldChange(index, 'EspecialidadId', parseInt(e.target.value))}
                                                    >
                                                        <option value="">Seleccione...</option>
                                                        {especialidades.map(esp => (
                                                            <option key={esp.Id} value={esp.Id}>{esp.Nombre}</option>
                                                        ))}
                                                    </select>
                                                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
                                                        <LayoutList className="h-4 w-4" />
                                                    </div>
                                                </div>
                                            </td>

                                            <td className="px-4 py-3">
                                                <div className="relative">
                                                    <select 
                                                        className="w-full appearance-none bg-white border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-2 pr-8 shadow-sm transition-all hover:border-slate-300 outline-none disabled:bg-slate-50 disabled:text-slate-400"
                                                        disabled={!comp.EspecialidadId}
                                                        value={comp.ActividadId || ""}
                                                        onChange={(e) => handleFieldChange(index, 'ActividadId', parseInt(e.target.value))}
                                                    >
                                                        <option value="">Seleccione...</option>
                                                        {acts.map(act => (
                                                            <option key={act.Id} value={act.Id}>{act.Nombre}</option>
                                                        ))}
                                                    </select>
                                                    <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-slate-400">
                                                        <Activity className="h-4 w-4" />
                                                    </div>
                                                </div>
                                            </td>

                                            <td className="px-4 py-3">
                                                <select 
                                                    className="w-full bg-white border border-slate-200 text-slate-700 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block p-2 shadow-sm transition-all hover:border-slate-300 outline-none"
                                                    value={comp.TipoConsulta || "PRIMERA_VEZ"}
                                                    onChange={(e) => handleFieldChange(index, 'TipoConsulta', e.target.value)}
                                                >
                                                    <option value="PRIMERA_VEZ">1ra Vez</option>
                                                    <option value="SUBSECUENTE">Subsc.</option>
                                                </select>
                                            </td>

                                            {['Pre_QT', 'Pre_QX', 'Quimio', 'EKG'].map((field) => (
                                                <td key={field} className="px-2 py-3 text-center align-middle">
                                                    <div className="flex justify-center">
                                                        <label className="relative flex cursor-pointer items-center rounded-full p-2">
                                                            <input 
                                                                type="checkbox" 
                                                                className="peer cursor-pointer appearance-none rounded-md border border-slate-300 h-5 w-5 checked:border-blue-600 checked:bg-blue-600 transition-all focus:ring-2 focus:ring-blue-500/30 outline-none"
                                                                checked={comp[field] || false} 
                                                                onChange={e => handleFieldChange(index, field, e.target.checked)} 
                                                            />
                                                            <div className="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 peer-checked:opacity-100 transition-opacity">
                                                                <svg xmlns="http://www.w3.org/2000/svg" className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor" stroke="currentColor" strokeWidth="1">
                                                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"></path>
                                                                </svg>
                                                            </div>
                                                        </label>
                                                    </div>
                                                </td>
                                            ))}

                                            <td className="px-4 py-3 text-right">
                                                <div className="flex justify-end items-center h-full">
                                                    {status === 'guardando' && (
                                                        <span className="flex items-center gap-1 text-slate-400 bg-slate-50 px-2 py-1 rounded-md text-xs font-medium border border-slate-100">
                                                            <Loader2 className="h-3 w-3 animate-spin" /> Guardando
                                                        </span>
                                                    )}
                                                    {status === 'guardado' && (
                                                        <span className="flex items-center gap-1 text-emerald-600 bg-emerald-50 px-2 py-1 rounded-md text-xs font-medium border border-emerald-100/50">
                                                            <CheckCircle2 className="h-3 w-3" /> Guardado
                                                        </span>
                                                    )}
                                                    {status === 'error' && (
                                                        <span className="flex items-center gap-1 text-red-600 bg-red-50 px-2 py-1 rounded-md text-xs font-medium border border-red-100/50">
                                                            <AlertCircle className="h-3 w-3" /> Error
                                                        </span>
                                                    )}
                                                </div>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AgendaPage;
