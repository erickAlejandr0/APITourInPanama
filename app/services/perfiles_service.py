import uuid
from supabase import Client
from fastapi import UploadFile
from typing import Optional

async def cargar_nueva_foto(
    supabase: Client,
    bucket: str,
    user_id: str,
    file: UploadFile,
) -> Optional[str]:
    # 1. Obtener imagen actual
    perfil = supabase.table("perfil").select("foto_perfil").eq("id_usuario", user_id).single().execute()
    imagen_actual = perfil.data["foto_perfil"] if perfil.data else None

    # 2. Borrar si hay imagen previa
    if imagen_actual:
        nombre_archivo = imagen_actual.split("/")[-1]
        supabase.storage.from_(bucket).remove([nombre_archivo])

    # 3. Subir nueva imagen
    extension = file.filename.split(".")[-1]
    nuevo_nombre = f"{uuid.uuid4()}.{extension}"
    contenido = await file.read()

    supabase.storage.from_(bucket).upload(nuevo_nombre, contenido,{"contentType": f"image/{extension}"})

    # 4. Obtener URL pública
    nueva_url = supabase.storage.from_(bucket).get_public_url(nuevo_nombre)

    # 5. Actualizar tabla perfil
    supabase.table("perfil").update({"foto_perfil": nueva_url}).eq("id_usuario", user_id).execute()

    return nueva_url