from pydantic import BaseModel
from typing import Optional

class ActividadOut(BaseModel):
    encabezado: str
    descp: str
    rating: Optional[float]
    latitud: float
    longitud: float
    foto_url: Optional[str]

class ActividadesCategoriaOut(BaseModel):
    id_cat: str
    encabezado: str
    descp: str
    rating: Optional[float]
    latitud: float
    longitud: float
    foto_url: Optional[str]

class Config:
    orm_mode = True