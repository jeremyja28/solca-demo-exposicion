from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, agenda, catalogos, complemento, exportacion, concentrado

app = FastAPI(
    title="SOLCA - Parte Diario Médico",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "AQUÍ_PEGA_TU_LINK_DE_VERCEL"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(agenda.router, prefix="/agenda", tags=["Agenda"])
app.include_router(catalogos.router, prefix="/catalogos", tags=["Catálogos"])
app.include_router(complemento.router, prefix="/complemento", tags=["Complemento"])
app.include_router(exportacion.router, prefix="/exportar", tags=["Exportación"])
app.include_router(concentrado.router, prefix="/concentrado", tags=["Concentrado"])

@app.get("/health")
def health_check():
    return {"status": "ok", "sistema": "SOLCA Parte Diario"}
