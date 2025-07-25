from fastapi import APIRouter, HTTPException, Request
import asyncpg
from typing import Union
from app.Models.actividadesModel_out import ActividadOut,ActividadCercanaOut,MensajeOut
from app.Models.itinerarioModel import Itinerario
from app.dataBase.db import connect_db

router = APIRouter(
    prefix="/actividad",
    tags=["actividad"]
)

@router.get("/get", response_model=list[ActividadOut])
async def get_actividad():
    try:
        conn = await connect_db()
        result = await conn.fetch(
            "SELECT * FROM mostrar_actividades()"
        )
        await conn.close()
        if result: 
            return[dict(row) for row in result]
        
        return[]
    except Exception as e:
        raise HTTPException(500,f"error al cargar actividades desde la base de datos{str(e)}")

@router.get("/{idcategoria}", response_model=list[ActividadOut])
async def get_actividad(idcategoria: int):
    try:
        conn = await connect_db()
        result = await conn.fetch(
            "SELECT * FROM actividades_por_categoria($1)", idcategoria
        )
        await conn.close()
        if result: 
            return[dict(row) for row in result]
        
        return[]
    except Exception as e:
        raise HTTPException(500,f"error al cargar actividades desde la base de datos{str(e)}")
        

@router.get("/cercanas_de/{lat}/{lon}/{radio}", response_model=Union[list[ActividadCercanaOut], MensajeOut])
async def get_actividad(lat:float, lon:float, radio:float):
    try:
        conn = await connect_db()
        result = await conn.fetch(
            "SELECT * FROM actividades_cercanas_usuario($1,$2,$3)", lat, lon, radio
        )
        await conn.close()

        if not result:
            return MensajeOut(mensaje="No hay actividades cercanas en tu ubicación.")


        return[dict(row) for row in result]
    except Exception as e:
        raise HTTPException(500,f"error al cargar actividades cercanas: {str(e)}")
    
@router.post("/itinerario", response_model = MensajeOut)
async def save_itinerario(i:Itinerario):
    try:
        conn = await connect_db()
        result = await conn.fetch(
            "SELECT * FROM guardar_actividad($1,$2,$3,$4,$5)",i.fecha,i.hora,i.nota,i.id_u,i.id_act
        )
        await conn.close()
        if result:
            return MensajeOut(mensaje = "actividad guardada en el itinerario")
        else:
            raise HTTPException(status_code=400, detail="No se guardó la actividad")
        
    except Exception as e:
        raise HTTPException(500,f"error al guardar el itinerario:{str(e)}")