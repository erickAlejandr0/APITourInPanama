from pydantic import BaseModel
from datetime import date, time

class ItinerarioUsuario(BaseModel):
    id_itinerario: int
    fecha_itinerario: date
    hora_itinerario: time
    nota_itinerario: str
    titulo_actividad: str
    id_act: int