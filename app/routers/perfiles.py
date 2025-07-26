from fastapi import APIRouter, HTTPException, Request
import asyncpg
from typing import Union
from app.dataBase.db import connect_db
from app.Models.actividadesModel_out import MensajeOut
from app.Models.perfilModel import FotoPerfilDTO

router = APIRouter(
    prefix="/perfiles",
    tags=["perfiles"]
)

@router.put("/cargar/{id}", response_model=MensajeOut)
async def cargarFoto(id: int, u: FotoPerfilDTO):
    try:

        conn = await connect_db()
        result = await conn.fetchval(
             "SELECT * FROM cargar_foto($1,$2)", id, u.foto_url
        )

        if not result:
            return MensajeOut(status_code=400, detail=" No se pudo guardar la foto de perfil")
        else:
            return result
    except Exception as e:
        raise HTTPException(500,f"error al guardar foto  :{str(e)}")
    finally:
        if conn:
            await conn.close() 
    
    
@router.get("/obtener-foto/{id}", response_model=MensajeOut)
async def cargarFoto(id: int):
    try:

        conn = await connect_db()
        result = await conn.fetchval(
                "SELECT * FROM get_foto_usuario($1)", id
        )

        if not result:
            return MensajeOut(mensaje="No se pudo obtener la foto de perfil")
        else:
            return result
    except Exception as e:
        raise HTTPException(500,f"error al guardar foto  :{str(e)}")
    finally:
        if conn:
            await conn.close() 