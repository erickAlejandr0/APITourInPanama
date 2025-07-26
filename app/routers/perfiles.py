from fastapi import APIRouter, HTTPException, Request,Form, File, UploadFile
import asyncpg
from typing import Union
from app.dataBase.db import connect_db
from app.Models.actividadesModel_out import MensajeOut
from app.Models.perfilModel import FotoPerfilDTO
import uuid

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




@router.put("/cargar/{id}", response_model=MensajeOut)
async def subir_foto(user_id: str = Form(...), imagen: UploadFile = File(...)):
    # 1. Obtener ruta de imagen actual desde la BD
    perfil = supabase.table("perfiles").select("foto").eq("id", user_id).single().execute()
    imagen_actual = perfil.data["foto"] if perfil.data else None

    # 2. Si hay una imagen previa, borrarla
    if imagen_actual:
        nombre_archivo = imagen_actual.split("/")[-1]
        supabase.storage.from_(bucket).remove([nombre_archivo])

    # 3. Subir nueva imagen al bucket
    extension = imagen.filename.split(".")[-1]
    nuevo_nombre = f"{uuid.uuid4()}.{extension}"
    contenido = await imagen.read()

    supabase.storage.from_(bucket).upload(nuevo_nombre, contenido)

    # 4. Obtener URL pública
    nueva_url = supabase.storage.from_(bucket).get_public_url(nuevo_nombre)

    # 5. Actualizar la tabla perfiles
    supabase.table("perfiles").update({"foto": nueva_url}).eq("id", user_id).execute()

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