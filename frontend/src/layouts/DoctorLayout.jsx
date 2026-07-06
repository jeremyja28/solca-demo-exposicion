import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { HeartPulse, LogOut, UserCircle } from 'lucide-react';
import Logo from '../assets/logo2.png';

const DoctorLayout = ({ children }) => {
    const { usuario, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <div className="min-h-screen bg-slate-50 font-sans text-slate-800 selection:bg-cyan-200 selection:text-cyan-900">
            {/* Header premium */}
            <header className="sticky top-0 z-50 flex h-16 items-center justify-between bg-gradient-to-r from-solca-azul to-blue-900 px-6 shadow-md border-b border-blue-800/50">
                <div className="flex items-center gap-3">
                    <img src={Logo} alt="Logo SOLCA" className="h-10 w-auto object-contain drop-shadow-sm" />
                    <div className="flex flex-col">
                        <span className="text-lg font-bold text-white tracking-wide leading-none">SOLCA</span>
                        <span className="text-xs font-medium text-cyan-200/80 leading-none mt-1">Parte Diario Médico</span>
                    </div>
                </div>
                
                <div className="flex items-center gap-6">
                    <div className="hidden sm:flex items-center gap-2 bg-white/10 px-4 py-1.5 rounded-full border border-white/10">
                        <UserCircle className="h-5 w-5 text-cyan-200" />
                        <span className="text-sm font-medium text-blue-50 tracking-wide">Dr(a). {usuario}</span>
                    </div>
                    <button 
                        onClick={handleLogout}
                        className="group flex items-center gap-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 px-3 py-1.5 text-sm font-medium text-red-100 transition-all border border-red-500/20 hover:border-red-500/40"
                    >
                        <LogOut className="h-4 w-4 group-hover:scale-110 transition-transform" />
                        <span className="hidden sm:inline">Cerrar Sesión</span>
                    </button>
                </div>
            </header>
            
            <main className="mx-auto max-w-7xl p-4 sm:p-6 lg:p-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
                {children}
            </main>
        </div>
    );
};

export default DoctorLayout;
