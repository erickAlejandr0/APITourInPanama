from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import usuarios, actividades,perfiles
from contextlib import asynccontextmanager
from .schedulers.tareas import iniciar_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_scheduler()
    yield


app = FastAPI(
    title="API Movil",
    version="1.0",
    lifespan=lifespan
    
)

@app.get("/")
def root():
    return {"mensaje": "API funcionando correctamente"}


# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)


# Incluir routers
app.include_router(usuarios.router)
app.include_router(actividades.router)
app.include_router(perfiles.router)
