from pydantic import BaseModel
from typing import Optional
from datetime import date, time


class Itinerario(BaseModel):
    fecha: date
    hora: time
    nota: str