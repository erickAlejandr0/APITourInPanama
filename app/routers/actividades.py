from fastapi import APIRouter, HTTPException, Request
import asyncpg
from app.Models.actividadesModel_out import ActividadOut,ActividadCercanaOut
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
        

@router.get("/cercanas_de/{lat}/{lon}/{radio}", response_model=list[ActividadCercanaOut])
async def get_actividad(lat:float, lon:float, radio:float):
    try:
        conn = await connect_db()
        result = await conn.fetch(
            "SELECT * FROM actividades_cercanas_usuario($1,$2,$3)", lat, lon, radio
        )
        await conn.close()

        if not result:
            return {"mensaje": "No hay actividades cercanas en tu ubicación.", "data": []}


        return[dict(row) for row in result]
    except Exception as e:
        raise HTTPException(500,f"error al cargar actividades cercanas: {str(e)}")
        