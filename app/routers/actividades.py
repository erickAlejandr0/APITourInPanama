from fastapi import APIRouter, HTTPException, Request
import asyncpg
from app.Models.actividadesModel_out import ActividadOut
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
        raise HTTPException(500,f"error al cargar actividades{str(e)}")

        