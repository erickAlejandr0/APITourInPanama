from pydantic import BaseModel
from typing import Optional


class UsuarioNew(BaseModel):
    nombre:str
    apellido:str
    correo:str
    contrasena:str
    identificacion:str

class UsuarioRegistrado(BaseModel):
    email:str
    password:str

    