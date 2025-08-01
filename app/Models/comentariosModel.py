from pydantic import BaseModel
from typing import Optional
from datetime import date


class Comentarios(BaseModel):
    id_usuario: int
    id_actividad: int
    titulo: str
    comentario: str
    calificacion: float

class ComentariosOut(BaseModel):
    encabezado: str
    opinion: str
    fecha_creacion: date
    id_user: int
    nombre_usuario: str
    apellido_usuario: str
    foto: str
    rating: float
    sesion: bool
