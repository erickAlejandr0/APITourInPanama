from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import usuarios, actividades
from contextlib import asynccontextmanager


app = FastAPI(
    title="API Movil",
    version="1.0",
    
)


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

