from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import usuarios, actividades,perfiles
from contextlib import asynccontextmanager


app = FastAPI(
    title="API Movil",
    version="1.0",
    
)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}


# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajustar en producción
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(usuarios.router)
app.include_router(actividades.router)
app.include_router(perfiles.router)
