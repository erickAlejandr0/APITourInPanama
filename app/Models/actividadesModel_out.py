from pydantic import BaseModel
from typing import Optional

class ActividadOut(BaseModel):
    titulo: str
    descripcion: str
    calificacion: Optional[float]
    latitud: float
    longitud: float
    foto_url: Optional[str]

class Config:
    orm_mode = True