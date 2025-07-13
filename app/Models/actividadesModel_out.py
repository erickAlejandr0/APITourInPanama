from pydantic import BaseModel
from typing import Optional

class MensajeOut(BaseModel):
    mensaje: str

class ActividadOut(BaseModel):
    id: int
    encabezado: str
    descp: str
    rating: Optional[float]
    latitud: float
    longitud: float
    foto_url: Optional[str]
    id_cat: int

class ActividadCercanaOut(BaseModel):
    id: int
    encabezado: str
    descp: str
    rating: Optional[float]
    latitud: float
    longitud: float
    distancia_m: float
    foto_url: Optional[str]
    id_cat: int


class Config:
    orm_mode = True