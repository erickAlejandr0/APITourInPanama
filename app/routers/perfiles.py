from fastapi import APIRouter, HTTPException, Request,Form, File, UploadFile
import asyncpg
from typing import Union
from app.dataBase.db import connect_db
from app.Models.actividadesModel_out import MensajeOut
from app.Models.perfilModel import FotoPerfilDTO
import uuid
from app.services.perfiles_service import cargar_nueva_foto

import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()  # Carga las variables del archivo .env

SUPABASE_URL = os.getenv("SUPABASE_URL")
ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
bucket = os.getenv("SUPABASE_BUCKET")

supabase = create_client(SUPABASE_URL, ANON_KEY)


router = APIRouter(
    prefix="/perfiles",
    tags=["perfiles"]
)




@router.put("/cargar/{user_id}")
async def subir_foto(user_id: str, imagen: UploadFile = File(...)):
    nueva_url= await cargar_nueva_foto(supabase, bucket, user_id, imagen)
    return {"mensaje": "Imagen actualizada", "url": nueva_url}

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